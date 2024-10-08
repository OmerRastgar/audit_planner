def distribute_tasks(tasks, daily_work_hours=8):
    daily_limit = daily_work_hours * 60  # Convert hours to minutes
    rest_time = 30  # in minutes, every 2 hours of work
    break_time = 60  # in minutes, after 4 hours of work
    work_block = 2 * 60  # in minutes, every 2 hours before rest
    max_continuous_work = 4 * 60  # in minutes, maximum work before mandatory break

    # Convert tasks to minutes and sort in descending order
    tasks_in_minutes = [task * 60 for task in tasks]
    tasks_in_minutes.sort(reverse=True)

    schedule = {}
    current_day = 1
    available_time = daily_limit
    total_work_time = 0
    continuous_work_time = 0

    for task in tasks_in_minutes:
        while task > 0:
            if available_time <= 0:
                # Move to the next day
                current_day += 1
                available_time = daily_limit
                total_work_time = 0
                continuous_work_time = 0

            # Check how much time is left in the day
            remaining_time = available_time
            
            # Check how much time we can allocate to this task
            time_to_allocate = min(task, remaining_time)
            
            # Check if we can fit a break or rest time
            if continuous_work_time + time_to_allocate > max_continuous_work:
                time_to_allocate = max_continuous_work - continuous_work_time
            
            # If time exceeds the daily limit, allocate what's left and go to the next day
            if total_work_time + time_to_allocate > daily_limit:
                time_to_allocate = remaining_time
            
            # Update task and schedule
            if time_to_allocate > 0:
                if current_day not in schedule:
                    schedule[current_day] = []

                schedule[current_day].append(time_to_allocate / 60)  # Store time in hours
                task -= time_to_allocate
                available_time -= time_to_allocate
                total_work_time += time_to_allocate
                continuous_work_time += time_to_allocate
            
            # Add breaks if necessary
            if continuous_work_time >= work_block:
                available_time -= break_time
                continuous_work_time = 0  # Reset continuous work time
                total_work_time += break_time  # Count break time towards total work time
            
            # Add rest time if necessary
            if continuous_work_time >= 2 * 60:  # 2 hours of work
                available_time -= rest_time
                continuous_work_time = 0  # Reset continuous work time
                total_work_time += rest_time  # Count rest time towards total work time

    return schedule

# Example usage:
tasks = [2, 3, 0.5, 4, 3, 2, 1]  # tasks in hours
schedule = distribute_tasks(tasks)
for day, task_hours in schedule.items():
    print(f"Day {day}: {task_hours}")