from datetime import date, timedelta

from pawpal_system import Task, Pet, Scheduler


def make_task(
    name="Feed",
    duration=15,
    priority="medium",
    pet_name="Rex",
    time="08:00",
    due_date=None,
    recurrence="none",
):
    kwargs = {
        "name": name,
        "duration": duration,
        "priority": priority,
        "petName": pet_name,
        "time": time,
        "recurrence": recurrence,
    }
    if due_date is not None:
        kwargs["due_date"] = due_date
    return Task(**kwargs)


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


def test_detect_conflicts_returns_empty_list_when_no_overlap():
    early = make_task(name="Feed", time="08:00", duration=15, pet_name="Rex")
    late = make_task(name="Walk", time="09:00", duration=30, pet_name="Rex")
    scheduler = Scheduler(tasks=[early, late], available_minutes=120)

    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_flags_overlap_for_same_pet():
    walk = make_task(name="Walk", time="14:30", duration=50, pet_name="Rex")
    nail_trim = make_task(name="Nail Trim", time="14:40", duration=15, pet_name="Rex")
    scheduler = Scheduler(tasks=[walk, nail_trim], available_minutes=120)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Walk" in conflicts[0] and "Nail Trim" in conflicts[0]


def test_detect_conflicts_flags_overlap_across_different_pets():
    walk = make_task(name="Walk", time="14:30", duration=50, pet_name="Rex")
    ear_cleaning = make_task(name="Ear Cleaning", time="14:35", duration=20, pet_name="Fido")
    scheduler = Scheduler(tasks=[walk, ear_cleaning], available_minutes=120)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Rex" in conflicts[0] and "Fido" in conflicts[0]


def test_detect_conflicts_treats_back_to_back_tasks_as_non_overlapping():
    feed = make_task(name="Feed", time="08:00", duration=15, pet_name="Rex")
    walk = make_task(name="Walk", time="08:15", duration=15, pet_name="Rex")
    scheduler = Scheduler(tasks=[feed, walk], available_minutes=120)

    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_ignores_same_time_tasks_on_different_days():
    today_task = make_task(name="Feed", time="08:00", duration=30, pet_name="Rex", due_date=date(2026, 7, 1))
    tomorrow_task = make_task(
        name="Feed", time="08:00", duration=30, pet_name="Rex", due_date=date(2026, 7, 1) + timedelta(days=1)
    )
    scheduler = Scheduler(tasks=[today_task, tomorrow_task], available_minutes=120)

    assert scheduler.detect_conflicts() == []


# --- Sorting edge cases -----------------------------------------------------

def test_sort_by_time_uses_numeric_comparison_not_lexicographic():
    # Lexicographic string sort would put "10:00" before "9:00" ('1' < '9').
    nine = make_task(name="Nine", time="9:00")
    ten = make_task(name="Ten", time="10:00")
    scheduler = Scheduler(tasks=[ten, nine], available_minutes=120)

    scheduler.sort_by_time()

    assert [t.name for t in scheduler.tasks] == ["Nine", "Ten"]


def test_sort_by_time_is_stable_for_tied_times():
    first = make_task(name="First", time="08:00")
    second = make_task(name="Second", time="08:00")
    third = make_task(name="Third", time="08:00")
    scheduler = Scheduler(tasks=[first, second, third], available_minutes=120)

    scheduler.sort_by_time()

    assert [t.name for t in scheduler.tasks] == ["First", "Second", "Third"]


def test_sort_by_time_on_empty_task_list_returns_empty_list():
    scheduler = Scheduler(tasks=[], available_minutes=120)

    result = scheduler.sort_by_time()

    assert result == []


# --- Recurrence edge cases ---------------------------------------------------

def test_mark_done_none_recurrence_returns_none():
    task = make_task(recurrence="none")

    assert task.markDone() is None


def test_mark_done_daily_recurrence_advances_due_date_by_one_day():
    task = make_task(recurrence="daily", due_date=date(2026, 7, 1))

    next_task = task.markDone()

    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 2)


def test_mark_done_weekly_recurrence_advances_due_date_by_one_week():
    task = make_task(recurrence="weekly", due_date=date(2026, 7, 1))

    next_task = task.markDone()

    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 8)


def test_mark_done_next_occurrence_is_not_marked_complete():
    task = make_task(recurrence="daily", due_date=date(2026, 7, 1))

    next_task = task.markDone()

    assert next_task.is_complete is False


def test_mark_done_next_occurrence_preserves_task_fields():
    task = make_task(
        name="Feed", duration=15, priority="high", pet_name="Rex", time="08:00",
        recurrence="daily", due_date=date(2026, 7, 1),
    )

    next_task = task.markDone()

    assert next_task.name == "Feed"
    assert next_task.duration == 15
    assert next_task.priority == "high"
    assert next_task.petName == "Rex"
    assert next_task.time == "08:00"
    assert next_task.recurrence == "daily"


def test_mark_done_called_twice_does_not_compound_next_due_date():
    # due_date advances relative to the original task's due_date each call,
    # not relative to the previously-generated occurrence.
    task = make_task(recurrence="daily", due_date=date(2026, 7, 1))

    first_next = task.markDone()
    second_next = task.markDone()

    assert first_next.due_date == date(2026, 7, 2)
    assert second_next.due_date == date(2026, 7, 2)


# --- Conflict detection edge cases ------------------------------------------

def test_detect_conflicts_chain_does_not_flag_non_overlapping_ends():
    # A overlaps B, B overlaps C, but A and C do not overlap each other.
    a = make_task(name="A", time="08:00", duration=30, pet_name="Rex")   # 08:00-08:30
    b = make_task(name="B", time="08:15", duration=30, pet_name="Rex")   # 08:15-08:45
    c = make_task(name="C", time="08:40", duration=30, pet_name="Rex")   # 08:40-09:10
    scheduler = Scheduler(tasks=[a, b, c], available_minutes=120)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 2
    assert any("'A'" in w and "'B'" in w for w in conflicts)
    assert any("'B'" in w and "'C'" in w for w in conflicts)
    assert not any("'A'" in w and "'C'" in w for w in conflicts)


def test_detect_conflicts_flags_full_containment():
    outer = make_task(name="Outer", time="08:00", duration=60, pet_name="Rex")  # 08:00-09:00
    inner = make_task(name="Inner", time="08:15", duration=10, pet_name="Rex")  # 08:15-08:25
    scheduler = Scheduler(tasks=[outer, inner], available_minutes=120)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Outer" in conflicts[0] and "Inner" in conflicts[0]


def test_detect_conflicts_flags_zero_duration_task_inside_another_tasks_window():
    walk = make_task(name="Walk", time="08:00", duration=30, pet_name="Rex")          # 08:00-08:30
    photo = make_task(name="Photo", time="08:15", duration=0, pet_name="Rex")         # instantaneous

    scheduler = Scheduler(tasks=[walk, photo], available_minutes=120)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Walk" in conflicts[0] and "Photo" in conflicts[0]


def test_detect_conflicts_zero_duration_task_does_not_conflict_at_its_own_start():
    photo = make_task(name="Photo", time="08:00", duration=0, pet_name="Rex")
    feed = make_task(name="Feed", time="08:00", duration=15, pet_name="Rex")
    scheduler = Scheduler(tasks=[photo, feed], available_minutes=120)

    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_finds_separate_overlapping_groups_on_different_days():
    day1_a = make_task(name="Day1-A", time="08:00", duration=30, pet_name="Rex", due_date=date(2026, 7, 1))
    day1_b = make_task(name="Day1-B", time="08:15", duration=30, pet_name="Rex", due_date=date(2026, 7, 1))
    day2_a = make_task(name="Day2-A", time="08:00", duration=15, pet_name="Rex", due_date=date(2026, 7, 2))
    day2_b = make_task(name="Day2-B", time="08:30", duration=15, pet_name="Rex", due_date=date(2026, 7, 2))
    scheduler = Scheduler(tasks=[day1_a, day1_b, day2_a, day2_b], available_minutes=120)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Day1-A" in conflicts[0] and "Day1-B" in conflicts[0]


# --- buildPlan edge cases -----------------------------------------------------

def test_build_plan_skips_oversized_task_but_still_includes_smaller_later_task():
    too_big = make_task(name="TooBig", duration=100)
    fits = make_task(name="Fits", duration=20)
    scheduler = Scheduler(tasks=[too_big, fits], available_minutes=50)

    plan = scheduler.buildPlan()

    assert [t.name for t in plan] == ["Fits"]


def test_build_plan_includes_task_that_exactly_fills_remaining_budget():
    task = make_task(name="ExactFit", duration=50)
    scheduler = Scheduler(tasks=[task], available_minutes=50)

    plan = scheduler.buildPlan()

    assert [t.name for t in plan] == ["ExactFit"]


# --- Weighted prioritization edge cases --------------------------------------

def test_compute_priority_score_ranks_high_above_low_priority_with_equal_urgency():
    today = date(2026, 7, 1)
    high = make_task(name="High", priority="high", due_date=today)
    low = make_task(name="Low", priority="low", due_date=today)
    scheduler = Scheduler(tasks=[high, low], available_minutes=120)

    assert scheduler.compute_priority_score(high, today) > scheduler.compute_priority_score(low, today)


def test_compute_priority_score_ranks_more_urgent_above_less_urgent_with_equal_priority():
    today = date(2026, 7, 1)
    urgent = make_task(name="Urgent", priority="medium", due_date=today)
    distant = make_task(name="Distant", priority="medium", due_date=today + timedelta(days=30))
    scheduler = Scheduler(tasks=[urgent, distant], available_minutes=120)

    assert scheduler.compute_priority_score(urgent, today) > scheduler.compute_priority_score(distant, today)


def test_build_plan_schedules_higher_scored_task_when_only_one_fits():
    today = date(2026, 7, 1)
    low = make_task(name="Low", priority="low", duration=50, due_date=today)
    high = make_task(name="High", priority="high", duration=50, due_date=today)
    scheduler = Scheduler(tasks=[low, high], available_minutes=50)

    plan = scheduler.buildPlan(today=today)

    assert [t.name for t in plan] == ["High"]
