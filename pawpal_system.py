from dataclasses import dataclass, field

PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}


@dataclass
class Task:
    name: str
    duration: int       # minutes
    priority: str    # "low", "medium", "high"
    petName: str     
    is_complete: bool = False

    def markDone(self) -> None:
        """Mark this task as complete."""
        self.is_complete = True


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

    def buildPlan(self) -> list[Task]:
        """Greedily fill the available time budget, taking tasks in list order."""
        time_used = 0
        self.daily_plan = []
        for task in self.tasks:
            if time_used + task.duration <= self.available_minutes:
                self.daily_plan.append(task)
                time_used += task.duration
        return self.daily_plan

    def displayPlan(self) -> str:
        """Render the built plan as a human-readable schedule starting at 08:00."""
        if not self.daily_plan:
            return "No plan built yet. Call buildPlan() first."
        lines = []
        current_minute = 8 * 60             # schedule starts at 08:00
        currPet = ""
        for task in self.daily_plan:
            if currPet == "" or currPet != task.petName:
                currPet = task.petName
                lines.append(f"Tasks for {currPet}")
            
            h, m = divmod(current_minute, 60)
            lines.append(
                f"  {h:02d}:{m:02d} — {task.name} ({task.duration} min) [priority: {task.priority}]"
            )
            current_minute += task.duration
        return "\n".join(lines)
