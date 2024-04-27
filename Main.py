from User import User
from Task import Task
from Database import Database

USERS_DB = "users.db"
# TASKS_DB = "tasks.db"


def main():  #
    db_users = Database(USERS_DB)
    db_users.create_tables()

    # db_users = Database(TASKS_DB)
    # db_users.create_tables()

    while True:
        print('========================================================')
        print('\tSTUDENT TO-DO-LIST APPLICATION')
        print('========================================================')
        print('\t1. Login')
        print('\t2. Create an Account')
        print('\t3. Exit')
        print('========================================================')
        try:
            choice = int(input('Enter choice [1-3]: '))
            print('========================================================')

            if choice == 1:
                user = login(db_users)
                if user:
                    main_menu(user, db_users)
                    break
            elif choice == 2:
                create_account(db_users)
            elif choice == 3:
                db_users.close()
                # db_users.close()
                print('========================================================')
                print('Thank you and come back again!')
                break
            else:
                print("Invalid choice [1-3] only!")
        except ValueError:
            print('========================================================')
            print("Invalid choice! Please enter a number [1-3] only.")


def login(db_users):
    try:
        username = input("Enter Registered Username: ")
        password = input("Enter Registered Password: ")
        users = db_users.load_users()
        for user in users:
            if user.username == username and user.password == password:
                print('========================================================')
                print("Login successful!")
                return user
        print('========================================================')
        print("Invalid username or password.")
        return None
    except Exception as e:
        print('An error occurred:', e)
        return None


def create_account(db_users):
    firstName = input("Enter your first name: ")
    lastName = input("Enter your last name: ")
    studentNum = input("Student Number: ")
    username = input("Desired Username: ")
    password = input("Desired Password: ")

    users = db_users.load_users()
    for user in users:
        if user.username == username:
            print('========================================================')
            print("Username already exists.")
            return

    new_user = User(firstName, lastName, studentNum, username, password)
    db_users.save_user(new_user)
    print('========================================================')
    print("Account created successfully!")


def main_menu(user, db_users):
    while True:
        print('========================================================')
        print(f"Hi {user.first_name + ' ' + user.last_name}, Welcome to TaskWise!")
        print('Your tasks today:')
        tasks = db_users.load_tasks(user.student_number)
        for i, task in enumerate(tasks, start=1):
            print(f"{task.task_id}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")
        print('========================================================')
        print('\t1. Create Task')
        print('\t2. Update Task')
        print('\t3. Delete Task')
        print('\t4. Search Task')
        print('\t5. Mark Task as Completed')
        print('\t6. Logout')
        print('========================================================')
        try:
            choice = int(input('Enter choice [1-6]: '))
            print('========================================================')
            if choice == 1:
                create_task(user, db_users)
            elif choice == 2:
                update_task(user, db_users)
            elif choice == 3:
                delete_task(user, db_users)
            elif choice == 4:
                search_task(user, db_users)
            elif choice == 5:
                mark_task_completed(user, db_users)
            elif choice == 6:
                print('Logging out...')
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print('========================================================')
            print("Invalid choice! Please enter a number.")


def create_task(user, db_users):
    task_name = input("Enter Task Name: ")
    task_desc = input("Enter Task Description: ")
    task_date = input("Enter Task Deadline (YYYY-MM-DD): ")
    task_time = input("Enter Task Time (00:00 AM/PM): ")
    task_sub = input("Enter Task Subject: ")
    task_cat = input("Enter Task Category: ")
    status = "Incomplete"
    new_task = Task(None, task_name, task_desc, task_date, task_time, task_sub, task_cat, status)
    db_users.save_task(new_task, user.student_number)
    print('========================================================')
    print('Task created successfully!')

def update_task(user, db_users):
    tasks = db_users.load_tasks(user.student_number)
    if not tasks:
        print("No tasks available to update.")
        return

    print("Select a task to update:")
    for i, task in enumerate(tasks, start=1):
        print(f"{task.task_id}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")

    try:
        task_id_to_update = int(input("Enter the task ID to update: "))
        selected_task = None
        for task in tasks:
            if task.task_id == task_id_to_update:
                selected_task = task
                break
        if selected_task:
            
            new_name = input(f"Enter new task name [{selected_task.task_name}]: ") or selected_task.task_name
            new_desc = input(f"Enter new task description [{selected_task.task_desc}]: ") or selected_task.task_desc
            new_date = input(f"Enter new task deadline (YYYY-MM-DD) [{selected_task.date}]: ") or selected_task.date
            new_time = input(f"Enter new task time (00:00 AM/PM) [{selected_task.time}]: ") or selected_task.time
            new_sub = input(f"Enter new task subject [{selected_task.task_sub}]: ") or selected_task.task_sub
            new_cat = input(f"Enter new task category [{selected_task.task_cat}]: ") or selected_task.task_cat

            selected_task.task_name = new_name
            selected_task.task_desc = new_desc
            selected_task.date = new_date
            selected_task.time = new_time
            selected_task.task_sub = new_sub
            selected_task.task_cat = new_cat

            db_users.update_task(selected_task, user.student_number)
            print("Task updated successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input! Please enter a number.")

def delete_task(user, db_users):
    tasks = db_users.load_tasks(user.student_number)
    if not tasks:
        print("No tasks available to delete.")
        return

    print("Select a task to delete:")
    for i, task in enumerate(tasks, start=1):
        print(f"{task.task_id}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")

    try:
        task_index = int(input("Enter the number of the task to delete: "))
        selected_task = None
        for task in tasks:
            if task.task_id == task_index:
                selected_task = task
                break
        if selected_task:

            confirmation = input(f"Are you sure you want to delete '{selected_task.task_name} - {selected_task.task_id}'? (yes/no): ")
            if confirmation == 'yes':
                db_users.delete_task(selected_task, user.student_number)
                print("Task deleted successfully!")
            else:
                print("Deletion canceled.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input! Please enter a number.")


def search_task(user, db_users):
    # Sanitize user input (optional but recommended)
    keyword = input("Enter a keyword to search: ").strip()

    # Call the search_tasks method from the database class
    tasks = db_users.search_tasks(user.student_number, keyword)
    
    if tasks:
        print("Search results:")
        for task in tasks:
            print(f"{task.task_id}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Subject: {task.task_sub} - Category: {task.task_cat} - Status: {task.status}")
    else:
        print("No tasks found matching the keyword.")


def mark_task_completed(user, db_users):
    tasks = db_users.load_tasks(user.student_number)
    incomplete_tasks = [task for task in tasks if task.status == "Incomplete"]
    
    if not incomplete_tasks:
        print("No incomplete tasks available.")
        return

    print("Select an incomplete task to mark as completed:")
    for i, task in enumerate(incomplete_tasks, start=1):
        print(f"{task.task_id}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")

    try:
        task_id = int(input("Enter the number of the task to mark as completed: "))
        selected_task = next((task for task in incomplete_tasks if task.task_id == task_id), None)
        if selected_task:
            db_users.update_task_status(task_id, "Completed", user.student_number)
            print("Task marked as completed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input! Please enter a number.")



# def mark_task_completed(user, db_users):
    tasks = db_users.load_tasks(user.student_number)
    if not tasks:
        print("No tasks found.")
        return

    print("Select the task you want to mark as completed:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")

    try:
        task_index = int(input("Select the task you want to mark as completed: ")) - 1
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            task.status = "Completed"
            db_users.save_task(task, user.student_number)
            print('========================================================')
            print("Task marked as completed!")
        else:
            print("Invalid task index.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    main()
