#===== importing libraries ===========
# importing both date and datetime from the datetime module
# because i will use date to extract the current date
# and will use datetime initially to convert date issued to dd mmm yyyy format
from datetime import date
from datetime import datetime

# also using inspect module for output readability
import inspect


# ======= Defining Functions ==========

# making a function to return a dictionary of all usernames and corresponding passwords
# to be called when checking login details match same key/value
def list_dict(x, y):
    return dict(zip(x, y))

# using the new dictionary created by get_dict function to check key/value against input user/pass
def dict_check(username, password, user_dict):
    while True:
        if user_dict[username] != password:
            print("The username and password do not match.")
            input_username = input("Username: ")
            input_password = input("Password: ")
            return login_check(input_username, input_password, user_dict)
        elif user_dict[username] == password:
            print("Logged in successfully.")
            break

# moved the login check into its own function to improve modularity
def login_check(username, password, user_dict):
    while True:
        if username not in usernames and password not in passwords:
            print("Invalid credentials.")
            username = input("Username: ")
            password = input("Password: ")
            continue
        elif username not in usernames and password in passwords:
            print("Invalid username.")
            username = input("Username: ")
            continue
        elif username in usernames and password not in passwords:
            print("Invalid password.")
            password = input("Password: ")
            continue
        else:
            return dict_check(username, password, user_dict)

# checking against list of usernames to see if input username already exists
def reg_user(username, password):
    with open('user.txt', 'a') as users:
        while True:
            if username not in usernames:
                    users.write(f"\n{username}, {password}")
                    print("\nUser registered successfully.")
                    break
            elif username in usernames:
                    print(f"Error: that username already exists.")
                    return 


def add_task(user, title, description, dateIssued, dateDue, complete):
    with open("tasks.txt", "a") as task_create:
        task_create.write(f"\n{user}, {title}, {description}, {dateIssued}, {dateDue}, {complete}")
        print("\nTask added successfully.")

def view_all(file):
    with open("tasks.txt", "r") as file:
        print("\nALL TASKS:\n")
        for task in file.readlines():
            lines = task.strip().split(", ")
            user = lines[0]
            title = lines[1]
            description = lines[2]
            dateIssued = lines[3]
            dateDue = lines[4]
            complete = lines[5]
            print(f"\n{user}, {title}, {description}, {dateIssued}, {dateDue}, {complete}")

# using this function to contain all processes when selecting 'vm' from the menu
def view_mine(file, input_username):
    all_tasks = []
    my_tasks = []
    all_tasks_dict = {}
    users_counter = 0

    with open("tasks.txt", "r") as file1:
        for line in file1.readlines():
            lines = line.strip().split(", ")
            user = lines[0]
            all_tasks.append(lines)
    
    # using enumerate() to provide both indexes and lines
    # by doing this i can create two views via dictionary - all tasks (with a counter) and my tasks (with a new counter)
    # this is mainly for code readability and efficiency when the user chooses a specific task from their tasks to edit
    for counter, lines in enumerate(all_tasks):
        tasks_dict = {
        'user': lines[0],
        'title': lines[1],
        'description': lines[2],
        'dateIssued': lines[3],
        'dateDue': lines[4],
        'complete': lines[5]}
        all_tasks_dict[counter] = tasks_dict

        if lines[0] == input_username:
            my_tasks.append(tasks_dict)
            users_counter += 1
            print(f'''
                \nTask {users_counter}
                \nAssigned to: {lines[0]}
                \nTitle: {lines[1]}
                \nDescription: {lines[2]}
                \nDate Issued: {lines[3]}
                \nDue: {lines[4]}
                \nCompleted? {lines[5]}
                ''')

    # ive added the second section of the vm function here instead of making a separate function
    # this is because i still want to use the details of the my_task list
    check_id = int(input("Enter the number of the task you'd like to access (or enter -1 to exit): "))-1
    if 0 <= check_id < len(my_tasks):
        selected_task = my_tasks[check_id]
        selected_dict_key = list(all_tasks_dict.values()).index(selected_task)
        edit_task = all_tasks_dict[selected_dict_key]
        print(selected_dict_key)
        choice = input(f'''
        \nWould you like to:
        m - Mark the task as complete
        e - Edit the task
        \nChoice: ''').lower()

        # using the dictionary key to change value then rewriting the entire text file with the new data
        if choice == 'm':
            edit_task['complete'] = 'Yes'
            with open('tasks.txt', 'w') as write_file:
                for line_dict in all_tasks_dict.values():
                    output = f"{line_dict['user']}, {line_dict['title']}, {line_dict['description']}, {line_dict['dateIssued']}, {line_dict['dateDue']}, {line_dict['complete']}\n"
                    write_file.write(output)
                print(f"Task {check_id} has been marked as complete.")
        
        # similar process for 'e' as 'm' by using key to access value and changing the contents then rewriting text file
        # added some checks via if statements to prevent tasks which are already complete from being edited
        # and to check if the new assigned user exists in the username database
        elif choice == 'e':
            if edit_task['complete'] == 'Yes':
                print(f"Completed tasks cannot be edited.")
                return
            elif edit_task['complete'] == 'No':
                print(f'''Would you like to:\n
                u = change assigned user
                d = change due date''')
                edit_choice = input(f"\nChoice: ").lower()

                if edit_choice == 'u':
                    edit_username = input("Who would you like to reassign this task to?: ")
                    if edit_username in usernames:
                        edit_task['user'] = edit_username
                        with open('tasks.txt', 'w') as write_file:
                            for line_dict in all_tasks_dict.values():
                                output = f"{line_dict['user']}, {line_dict['title']}, {line_dict['description']}, {line_dict['dateIssued']}, {line_dict['dateDue']}, {line_dict['complete']}\n"
                                write_file.write(output)
                            print(f"Task {check_id} reassigned to {edit_username} successfully.")
                    elif edit_username not in usernames:
                        print("Username cannot be found.")
                        return
                
                elif edit_choice == 'd':
                    edit_date = input("Enter the new due date for this task (DD MMM YYYY): ")
                    edit_task['dateDue'] = edit_date
                    with open('tasks.txt', 'w') as write_file:
                        for line_dict in all_tasks_dict.values():
                            output = f"{line_dict['user']}, {line_dict['title']}, {line_dict['description']}, {line_dict['dateIssued']}, {line_dict['dateDue']}, {line_dict['complete']}\n"
                            write_file.write(output)
                        print(f"The due date for task {check_id} has been changed to {edit_date}.")
    
    elif check_id == -1:
        return

def get_report(file, user_dict):
    # making empty lists and appending all applicable lines to the relevant list given it meets the if/elif condition
    all_tasks = []
    all_users = []
    completed_tasks = []
    uncompleted_tasks = []
    overdue_tasks = []

    with open ('tasks.txt', 'r') as file:
        for lines in file.readlines():
            line = lines.strip().split(', ')

            all_tasks.append(line)

            if line[5] == 'Yes':
                completed_tasks.append(line)
            elif line[5] == 'No':
                uncompleted_tasks.append(line)
            
            # using date and datetime here to compare current date with due date of task
            # datetime was necessary to format the data input by user
            today = date.today()
            due_date = datetime.strptime(line[4].lstrip(),'%d %b %Y')
            
            # due date could then be transformed to date format so the condition check could be applied
            if datetime.date(due_date) > today:
                overdue_tasks.append(line)

    with open('task_overview.txt', 'w') as task_file:
        # found the method of inspect.cleandoc() from SO, source: https://stackoverflow.com/questions/2504411
        # this was purely to neaten up the multiline code which would be written out to the external file and printed out in this program
        task_overview = inspect.cleandoc(f'''\
            Total tasks generated: {len(all_tasks)}
            Total no. tasks completed: {len(completed_tasks)}
            Total no. tasks uncompleted: {len(uncompleted_tasks)}
            Total no. tasks uncompleted & overdue: {len(overdue_tasks)}
            Perecntage of incomplete tasks: %{float(len(uncompleted_tasks)/(len(all_tasks)))}
            Percentage of overdue tasks: %{float(len(overdue_tasks)/len(all_tasks))}
            ''')
        task_file.write(task_overview)

    with open('user_overview.txt', 'w') as user_file:
        user_write = inspect.cleandoc(f'''\
            Total users registered: {len(usernames)}
            Total tasks generated: {len(all_tasks)}
            ''')
        user_file.write(user_write)


    tasks_dict = {
    'user': lines[0],
    'title': lines[1],
    'description': lines[2],
    'dateIssued': lines[3],
    'dateDue': lines[4],
    'complete': lines[5]}

    # looping through each user in the user dictionary first in order to produce collective user-friendly output
    # similar process as above except this loops through the users after all lines in all_tasks have been iterated through
    for key in user_dict:
        key_tasks = []
        key_completed = []
        key_uncompleted = []
        key_overdue = []
        for lines in all_tasks:
            if key == lines[0]:
                key_tasks.append(lines)
                if lines[5] == 'Yes':
                    key_completed.append(lines)
                elif lines[5] == 'No':
                    key_uncompleted.append(lines)
                today = date.today()
                due_date = datetime.strptime(line[4].lstrip(),'%d %b %Y')
                if datetime.date(due_date) > today:
                    key_overdue.append(lines)
        
        # i noticed here when using inspect.cleandoc() that the indentations were not removed in the user_overview file
        # this is unlike the task_overview file which has utilised the inspect.cleandoc() method with no issues
        # i couldn't find an alternative to this whilst keeping my code uniform so i have left it as is
        # the output in both files are still user friendly so it shouldn't be too much of an issue
        with open('user_overview.txt', 'a') as user_file:
            key_write = inspect.cleandoc(f'''
                \nFor user {key}:
                Total tasks assigned: {len(key_tasks)}
                Percentage of all tasks assigned: %{float(len(key_tasks)/len(all_tasks))}
                Percentage of complete tasks: %{float(len(key_completed)/len(completed_tasks))}
                Percentage of incomplete tasks: %{float(len(key_uncompleted)/len(uncompleted_tasks))}
                Percentage of incomplete & overdue tasks: %{float(len(key_overdue)/len(overdue_tasks))}
                ''')
            user_file.write(key_write)


#==== Login Section ====
with open('user.txt', 'r') as login:

    usernames = []
    passwords = []

    for line in login.readlines():
        strip_line = line.strip().split(', ')
        usernames.append(strip_line[0])
        passwords.append(strip_line[1])
# establishing dictionary to store all users and passwords in key/value format
# for use when calling functions after inputting login details
user_dict = list_dict(usernames, passwords)

input_username = input("Username: ")
input_password = input("Password: ")

login_check(input_username, input_password, user_dict)


# merged the non-admin and admin menu pages i had made for part 2 of T21
# this meant including the 'display statistics' item in the general menu
# but only making it accessible to admin if selected
while True:

# ==== menu page ============================================================================================

    print('''\nSelect one of the following options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task''')

    if input_username == 'admin':
        print('''\
    gr - generate reports
    ds - display statistics
    e - exit''')
        menu = input("\nChoice: ").lower()

    elif input_username != 'admin':
        print('''\
    e - exit''')
        menu = input("\nChoice: ").lower()


# ==== REGISTERING NEW USER ======
    if menu == 'r':
        if input_username != 'admin':
            print("Insufficient privileges.")
        elif input_username == 'admin':
            with open('user.txt', 'a') as users:
                while True:
                    new_user = input("\nPlease enter the new username: ")
                    new_password = input("Please enter the new password: ")
                    confirm_password = input("Confirm password: ")
                    if confirm_password != new_password:
                        print("\nThe passwords do not match.")
                        continue
                    elif new_user == "" or new_password == "" or confirm_password == "":
                        print("\nEmpty answers are invalid.")
                        continue
                    else:
                        reg_user(new_user, new_password)
                        break


# ======= ASSIGNING NEW TASK =======
    elif menu == 'a':
        user_choice = input("\nWhich user would you like to assign a task to?: ")
        while True:
            if user_choice in usernames:
                title_choice = input("Enter a title for this task: ")
                desc_choice = input("Enter task description: ")
                due_choice = input("Enter the due date for this task (DD MMM YYYY): ")

                today = date.today()
                date_issued = today.strftime("%d %b %Y")
                completed = "No"
                
                add_task(user_choice, title_choice, desc_choice, date_issued, due_choice, completed)
                break

            else:
                print("\nUsername not found. Please try entering again.")
                user_choice = input("\nWhich user would you like to assign a task to?: ")
                continue


# ======= VIEWING ALL TASKS  ============
    elif menu == 'va':
        view_all('tasks.txt')


# ======== VIEWING MY TASKS ===============
    elif menu == 'vm':
        view_mine('tasks.txt', input_username)


# ========== GENERATING REPORTS (ADMIN) ================
    elif menu == 'gr':
        # decided to put this code in a function for modularity and simply call it here
        if input_username == 'admin':
            get_report('tasks.txt', user_dict)
        elif input_username != 'admin':
            print("Insufficient privileges.")





# ========== DISPLAYING STATISTICS (ADMIN) =================
    elif menu == 'ds':
        if input_username != 'admin':
            print("Insufficient privileges.")
        elif input_username == 'admin':
            # removed old code here for displaying statistics and replaced with get_report() data
            print("\nSTATISITCS\n")
            get_report('tasks.txt', user_dict)
            with open('task_overview.txt', 'r') as file1:
                for line in file1.readlines():
                    print(line)
            with open('user_overview.txt', 'r') as file2:
                # didnt need line 3 of user_overview as that same data has already been printed from task_oveview
                lines = file2.readlines()
                print(f"\n{lines[0]}")
                for i in range(2, len(lines)):
                    print(lines[i])


# ===== EXITING ======
    elif menu == 'e':
        print('Goodbye!!!')
        exit()


# ===== ERROR MESSAGE ======
    else:
        print("You have made a wrong choice, Please Try again")
