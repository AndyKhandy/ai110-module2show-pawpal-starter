from dataclasses import dataclass, field
from datetime import date, timedelta

PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}
RECURRENCE_DELTA = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}

# Weighted prioritization: buildPlan() ranks tasks by priority tier plus due-date
# urgency instead of raw list order. Priority dominates (20-pt spread across 3
# tiers) but urgency (max 14-pt swing) can still bump a due-today medium task
# above a high-priority task that's weeks away.
PRIORITY_WEIGHT = 10
URGENCY_WEIGHT = 2
URGENCY_CAP_DAYS = 7


def _time_str_to_minutes(time_str: str) -> int:
    """Parse an "HH:MM" (or "H:MM") string into minutes since midnight."""
    h, m = (int(p) for p in time_str.split(":"))
    return h * 60 + m


def _minutes_to_time_str(minutes: int) -> str:
    """Format minutes since midnight back into a zero-padded "HH:MM" string."""
    h, m = divmod(minutes, 60)
    return f"{h:02d}:{m:02d}"


@dataclass
class Task:
    name: str
    duration: int       # minutes
    priority: str    # "low", "medium", "high"
    petName: str
    time: str            # "HH:MM" scheduled start time
    is_complete: bool = False
    recurrence: str = "none"    # "none", "daily", "weekly"
    due_date: date = field(default_factory=date.today)

    def markDone(self) -> "Task | None":
        """Mark this task complete; if recurring, return the next occurrence as a new Task."""
        self.is_complete = True
        delta = RECURRENCE_DELTA.get(self.recurrence)
        if delta is None:
            return None
        return Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            petName=self.petName,
            time=self.time,
            recurrence=self.recurrence,
            due_date=self.due_date + delta,
        )


@dataclass
class Pet:
    name: str
    species: str                            # "dog", "cat", "other"
    tasks: list[Task] = field(default_factory=list)

    def addTask(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def addPet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def getAllTasks(self) -> list[Task]:
        """Flatten and return the tasks of every pet this owner has."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Scheduler:
    tasks: list[Task]
    available_minutes: int                  # total time budget for the day
    daily_plan: list[Task] = field(default_factory=list)

    def compute_priority_score(self, task: Task, today: date = None) -> int:
        """Score a task by priority tier plus how soon it's due (higher = more important)."""
        today = today or date.today()
        days_until_due = (task.due_date - today).days
        urgency = max(0, URGENCY_CAP_DAYS - max(days_until_due, 0))
        return PRIORITY_ORDER.get(task.priority, 0) * PRIORITY_WEIGHT + urgency * URGENCY_WEIGHT

    def buildPlan(self, today: date = None) -> list[Task]:
        """Greedily fill the available time budget, ranking tasks by weighted priority score first."""
        time_used = 0
        self.daily_plan = []
        ranked_tasks = sorted(self.tasks, key=lambda t: self.compute_priority_score(t, today), reverse=True)
        for task in ranked_tasks:
            if time_used + task.duration <= self.available_minutes:
                self.daily_plan.append(task)
                time_used += task.duration
        return self.daily_plan

    def sort_by_time(self) -> list[Task]:
        """Sort tasks chronologically by their HH:MM start time."""
        self.tasks = sorted(self.tasks, key=lambda t: _time_str_to_minutes(t.time))
        return self.tasks

    def filter_tasks(self, pet_name: str = None, is_complete: bool = None) -> list[Task]:
        """Return tasks matching the given pet name and/or completion status."""
        results = self.tasks
        if pet_name is not None:
            results = [t for t in results if t.petName == pet_name]
        if is_complete is not None:
            results = [t for t in results if t.is_complete == is_complete]
        return results

    def detect_conflicts(self) -> list[str]:
        """Find same-day, overlapping-time tasks (same pet or different pets) and return warning messages."""
        warnings = []
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.due_date, _time_str_to_minutes(t.time)))
        for i, a in enumerate(sorted_tasks):
            a_end = _time_str_to_minutes(a.time) + a.duration
            for b in sorted_tasks[i + 1:]:
                if b.due_date != a.due_date:
                    break
                if _time_str_to_minutes(b.time) >= a_end:
                    break
                warnings.append(
                    f"Conflict: '{a.name}' ({a.petName}, {a.time}-{_minutes_to_time_str(a_end)}) "
                    f"overlaps with '{b.name}' ({b.petName}, {b.time})"
                )
        return warnings

    def displayPlan(self) -> str:
        """Render the built plan as a human-readable schedule using each task's own start time."""
        if not self.daily_plan:
            return "No plan built yet. Call buildPlan() first."
        lines = []
        currPet = ""
        for task in self.daily_plan:
            if currPet == "" or currPet != task.petName:
                currPet = task.petName
                lines.append(f"Tasks for {currPet}")

            end_time = _minutes_to_time_str(_time_str_to_minutes(task.time) + task.duration)
            lines.append(
                f"  {task.time} to {end_time} — {task.name} [priority: {task.priority}]"
            )
        return "\n".join(lines)
