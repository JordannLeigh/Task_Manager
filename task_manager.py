import os
from datetime import datetime

# Function to register a new user
def reg_user():
    username = input("Enter new username: ")
    with open("user.txt", "a+") as file:
        existing_users = [line.split(",")[0].strip() for line in file.readlines()]
        if username in existing_users:
            print("Error: Username already exists. Please try again with a different username.")
            return
        file.write(f"{username},\n")
    print("User registration successful.")

# Function to add a new task
def add_task():
    username = input("Enter username of the person the task is assigned to: ")
    title = input("Enter the title of the task: ")
    description = input("Enter the task description: ")
    while True:
        due_date_str = input("Enter the due date (yyyy-mm-dd) of the task: ")
        try:
            datetime.strptime(due_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Invalid date format. Please enter the date in yyyy-mm-dd format.")
    
    completed = "No"
    
    with open("tasks.txt", "a") as file:
        file.write(f"{username},{title},{description},{due_date_str},{completed}\n")
    print("Task added successfully.")

# Function to view all tasks
def view_all():
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()
        if not tasks:
            print("No tasks found.")
            return
        for i, task in enumerate(tasks, 1):
            print(f"Task {i}: {task}")

# Function to view tasks assigned to the current user
def view_mine():
    current_user = input("Enter your username: ")
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()
        user_tasks = [(i, task) for i, task in enumerate(tasks, 1) if task.split(",")[0] == current_user]
        if not user_tasks:
            print("No tasks assigned to you found.")
            return

        for i, task in user_tasks:
            print(f"Task {i}: {task}")

        while True:
            task_choice = input("Enter the number of the task you want to select, or -1 to return to the main menu: ")
            if task_choice == "-1":
                return
            elif not task_choice.isdigit() or int(task_choice) < 1 or int(task_choice) > len(user_tasks):
                print("Invalid input. Please enter a valid task number.")
                continue
            else:
                task_index = int(task_choice) - 1
                task_number, selected_task = user_tasks[task_index]
                print(selected_task)

                while True:
                    action = input("Choose action: mark as complete (c) or edit (e), or enter -1 to go back: ")
                    if action == "-1":
                        break
                    elif action.lower() == "c":
                        # Mark task as complete
                        task_details = selected_task.split(",")
                        task_details[4] = "Yes\n"
                        tasks[task_number - 1] = ",".join(task_details)
                        with open("tasks.txt", "w") as file:
                            file.writelines(tasks)
                        print("Task marked as complete.")
                        break
                    elif action.lower() == "e":
                        # Edit task
                        if task_details[4].strip() == "Yes":
                            print("Error: Completed tasks cannot be edited.")
                            break
                        else:
                            new_username = input("Enter new username or leave empty to keep current: ")
                            new_due_date = input("Enter new due date (yyyy-mm-dd) or leave empty to keep current: ")
                            if new_username:
                                task_details[0] = new_username
                            if new_due_date:
                                task_details[3] = new_due_date
                            tasks[task_number - 1] = ",".join(task_details)
                            with open("tasks.txt", "w") as file:
                                file.writelines(tasks)
                            print("Task edited successfully.")
                            break
                    else:
                        print("Invalid input. Please choose 'c' to mark as complete or 'e' to edit.")
                        continue

# Function to generate reports
def generate_reports():
    tasks = []
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.strip().endswith("Yes"))
    overdue_tasks = sum(1 for task in tasks if not task.strip().endswith("Yes") and datetime.strptime(task.split(",")[3], "%Y-%m-%d") < datetime.today())

    total_users = sum(1 for line in open("user.txt"))
    with open("task_overview.txt", "w") as file:
        file.write(f"Total Tasks: {total_tasks}\n")
        file.write(f"Completed Tasks: {completed_tasks}\n")
        file.write(f"Uncompleted Tasks: {total_tasks - completed_tasks}\n")
        file.write(f"Overdue Tasks: {overdue_tasks}\n")
        file.write(f"Percentage of Incomplete Tasks: {(total_tasks - completed_tasks) / total_tasks * 100:.2f}%\n")
        file.write(f"Percentage of Overdue Tasks: {overdue_tasks / total_tasks * 100:.2f}%\n")

    with open("user_overview.txt", "w") as file:
        file.write(f"Total Users: {total_users}\n")
        file.write(f"Total Tasks: {total_tasks}\n")
        for username in open("user.txt"):
            username = username.strip()
            user_tasks = sum(1 for task in tasks if task.split(",")[0] == username)
            if total_tasks == 0:
                task_percentage = 0
                completed_percentage = 0
                incomplete_percentage = 0
                overdue_percentage = 0
            else:
                task_percentage = user_tasks / total_tasks * 100
                completed_percentage = sum(1 for task in tasks if task.split(",")[0] == username and task.strip().endswith("Yes")) / user_tasks * 100
                incomplete_percentage = (user_tasks - sum(1 for task in tasks if task.split(",")[0] == username and task.strip().endswith("Yes"))) / user_tasks * 100
                overdue_percentage = sum(1 for task in tasks if task.split(",")[0] == username and not task.strip().endswith("Yes") and datetime.strptime(task.split(",")[3], "%Y-%m-%d") < datetime.today()) / user_tasks * 100
            file.write(f"Username: {username}\n")
            file.write(f"Total Tasks: {user_tasks}\n")
            file.write(f"Percentage of Total Tasks: {task_percentage:.2f}%\n")
            file.write(f"Percentage of Completed Tasks: {completed_percentage:.2f}%\n")
            file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n")
            file.write(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%\n")
            file.write("\n")

# Function to display statistics
def display_statistics():
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()

    with open("task_overview.txt", "r") as file:
        task_overview = file.read()
        print("Task Overview:")
        print(task_overview)

    with open("user_overview.txt", "r") as file:
        user_overview = file.read()
        print("User Overview:")
        print(user_overview)

# Main function to handle menu and user interaction
def main():
    while True:
        print("Please select one of the following options:")
        print("I - register user")
        print("a - add task")
        print("va - view all tasks")
        print("vm - view my tasks")
        print("gr - generate reports")
        print("ds - display statistics")
        print("e - exit")

        option = input("Enter your choice: ").lower()

        if option == "i":
            reg_user()
        elif option == "a":
            add_task()
        elif option == "va":
            view_all()
        elif option == "vm":
            view_mine()
        elif option == "gr":
            generate_reports()
        elif option == "ds":
            display_statistics()
        elif option == "e":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
