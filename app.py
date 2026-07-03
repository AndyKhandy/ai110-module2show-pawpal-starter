import streamlit as st
from pawpal_system import Task,Owner,Pet,Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
owner = st.session_state.owner
owner.name = owner_name

st.markdown("### Pets")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.addPet(Pet(name=pet_name, species=species))
    st.success(f"Added {pet_name} the {species} 🐾")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if owner.pets:
    task_pet_name = st.selectbox("Pet", [p.name for p in owner.pets])
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        task_time = st.text_input("Start time (HH:MM)", value="08:00")
    with col5:
        recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == task_pet_name)
        pet.addTask(
            Task(
                name=task_title,
                duration=int(duration),
                priority=priority,
                petName=task_pet_name,
                time=task_time,
                recurrence=recurrence,
            )
        )
        st.success(f"Added task '{task_title}' for {task_pet_name} at {task_time}")
else:
    st.info("Add a pet before adding tasks.")

PRIORITY_BADGES = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}


def _end_time(t):
    h, m = (int(p) for p in t.time.split(":"))
    total = h * 60 + m + t.duration
    eh, em = divmod(total, 60)
    return f"{eh:02d}:{em:02d}"


def _task_row(t):
    return {
        "pet": t.petName,
        "title": t.name,
        "time": t.time,
        "duration_minutes": t.duration,
        "priority": PRIORITY_BADGES.get(t.priority, t.priority),
        "recurrence": t.recurrence,
        "due_date": t.due_date,
    }


all_tasks = owner.getAllTasks()
incomplete_tasks = [t for t in all_tasks if not t.is_complete]
completed_tasks = [t for t in all_tasks if t.is_complete]

if all_tasks:
    st.write("Current tasks:")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Total tasks", len(all_tasks))
    metric_col2.metric("Pending", len(incomplete_tasks))
    metric_col3.metric("Completed", len(completed_tasks))

    if incomplete_tasks:
        st.table([_task_row(t) for t in incomplete_tasks])
    else:
        st.success("No pending tasks — all caught up!")

    if completed_tasks:
        with st.expander(f"Completed tasks ({len(completed_tasks)})"):
            st.table([_task_row(t) for t in completed_tasks])

    st.markdown("### Filter & Sort Tasks")
    filt_col1, filt_col2, filt_col3 = st.columns(3)
    with filt_col1:
        filter_pet = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
    with filt_col2:
        filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])
    with filt_col3:
        sort_chrono = st.checkbox("Sort by start time", value=True)

    view_scheduler = Scheduler(tasks=list(all_tasks), available_minutes=0)
    if sort_chrono:
        view_scheduler.sort_by_time()

    pet_arg = None if filter_pet == "All" else filter_pet
    status_arg = None if filter_status == "All" else (filter_status == "Completed")
    filtered_tasks = view_scheduler.filter_tasks(pet_name=pet_arg, is_complete=status_arg)

    if filtered_tasks:
        st.table([_task_row(t) for t in filtered_tasks])
    else:
        st.warning("No tasks match the selected filters.")

    conflicts = view_scheduler.detect_conflicts()
    if conflicts:
        for warning_msg in conflicts:
            st.warning(warning_msg)
    else:
        st.success("No scheduling conflicts detected.")

    if incomplete_tasks:
        selected_idx = st.selectbox(
            "Mark a task complete",
            range(len(incomplete_tasks)),
            format_func=lambda i: f"{incomplete_tasks[i].petName} — {incomplete_tasks[i].name} ({incomplete_tasks[i].time})",
        )
        if st.button("Mark complete"):
            task_to_complete = incomplete_tasks[selected_idx]
            next_task = task_to_complete.markDone()
            if next_task is not None:
                pet = next(p for p in owner.pets if p.name == next_task.petName)
                pet.addTask(next_task)
                st.success(f"Marked done. Next occurrence scheduled for {next_task.due_date}.")
            else:
                st.success("Marked done.")
            st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
available_minutes = st.number_input("Available minutes today", min_value=1, max_value=1440, value=120)

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(tasks=all_tasks, available_minutes=int(available_minutes))
        plan = scheduler.buildPlan()

        if not plan:
            st.warning("No tasks fit in the available time.")
        else:
            minutes_used = sum(t.duration for t in plan)
            st.success(
                f"Schedule built — {len(plan)} task(s) scheduled, "
                f"{minutes_used} of {int(available_minutes)} minutes used."
            )
            st.table(
                [
                    {
                        "pet": t.petName,
                        "task": t.name,
                        "start": t.time,
                        "end": _end_time(t),
                        "priority": PRIORITY_BADGES.get(t.priority, t.priority),
                    }
                    for t in plan
                ]
            )

            skipped = [t for t in all_tasks if t not in plan]
            if skipped:
                with st.expander(f"Not scheduled ({len(skipped)}) — ran out of time"):
                    st.table([_task_row(t) for t in skipped])
