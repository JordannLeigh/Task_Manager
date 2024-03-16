import os
from datetime import datetime

# Create empty user.txt and tasks.txt files if they don't exist
if not os.path.exists("user.txt"):
    open("user.txt", "w").close()

if not os.path.exists("tasks.txt"):
    open("tasks.txt", "w").close()


# Function to register a new user
def reg_user(username, password):

    
    # Check if user already exists
    with open("user.txt", "r") as file:
        existing_users = [line.split(",")[0].strip() for line in file.readlines()]
        if username in existing_users:
            print("Error: Username already exists. Please try again with a different username.")
            return
    
    # Add new user to user.txt
    with open("user.txt", "a") as file:
        file.write(f"{username},{password}\n")
    print("User registration successful.")


# Function to authenticate user
def authenticate(username, password):
    # Check if entered credentials match any user in user.txt
    with open("user.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if username == stored_username and password == stored_password:
                return True
    print("Invalid username or password. Please try again.")
    return False


# Function to add a new task
def add_task():
    flag = False
    username = input("Enter username of the person the task is assigned to: ")
    with open("user.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if username == stored_username:
                flag =  True
            else:
                print("Username is not registered yet. User Must have to Register first to be able to assinged task")
    if flag:
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
    if not os.path.exists("tasks.txt"):
        print("No tasks found.")
        return
    
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()
        if not tasks:
            print("No tasks found.")
            return
        for i, task in enumerate(tasks, 1):
            print(f"Task {i}: {task}")


            
def view_mine(current_user):
    if not os.path.exists("tasks.txt"):
        print("No tasks assigned to you found.")
        return
    
    print("Current User:", current_user)  # Debug print
    
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()
        print("All Tasks:", tasks)  # Debug print
        
        user_tasks = [(i, task) for i, task in enumerate(tasks, 1) if task.split(",")[0].strip() == current_user]
        print("User Tasks:", user_tasks)  # Debug print
        
        if not user_tasks:
            print("No tasks assigned to you found.")
            return

        for i, (task_number, selected_task) in enumerate(user_tasks, 1):
            print(f"Task {i}: {selected_task}")

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

                task_details = selected_task.split(",")  # Define task_details here
                
                while True:
                    action = input("Choose action: mark as complete (c) or edit (e), or enter -1 to go back: ")
                    if action == "-1":
                        break
                    elif action.lower() == "c":
                        # Mark task as complete
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
    if not os.path.exists("tasks.txt"):
        print("No tasks found.")
        return

    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.strip().endswith("Yes"))
    overdue_tasks = sum(1 for task in tasks if not task.strip().endswith("Yes") and datetime.strptime(task.split(",")[3], "%Y-%m-%d") < datetime.today())
    if total_tasks != 0:
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
            if total_tasks == 0:
                file.write("No tasks found.\n")
            else:
                for username in open("user.txt"):
                    username = username.split(",")[0]
                    user_tasks = sum(1 for task in tasks if task.split(",")[0].strip() == username)
                    completed_tasks = sum(1 for task in tasks if task.split(",")[0].strip() == username and task.strip().endswith("Yes"))
                    incomplete_tasks = user_tasks - completed_tasks
                    overdue_tasks = sum(1 for task in tasks if task.split(",")[0].strip() == username and not task.strip().endswith("Yes") and datetime.strptime(task.split(",")[3].strip(), "%Y-%m-%d") < datetime.today())

                    print(f"User: {username}")
                    print(f"Total Tasks: {user_tasks}")
                    print(f"Completed Tasks: {completed_tasks}")
                    print(f"Incomplete Tasks: {incomplete_tasks}")
                    print(f"Overdue Tasks: {overdue_tasks}")

                    task_percentage = (user_tasks / total_tasks) * 100
                    completed_percentage = (completed_tasks / total_tasks) * 100
                    incomplete_percentage = (incomplete_tasks / total_tasks) * 100
                    overdue_percentage = (overdue_tasks / total_tasks) * 100

                    file.write(f"Username: {username}\n")
                    file.write(f"Total Tasks: {user_tasks}\n")
                    file.write(f"Percentage of Total Tasks: {task_percentage:.2f}%\n")
                    file.write(f"Percentage of Completed Tasks: {completed_percentage:.2f}%\n")
                    file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n")
                    file.write(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%\n")
                    file.write("\n")
    else:
        print("No Task is assigned yet to display")



# Function to display statistics
def display_statistics():
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    total_tasks = len(tasks)
    if total_tasks != 0:
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
    else:
        print("No task is assigned yet to Display")


# Main function to handle menu and user interaction
def main():
    while True:
        login=False
        current_user = None
        print("\nPlease select one of the following options:")
        print("1 - Register a new user")
        print("2 - Login")
        print("3 - Exit")

        option = input("Enter your choice: ")

        if option == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            reg_user(username=username, password=password)
        elif option == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authenticate(username=username, password=password):
                print("Login successful!")
                current_user=username
                login=True
                # Proceed with other functionalities after successful authentication
                break
            else:
                print("Login failed. Please try again.")
        elif option == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")
    if login:
        while True:
            print("\nPlease select one of the following options:")
            print("a - add task")
            print("va - view all tasks")
            print("vm - view my tasks")
            print("gr - generate reports")
            print("ds - display statistics")
            print("e - exit")

            option = input("Enter your choice: ").lower()

            if option == "a":
                add_task()
            elif option == "va":
                view_all()
            elif option == "vm":
                view_mine(current_user)
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
