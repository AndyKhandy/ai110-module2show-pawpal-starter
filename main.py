from pawpal_system import Task, Owner, Pet, Scheduler

andy = Owner("Andy Ta")
pet1 = Pet("Cassie", "Dog")
pet2 = Pet("Bob", "Cat")
andy.addPet(pet1)
andy.addPet(pet2)

# Tasks are added out of chronological order on purpose to exercise sort_by_time().
pet1Task1 = Task("Walk", 50, "high", pet1.name, "14:30")
pet1Task2 = Task("Bath", 25, "low", pet1.name, "08:00")
pet1Task3 = Task("Feed", 10, "medium", pet1.name, "12:00")
pet2Task1 = Task("Cut Hair", 40, "medium", pet2.name, "09:15")
pet2Task2 = Task("Vet Checkup", 30, "high", pet2.name, "16:00")

# Deliberately overlaps pet1Task1 ("Walk", 14:30-15:20) to verify same-pet conflict detection.
pet1Task4 = Task("Nail Trim", 15, "low", pet1.name, "14:40")
# Deliberately overlaps pet1Task1 ("Walk", 14:30-15:20) to verify cross-pet conflict detection.
pet2Task3 = Task("Ear Cleaning", 20, "medium", pet2.name, "14:35")

pet1Task2.markDone()
pet2Task1.markDone()

pet1.addTask(pet1Task1)
pet1.addTask(pet1Task2)
pet1.addTask(pet1Task3)
pet1.addTask(pet1Task4)
pet2.addTask(pet2Task1)
pet2.addTask(pet2Task2)
pet2.addTask(pet2Task3)

planner = Scheduler(andy.getAllTasks(), 900)
planner.buildPlan()
print("-----Today's Schedule-----")
print(planner.displayPlan())

print("\n-----Tasks Sorted by Time-----")
for task in planner.sort_by_time():
    print(f"  {task.time} - {task.name} ({task.petName})")

print("\n-----Incomplete Tasks-----")
for task in planner.filter_tasks(is_complete=False):
    print(f"  {task.name} ({task.petName}) - {task.time}")

print("\n-----Cassie's Tasks-----")
for task in planner.filter_tasks(pet_name="Cassie"):
    status = "done" if task.is_complete else "pending"
    print(f"  {task.name} - {task.time} [{status}]")

print("\n-----Schedule Conflicts-----")
conflicts = planner.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")
