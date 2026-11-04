"""3.1.4: shifts named in plain words – how the verifier reads a notice or a mail that has no shift attached.

Fixed rules, no model (VERIFIER_SPEC_V3 § 3e):

- A **shift** is a date and a shift type on one line of the text. A date is any of: `2026-10-09`, `9/10`, `09.10.`,
  `9.10.2026`, `9 Oct`, `9th October`, `October 9`, `9. Oktober`, a weekday with the day (`Fri 9`, `Freitag, 9.`),
  `the 9th`, `am 9.`, `today`/`heute`, `tomorrow`/`morgen`, `tonight` (today's night) – and a weekday alone
  (`Friday`, `Fr.`) when that weekday occurs only once in the planning period. A shift type is `early`/`late`/`night`
  (`earlies`, `night shift` …) or `Früh`/`Spät`/`Nacht` (`Frühdienst`, `Nachtschicht` …). On a line that starts with a
  date, each date takes the shift types after it; on a line that starts with a shift type, each shift type takes the
  dates after it (`Fri 9 Oct night and Sat 10 Oct early`, `the night on Fri 9 Oct`).
- An **open-shift claim** in a mail is a shift on a line that says it is open (`open`, `not covered`, `could not be
  filled`, `short-staffed`, `offen`, `unbesetzt`, `nicht besetzt`, `Unterbesetzung`, `fehlt` …) and does not say it is
  covered after all (`covered`, `filled`, `booked`, `besetzt`, `übernimmt` … not negated) or that it *was* open.
- A role named on that line (`nurse`, `RN`, `care assistant`, `senior`, `Pflegefachkraft`, `Pflegehilfskraft`,
  `Schichtleitung` …) is the role the claim says is missing.
"""

from __future__ import annotations

import re
from collections import Counter
from datetime import date, timedelta
from typing import Any

EN_MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
             "november", "december")
DE_MONTHS = ("januar", "februar", "märz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november",
             "dezember")
EN_DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
DE_DAYS = ("montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag")
EN_DAY_SHORT = (("Mon",), ("Tue", "Tues"), ("Wed",), ("Thu", "Thur", "Thurs"), ("Fri",), ("Sat",), ("Sun",))
DE_DAY_SHORT = ("Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So.")

SHIFT = re.compile(r"(?<![a-zäöüß])(?:(early|late|night)(?:s|\s?shifts?)?(?![a-z])|(earlies)(?![a-z])|(tonight)(?![a-z])|"
                   r"(früh|frueh|spät|spaet|nacht)(?:dienst(?:e|en)?|schicht(?:en)?|e)?(?![a-zäöüß]))", re.IGNORECASE)
SHIFT_OF = {"early": "early", "earlies": "early", "late": "late", "night": "night", "tonight": "night", "früh": "early", "frueh": "early",
            "spät": "late", "spaet": "late", "nacht": "night"}

OPEN = re.compile(
    r"(?:could\s*not|couldn'?t|cannot|can'?t|not|nicht|keine?n?)\s+(?:be\s+|zu\s+)?(?:fill|filled|cover|covered|book|"
    r"booked|staff|staffed|besetz\w*|abgedeckt|abdecken|gefunden|finden)|"
    r"\b(?:open|uncovered|unfilled|understaff\w*|short[- ]staffed|short\s+of|no\s+cover|no\s+one|nobody|gap|"
    r"still\s+need\w*)\b|(?<![a-zäöüß])(?:offen|unbesetzt|unterbesetz\w*|fehl(?:t|en)|niemand|keine\s+vertretung|"
    r"kein\s+ersatz|lücke)(?![a-zäöüß])", re.IGNORECASE)
RESOLVED = re.compile(r"\b(?:covered|filled|sorted|booked|staffed|takes|taking)\b|(?<![a-zäöüß])(?:besetzt|übernimmt|"
                      r"abgedeckt|gebucht|eingeplant|eingetragen)(?![a-zäöüß])", re.IGNORECASE)
PAST = re.compile(r"\b(?:was|were)\s+(?:still\s+)?open\b|\b(?:war|waren)\s+(?:noch\s+)?offen\b", re.IGNORECASE)
ROLES = {
    "registered_nurse": re.compile(r"\b(?:registered\s+nurses?|nurses?|RNs?|RGN)\b|(?<![a-zäöüß])(?:pflegefachkr\w*|"
                                   r"fachkr\w*|examiniert\w*)", re.IGNORECASE),
    "care_assistant": re.compile(r"\b(?:care\s+assistants?|carers?|HCAs?)\b|(?<![a-zäöüß])(?:pflegehilf\w*|hilfskr\w*|"
                                 r"pflegehelfer\w*)", re.IGNORECASE),
    "team_lead": re.compile(r"\b(?:team\s+leads?|team\s+leaders?|shift\s+leads?|shift\s+leaders?|seniors?)\b|"
                            r"(?<![a-zäöüß])(?:schichtleit\w*|teamleit\w*)", re.IGNORECASE),
}


def _ordinal(day: int) -> str:
    return r"(?:st|nd|rd|th)"


def date_patterns(d: date, period: list[date], today: date | None) -> list[re.Pattern]:
    """The ways a text names `d` (see the module text); a weekday alone only when it is unique in `period`."""
    dd, mm, yyyy = d.day, d.month, d.year
    day = rf"0?{dd}"
    months = "|".join(re.escape(m) for m in (EN_MONTHS[mm - 1], EN_MONTHS[mm - 1][:3], "sept" if mm == 9 else "",
                                              DE_MONTHS[mm - 1], DE_MONTHS[mm - 1][:3], "maerz" if mm == 3 else "",
                                              "mär" if mm == 3 else "") if m)
    wd = d.weekday()
    long_days = f"{EN_DAYS[wd]}|{DE_DAYS[wd]}"
    short_days = "|".join(re.escape(s) for s in (*EN_DAY_SHORT[wd], DE_DAY_SHORT[wd]))
    out = [
        rf"(?<!\d){yyyy}-{mm:02d}-{dd:02d}(?!\d)",
        rf"(?<![\d.,:/]){day}[./]0?{mm}(?:[./](?:{yyyy}|{yyyy % 100:02d}))?(?![\d,:/])(?!\.\d)(?!\s*(?:uhr|h\b|€|eur|£))",
        rf"(?<![\d.,:]){day}(?:{_ordinal(dd)}|\.)?\s*(?:of\s+)?(?:{months})\b",
        rf"\b(?:{months})\.?\s+{day}(?:{_ordinal(dd)})?(?![\d:])",
        rf"\b(?:{long_days})\b,?\s+(?:the\s+|den\s+)?{day}(?:{_ordinal(dd)}|\.)?(?![\d:])",
        rf"(?<![A-Za-z])(?:{short_days})(?![a-z]),?\s+(?:the\s+|den\s+)?{day}(?:{_ordinal(dd)}|\.)?(?![\d:])",
        rf"\bthe\s+{day}{_ordinal(dd)}\b|(?<![\d.]){day}{_ordinal(dd)}\b|\bam\s+{day}\.(?!\d)",
    ]
    patterns = [re.compile(p, re.IGNORECASE) for p in out]
    if sum(1 for x in period if x.weekday() == wd) == 1:
        patterns.append(re.compile(rf"\b(?:{long_days})s?\b", re.IGNORECASE))
        patterns.append(re.compile(rf"(?<![A-Za-z])(?:{short_days})(?![a-z])"))  # abbreviations as written: "Fri", "Fr."
    if today is not None and d == today:
        patterns.append(re.compile(r"\b(?:today|tonight)\b|(?<![a-zäöüß])heute(?![a-zäöüß])", re.IGNORECASE))
    if today is not None and d == today + timedelta(days=1):
        patterns.append(re.compile(r"\btomorrow\b|(?<![A-Za-zäöüß])morgen(?![a-zäöüß])"))  # lower case: not "Morgen"
    return patterns


class Reader:
    """Reads shifts out of plain text for one planning period."""

    def __init__(self, period: list[date], today: date | None = None):
        self.period = period
        self.patterns = {d: date_patterns(d, period, today) for d in period}

    def _tokens(self, line: str) -> list[tuple[int, str, str]]:
        tokens: list[tuple[int, str, str]] = []
        for d, patterns in self.patterns.items():
            spans = sorted({m.start() for p in patterns for m in p.finditer(line)})
            last = -100
            for start in spans:  # one token per date mention (several patterns hit "Fri 9 Oct")
                if start - last > 12:
                    tokens.append((start, "D", d.isoformat()))
                last = start
        for m in SHIFT.finditer(line):
            word = next(g for g in m.groups() if g).lower()
            tokens.append((m.start(), "S", SHIFT_OF[word]))
        return sorted(tokens)

    def shifts(self, line: str) -> set[tuple[str, str]]:
        """(date, shift type) pairs named on one line."""
        tokens = self._tokens(line)
        if not tokens:
            return set()
        lead = tokens[0][1]
        pairs: set[tuple[str, str]] = set()
        for i, (_, kind, value) in enumerate(tokens):
            if kind != lead:
                continue
            following = []
            for _, k, v in tokens[i + 1:]:
                if k == lead:
                    if following:
                        break
                    continue  # "Fri 9 Oct, Sat 10 Oct: nights" – dates in a row share what follows
                following.append(v)
            if not following:  # a date in a row without its own type: take the next one's
                for _, k, v in tokens[i + 1:]:
                    if k != lead:
                        following.append(v)
                        break
            pairs |= {(value, v) if lead == "D" else (v, value) for v in following}
        return pairs

    def text_shifts(self, text: str) -> set[tuple[str, str]]:
        found = set()
        for line in text.splitlines():
            found |= self.shifts(line)
        if not found:  # date and type on different lines of a short note: only when each is named once
            tokens = self._tokens(" ".join(text.splitlines()))
            dates = {v for _, k, v in tokens if k == "D"}
            types = {v for _, k, v in tokens if k == "S"}
            if len(dates) == 1 and len(types) == 1:
                found = {(dates.pop(), types.pop())}
        return found

    def open_claims(self, text: str) -> list[tuple[str, str, list[str], str]]:
        """Open-shift claims of a mail: (date, shift type, roles named on the line, the line)."""
        out = []
        for line in text.splitlines():
            if not OPEN.search(line) or PAST.search(line) or RESOLVED.search(OPEN.sub(" ", line)):
                continue
            roles = [q for q, p in ROLES.items() if p.search(line)]
            out += [(d, s, roles, line) for d, s in sorted(self.shifts(line))]
        return out


def period_of(state) -> list[date]:
    start = state.start_date
    return [start + timedelta(days=i) for i in range(state.horizon_days)]


# ------------------------------------------------------------------ shift notices in plain words

SHIFT_FIELDS = ("shift_date", "shift_type", "ward_id")


def plain_notices(actions: list[Any], initial: Any, state: Any,
                  changed_positions: dict[str, set[tuple[str, str, str]]]) -> list[dict[str, Any]]:
    """Shift notices written in plain words (no shift attached), in the notice layer's own form.

    A rota message or a direct chat message to a person whose text names one of their changed shifts is a notice
    about that shift; a team-chat post is a notice for each person it names (full name, or a first name no colleague
    shares) whose changed shift it names. A direct message that names someone else's changed shift is a notice to the
    wrong person (it lowers precision, like a shift notice sent to the wrong person). Messages that name no changed
    shift are ordinary messages and do not count either way. Questions with a shift attached (`ask`) never count."""
    reader = Reader(period_of(initial), today=initial.current_date)
    staff = {e.employee_id: e.name for e in state.employees}
    firsts = Counter(n.split()[0] for n in staff.values())
    anyone = {(d, str(t)) for positions in changed_positions.values() for d, _w, t in positions}
    out: list[dict[str, Any]] = []
    for a in actions:
        args = a.args.get("args") or {}
        if a.args.get("error_code") or all(args.get(k) for k in SHIFT_FIELDS):
            continue  # refused, or a notice with the shift attached (counted as such)
        group = False
        if a.action == "messaging.send" and args.get("recipient_id") and not args.get("request_intent"):
            targets, text = [str(args["recipient_id"])], f"{args.get('subject') or ''}\n{args.get('body') or ''}"
        elif a.action == "chat.post" and not args.get("ask"):
            channel = str(args.get("channel_id") or "")
            who = args.get("employee_id") or (channel[3:] if channel.startswith("dm-") else None)
            text = str(args.get("text") or "")
            if who:
                targets = [str(who)]
            else:
                group = True
                targets = [eid for eid, name in staff.items() if name in text or (
                    firsts[name.split()[0]] == 1 and re.search(rf"(?<![\w-]){re.escape(name.split()[0])}(?![\w-])", text))]
        else:
            continue
        named = reader.text_shifts(text)
        if not named:
            continue
        for who in targets:
            mine = {(d, str(t)): w for d, w, t in changed_positions.get(who, set())}
            hits = sorted(k for k in named if k in mine)
            out += [{"recipient_id": who, "shift_date": d, "shift_type": t, "ward_id": mine[(d, t)]} for d, t in hits]
            if not hits and not group and named & anyone:
                d, t = sorted(named & anyone)[0]
                out.append({"recipient_id": who, "shift_date": d, "shift_type": t, "ward_id": "(not theirs)"})
    return out


# ------------------------------------------------------------------ understaffing told by mail

# The request asks for the app's form by name: then a mail does not replace it.
FORM_ASKED = re.compile(r"understaffing report|report understaffing|„Unterbesetzung melden“|\"Unterbesetzung melden\"|"
                        r"Unterbesetzung an die Heimleitung melden", re.IGNORECASE)


def mail_uncovered(state: Any, app: Any, initial_app: Any, task: dict[str, Any]) -> list[dict[str, Any]] | None:
    """The open shifts claimed in the latest mail to the home manager that claims any (None: no such mail, or the
    request asks for the understaffing form by name). Each claim is mapped onto the open positions of that date and
    shift (the unit when the line names one); a role named on the line must be one that is really missing there (any
    role fits a shift that is only short of a person); no role named – the claim takes the missing role. A claimed
    shift that is not open stays in the claim as it is, so the honesty check sees it."""
    from opsdesk.workforce import views
    if FORM_ASKED.search(str(task.get("instruction") or "")):
        return None
    manager = {c.address.casefold() for c in app.contacts if c.contact_id == "contact-manager"}
    before = {m.mail_id for m in initial_app.mails} if initial_app is not None else set()
    reader = Reader(period_of(state), today=state.current_date)
    latest = None
    for m in app.mails:
        if m.folder != "sent" or m.mail_id in before or not {x.casefold() for x in [*m.to, *m.cc]} & manager:
            continue
        claims = reader.open_claims(f"{m.subject}\n{m.body}")
        if claims:
            latest = claims
    if latest is None:
        return None
    actual = views.open_positions(state)
    items: dict[tuple[str, str, str], str] = {}
    for d, t, roles, line in latest:
        units = [w for w, label in sorted(app.unit_names.items()) if label.casefold() in line.casefold()]
        here = [g for g in actual if g["date"].isoformat() == d and str(g["shift"]) == t and (not units or g["unit"] in units)]
        if not here:
            items[(d, units[0] if units else sorted(app.unit_names)[0], t)] = roles[0] if roles else "headcount"
            continue
        for g in here:
            quals = g["missing_qualifications"]
            wrong = bool(quals and roles and not any(r in quals for r in roles))  # names a role that is not missing
            items[(d, g["unit"], t)] = roles[0] if wrong else g["missing"]
    return [{"date": d, "unit": u, "shift": t, "missing": m} for (d, u, t), m in sorted(items.items())]
