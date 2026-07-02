from pawpal_system import Task, Pet, Scheduler


def make_task(name="Feed", duration=15, priority="medium", pet_name="Rex", time="08:00"):
    return Task(name=name, duration=duration, priority=priority, petName=pet_name, time=time)


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


def test_sort_by_time_orders_tasks_chronologically():
    early = make_task(name="Feed", time="9:05")
    late = make_task(name="Walk", time="10:00")
    scheduler = Scheduler(tasks=[late, early], available_minutes=120)

    scheduler.sort_by_time()

    assert [t.name for t in scheduler.tasks] == ["Feed", "Walk"]


def test_sort_by_time_returns_the_sorted_list():
    task = make_task()
    scheduler = Scheduler(tasks=[task], available_minutes=120)

    result = scheduler.sort_by_time()

    assert result is scheduler.tasks


def test_display_plan_shows_start_to_end_time_range():
    task = make_task(name="Walk", duration=20, time="09:40", pet_name="Rex")
    scheduler = Scheduler(tasks=[task], available_minutes=120)
    scheduler.buildPlan()

    plan_text = scheduler.displayPlan()

    assert "09:40 to 10:00 — Walk [priority: medium]" in plan_text


def test_filter_tasks_by_pet_name():
    rex_task = make_task(name="Feed", pet_name="Rex")
    fido_task = make_task(name="Walk", pet_name="Fido")
    scheduler = Scheduler(tasks=[rex_task, fido_task], available_minutes=120)

    result = scheduler.filter_tasks(pet_name="Rex")

    assert result == [rex_task]


def test_filter_tasks_by_completion_status():
    done_task = make_task(name="Feed")
    done_task.markDone()
    pending_task = make_task(name="Walk")
    scheduler = Scheduler(tasks=[done_task, pending_task], available_minutes=120)

    result = scheduler.filter_tasks(is_complete=False)

    assert result == [pending_task]


def test_filter_tasks_by_pet_name_and_completion_status():
    rex_done = make_task(name="Feed", pet_name="Rex")
    rex_done.markDone()
    rex_pending = make_task(name="Walk", pet_name="Rex")
    fido_pending = make_task(name="Groom", pet_name="Fido")
    scheduler = Scheduler(tasks=[rex_done, rex_pending, fido_pending], available_minutes=120)

    result = scheduler.filter_tasks(pet_name="Rex", is_complete=False)

    assert result == [rex_pending]


def test_filter_tasks_with_no_criteria_returns_all_tasks():
    task_a = make_task(name="Feed")
    task_b = make_task(name="Walk")
    scheduler = Scheduler(tasks=[task_a, task_b], available_minutes=120)

    result = scheduler.filter_tasks()

    assert result == [task_a, task_b]
