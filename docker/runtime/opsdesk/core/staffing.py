"""3.2: the home's minimum staffing per shift (a house standard). In `core` so the sample runtime has it too
(the documents state it; the generator in `generator.world` uses it)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StaffingStandard:
    """3.2: the home's minimum staffing per shift (a house standard), per unit of `residents_basis` residents.

    The default is what a practising head of nursing gave for her home (a unit of 25 residents: early 4, late 3,
    night 1, care staff only). A specialist (dementia) unit has `specialist_extra_day` more by day (its team leader).
    Nurses: by day the house minimum on every unit; at night `night_nurses_in_home` registered nurse(s) in the home –
    rostered on the first unit – the others' night cover may be a care assistant. Germany: at night at least one
    person per 45 residents (the floor some state regulations set) – with units of up to 45 residents the default
    already meets it. Before 3.2 every shift needed the same (3, a dementia unit 4)."""

    early: int = 4
    late: int = 3
    night: int = 1
    residents_basis: int = 25
    specialist_extra_day: int = 1
    night_nurses_in_home: int = 1
    residents_range: tuple[int, int] = (22, 28)
    specialist_residents_range: tuple[int, int] = (16, 22)
    # staff and nurse numbers follow the (smaller) demand; False keeps the 3.1 sizes
    staff_follow_demand: bool = True


PDL_STANDARD = StaffingStandard()
DE_NIGHT_RESIDENTS_PER_PERSON = 45
