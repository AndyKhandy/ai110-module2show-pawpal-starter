from pawpal_system import Task, Pet


def make_task(name="Feed", duration=15, priority="medium", pet_name="Rex"):
    return Task(name=name, duration=duration, priority=priority, petName=pet_name)


def test_mark_done_sets_is_complete_true():
    task = make_task()
    assert task.is_complete is False

    task.markDone()

    assert task.is_complete is True


def test_mark_done_is_idempotent():
    task = make_task()

    task.markDone()
    task.markDone()

    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rex", species="dog")
    assert len(pet.tasks) == 0

    pet.addTask(make_task(pet_name="Rex"))

    assert len(pet.tasks) == 1


def test_add_task_increases_pet_task_count_for_multiple_tasks():
    pet = Pet(name="Rex", species="dog")

    pet.addTask(make_task(name="Feed", pet_name="Rex"))
    pet.addTask(make_task(name="Walk", pet_name="Rex"))
    pet.addTask(make_task(name="Groom", pet_name="Rex"))

    assert len(pet.tasks) == 3


def test_add_task_appends_the_same_task_instance():
    pet = Pet(name="Rex", species="dog")
    task = make_task(pet_name="Rex")

    pet.addTask(task)

    assert pet.tasks[0] is task
