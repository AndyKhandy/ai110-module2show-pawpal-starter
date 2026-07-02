from pawpal_system import Task, Owner, Pet, Scheduler

andy = Owner("Andy Ta")
pet1 = Pet("Cassie", "Dog")
pet2 = Pet("Bob", "Cat")
andy.addPet(pet1)
andy.addPet(pet2)

pet1Task1 = Task("Walk", 50, "high", pet1.name)
pet1Task2 = Task("Bath", 25, "low", pet1.name)
pet2Task1 = Task("Cut Hair", 40, "medium", pet2.name)

pet1.addTask(pet1Task1)
pet1.addTask(pet1Task2)
pet2.addTask(pet2Task1)

planner = Scheduler(andy.getAllTasks(), 900)
planner.buildPlan()
print("-----Today's Schedule-----")
print(planner.displayPlan())