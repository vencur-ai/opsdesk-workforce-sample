"""OpsDesk Workforce taskset for HUD: one run per task folder in data/tasks."""

from env import env, workspace

TASK_IDS = [
    "ow-e47b95f24436",
    "ow-658ad870c5a6",
    "ow-0dcf43a361e2",
    "ow-52c93274b5a8",
    "ow-087ab90a8670"
]

tasks = [workspace(task_id=t) for t in TASK_IDS]

__all__ = ["env", "tasks"]
