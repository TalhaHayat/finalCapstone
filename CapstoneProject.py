
#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def reg_user():

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        new_username = input("New Username: ").lower()

        # - Detects Similar Usernames and Prompts Input.
        while new_username in username_password.keys():
            print("This username has already been registered.\n")
            new_username = input("Please register with a different username: ")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")

def add_user ():

    # elif menu == 'a':

        '''Allow a user to add a new task to task.txt file

            Prompt a user for the following:
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and
             - the due date of the task.'''

        task_username = input("Name of person assigned to task: ").lower()
        if task_username not in username_password.keys():
            print("User does not exist. Please register the user first.")
            return
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified.")

        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

def view_all ():

    # elif menu == 'va':
    '''Reads the task from task.txt file and prints to the console in the
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling)
    '''

    for ind, t in enumerate(task_list):
        disp_str = f"Task {ind + 1}: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t\t {t['username'].capitalize()}\n"
        disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Completed: \t {t['completed']}\n"
        disp_str += f"Task Description: \t {t['description']}\n"
        print(disp_str)

def view_mine ():

    # elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''

        for ind, t in enumerate(task_list):
            if t['username'] == curr_user:
                disp_str = f"Task {ind + 1}: \t\t\t {t['title']}\n"
                disp_str += f"Assigned to: \t\t {t['username'].capitalize()}\n"
                disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t\t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Completed: \t {t['completed']}\n"
                disp_str += f"Task Description: \t {t['description']}\n"
                print(disp_str)

        # This allows the user to select a task and mark it as complete:

        while True:
            try:
                task_num = int(input("Please enter the task number to mark as complete "
                                     "(or -1 to go back, or \"0\" to edit): "))
                if task_num == -1:
                    break
                elif 1 <= task_num <= len(task_list):
                    task_list[task_num - 1]['completed'] = True
                    break
                elif task_num == 0:
                    edit_task_num = int(input("Enter the task number you wish to edit: ")) - 1

                    try:
                        if task_list[edit_task_num]['completed'] == True:
                            print("\nThis task has already been marked as completed, hence it cannot be edited.")
                            break

                    except IndexError:
                        print("This task cannot be found. Please try again.")
                        continue

                    except ValueError:
                        print("Please enter a numerical value.")
                        continue

                    if 0 <= edit_task_num < len(task_list):

                        #  This will allow the user to edit the username:
                        task_list[edit_task_num]['username'] = input("Please enter a new username: ")

                        #  This will allow the user to edit the date via defensive programming:

                        while True:
                            try:
                                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                                task_list[edit_task_num]['due_date'] = due_date_time
                                break
                            except ValueError:
                                print("Invalid datetime format. Please use the format specified and try again.")

                    else:
                        print("Invalid task number for editing.")
                    break

                else:
                    print("Invalid task number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        # This will update the file into the text file "tasks.txt".
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))

def display_report():

    # This function will display an expanded set of statistics if requested.
    # This code is then reformulated to generate reports in the subsequent function.

    counter = 0
    counter_complete = 0
    counter_uncomplete = 0
    list_of_username = []

    current_date = datetime.today().strftime(DATETIME_STRING_FORMAT)

    overdue_task_incomplete = 0  # This includes overdue task which are ALSO marked as incomplete.
    overdue_task = 0  # This is the total number of overdue tasks, both complete and incomplete.

    task_count_per_user = {}  # This is designed to get number of task per username.

    # This will get the total number of task entries and unique registrations.

    for task in task_list:
        # print(task['username']) # - This is used as a diagnostic tool. Can be utilised if debugging is required.
        counter += 1

        list_of_username.append(task['username'])

    print("\n")
    unique_usernames = set(list_of_username)
    print(f"There are a total of {counter} task entries, divided between {len(unique_usernames)} unique users.\n")

    # This will provide the total number of task per user.

    for task in task_list:

        if task['username'] in task_count_per_user:
            task_count_per_user[task['username']] += 1
        else:
            task_count_per_user[task['username']] = 1

    for username, task_count in task_count_per_user.items():
        print(f"{username.capitalize()} has registered a grand total of {task_count} tasks.")
        print(f"This represents {(task_count/len(list_of_username))*100:.2f}% of the workload.\n")
    print("")  # Provides a line break outside the For Loop.

    # The following For Loop is designed to get number of completed task per username.

    task_completed_per_user = {}

    for task in task_list:
        if task['completed'] == True:
            if task['username'] in task_completed_per_user:
                task_completed_per_user[task['username']] += 1
            else:
                task_completed_per_user[task['username']] = 1

    for username, task_count in task_completed_per_user.items():
        print(f"{username.capitalize()} has registered a grand total of {task_count} completed tasks.")
    print("") # Provides a line break outside the For Loop.

    # The next Loop statement will provide both the completion and non-completion percentage per user.
    # This code will use a new empty dictionary to achieve this - Which took me a long time to figure out.

    task_completion_percentage_per_user = {}

    for username in task_count_per_user.keys():
        total_tasks = task_count_per_user[username]
        completed_tasks = task_completed_per_user.get(username, 0)  # Defensive Programming.
        uncompleted_tasks = total_tasks - completed_tasks

        # Percentage Calculations.
        completed_percentage = (completed_tasks / total_tasks) * 100 if total_tasks else 0
        uncompleted_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks else 0

        # Storing Data into Dictionary.
        task_completion_percentage_per_user[username] = {
            'completed_percentage': completed_percentage,
            'uncompleted_percentage': uncompleted_percentage
        }

    for username, percentages in task_completion_percentage_per_user.items():
        print(f"{username.capitalize()}:")
        print(f"Completed Tasks: {percentages['completed_percentage']:.2f}%")
        print(f"Uncompleted Tasks: {percentages['uncompleted_percentage']:.2f}%")
        print("")  # Provides a line break for readability.

    # This will try to calculate the number of overdue-uncompleted tasks.

    task_overdue_incomplete = {}

    for task in task_list:
        if task['completed'] == False and task['due_date'].strftime(DATETIME_STRING_FORMAT) < current_date:
            if task['username'] in task_overdue_incomplete:
                task_overdue_incomplete[task['username']] += 1
            else:
                task_overdue_incomplete[task['username']] = 1

    for username, task_count in task_overdue_incomplete.items():
        print(f"{username.capitalize()} has a total of {task_count} tasks which are both incomplete and overdue.")
    print("")  # Provides a line break outside the For Loop.

    # The following will calculate the percentage of incomplete and overdue tasks.

    task_incompletion_percentage_per_user = {}

    for username in task_count_per_user.keys():
        total_tasks = task_count_per_user[username]
        incomplete_tasks = task_overdue_incomplete.get(username, 0)  # Defensive Programming.

        # Percentage Calculations.
        uncompleted_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks else 0

        # Storing Data into Dictionary.
        task_incompletion_percentage_per_user[username] = uncompleted_percentage

    for username, task_percentage in task_incompletion_percentage_per_user.items():
        print(f"User: {username.capitalize()}\nIncomplete & Overdue Tasks in Percentage: {task_percentage:.2f}%\n")
    print("")  # Provides a line break outside the For Loop.

    # This section will follow the task_overview criteria.

    for task in task_list:
        if task['completed'] == True:
            counter_complete += 1
        else:
            counter_uncomplete += 1

        if task['due_date'].strftime(DATETIME_STRING_FORMAT) < current_date and task['completed'] == False:
            overdue_task_incomplete += 1
        else:
            pass  # Skips to below if-else statement without breaking code

        if task['due_date'].strftime(DATETIME_STRING_FORMAT) < current_date:
            overdue_task += 1
        else:
            continue

    total_task = counter_complete + counter_uncomplete
    print(f"The Total Numbers of Task Present: {total_task}")
    print(f"Number of Completed Tasks: {counter_complete}\nNumber of Uncomplete Tasks: {counter_uncomplete}\n")
    print(f"The total number of overdue tasks which are marked as incomplete: {overdue_task_incomplete}")
    print(f"The total percentage of incompleted task: {(overdue_task_incomplete/total_task)*100 if total_task else 0:.2f}%.")
    print(f"The total percentage of overdue tasks is: {(overdue_task/total_task)*100 if total_task else 0:.2f}%.")

def generate_report():

    '''
    This will generate reports.
    It will follow the structure of the 'display_report()' function.
    It will then output to "task_overview.txt" and "user_overview.txt" files.
    '''

    # This function is essentially a duplicate of the prior function, but without any in-printed data.

    counter = 0
    counter_complete = 0
    counter_uncomplete = 0
    list_of_username = []

    current_date = datetime.today().strftime(DATETIME_STRING_FORMAT)

    overdue_task_incomplete = 0 # This includes overdue task which are ALSO marked as incomplete.
    overdue_task = 0 # This is the total number of overdue tasks, both complete and incomplete.

    task_count_per_user = {}  # This is designed to get number of task per username.

    # This will get the total number of unique registrations.

    for task in task_list:
        counter += 1
        list_of_username.append(task['username'])

    unique_usernames = set(list_of_username)

    # This will provide the total number of task per user.

    for task in task_list:

        if task['username'] in task_count_per_user:
            task_count_per_user[task['username']] += 1
        else:
            task_count_per_user[task['username']] = 1

    # The following For Loop is designed to get number of completed task per username.

    task_completed_per_user = {}

    for task in task_list:
        if task['completed'] == True:
            if task['username'] in task_completed_per_user:
                task_completed_per_user[task['username']] += 1
            else:
                task_completed_per_user[task['username']] = 1

    # The next Loop statement will provide both the completion and non-completion percentage per user.

    task_completion_percentage_per_user = {}

    for username in task_count_per_user.keys():
        total_tasks = task_count_per_user[username]
        completed_tasks = task_completed_per_user.get(username, 0)  # Defensive Programming.
        uncompleted_tasks = total_tasks - completed_tasks

        # Percentage Calculations.
        completed_percentage = (completed_tasks / total_tasks) * 100 if total_tasks else 0
        uncompleted_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks else 0

        # Storing Data into Dictionary.
        task_completion_percentage_per_user[username] = {
            'completed_percentage': completed_percentage,
            'uncompleted_percentage': uncompleted_percentage
        }

    # This will try to calculate the number overdue-uncompleted tasks.

    task_overdue_incomplete = {}

    for task in task_list:
        if task['completed'] == False and task['due_date'].strftime(DATETIME_STRING_FORMAT) < current_date:
            if task['username'] in task_overdue_incomplete:
                task_overdue_incomplete[task['username']] += 1
            else:
                task_overdue_incomplete[task['username']] = 1

    # The following will calculate the percentage of incomplete and overdue tasks.

    task_incompletion_percentage_per_user = {}

    for username in task_count_per_user.keys():
        total_tasks = task_count_per_user[username]
        incomplete_tasks = task_overdue_incomplete.get(username, 0)  # Defensive Programming.

        # Percentage Calculations.
        uncompleted_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks else 0

        # Storing Data into Dictionary.
        task_incompletion_percentage_per_user[username] = uncompleted_percentage

    #  Writes data into external file called "user_overview.txt".
    with open('user_overview.txt', 'w') as file:
        file.write("User Task Report\n")
        file.write("-------------------------------\n")
        file.write(f"There are a total of {counter} task entries, divided between {len(unique_usernames)} unique users,"
                   f" from a total of {len(list_of_username)} users registered in the system.\n\n")

        for username, task_count in task_count_per_user.items():
            workload_percentage = (task_count / len(list_of_username)) * 100
            file.write(f"{username.capitalize()} has registered a grand total of {task_count} tasks.\n")
            file.write(f"This represents {workload_percentage:.2f}% of the workload.\n\n")

        for username, task_count in task_completed_per_user.items():
            file.write(f"{username.capitalize()} has completed a total of {task_count} tasks.\n")
        file.write("\n")

        for username, percentages in task_completion_percentage_per_user.items():
            file.write(f"{username.capitalize()}:\n")
            file.write(f"Completed Tasks: {percentages['completed_percentage']:.2f}%\n")
            file.write(f"Uncompleted Tasks: {percentages['uncompleted_percentage']:.2f}%\n\n")

        for username, task_count in task_overdue_incomplete.items():
            file.write(
                f"{username.capitalize()} has a total of {task_count} tasks which are both incomplete and overdue.\n")
        file.write("\n")

        for username, task_percentage in task_incompletion_percentage_per_user.items():
            file.write(
                f"User: {username.capitalize()}\nIncomplete & Overdue Tasks in Percentage: {task_percentage:.2f}%\n\n")

    # This section will print the task_overview.txt document.

    for task in task_list:
        if task['completed'] == True:
            counter_complete += 1
        else:
            counter_uncomplete += 1

        if task['due_date'].strftime(DATETIME_STRING_FORMAT) < current_date and task['completed'] == False:
            overdue_task_incomplete += 1
        else:
            pass # Skips to below if-else statement without breaking code

        if task['due_date'].strftime(DATETIME_STRING_FORMAT) < current_date:
            overdue_task += 1
        else:
            continue

    total_task = counter_complete + counter_uncomplete

    # Writes data into external file called "task_overview.txt".
    with open('task_overview.txt', 'w') as file:
        file.write("Task Overview Report\n")
        file.write("-------------------------------\n")
        file.write(f"Total Number of Tasks Present: {total_task}\n")
        file.write(f"Number of Completed Tasks: {counter_complete}\n")
        file.write(f"Number of Uncompleted Tasks: {counter_uncomplete}\n\n")

        # This is to avoid a ZeroDivision Error and promote Defense Programming.
        if total_task > 0:
            overdue_incomplete_percentage = (overdue_task_incomplete / total_task) * 100
            overdue_task_percentage = (overdue_task / total_task) * 100
        else:
            overdue_incomplete_percentage = 0
            overdue_task_percentage = 0

        file.write(f"Total Number of Overdue Tasks Marked as Incomplete: {overdue_task_incomplete}\n")
        file.write(f"Percentage of Incompleted Tasks: {overdue_incomplete_percentage:.2f}%\n")
        file.write(f"Percentage of Overdue Tasks: {overdue_task_percentage:.2f}%\n")
        file.write("-------------------------------")



while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Report
ds - Display statistics
e - Exit
: ''').lower()

    if menu == "r":
        reg_user()

    elif menu == "a":
        add_user()

    elif menu == "va":
        view_all()

    elif menu =="vm":
        view_mine()

    elif menu == "gr":
        generate_report()
        print("The files have been generated as request. Please check the immediate directory. "
              "For any issues, please contact the administrators.")

    elif menu == 'ds' and curr_user == 'admin':
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(set(username_password.keys()))
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

        expanded = input("Please Enter Any Key To View Additional Statistics."
                         "\nOtherwise, Please Type '-1' to Exit: ")
        if expanded == "-1":
            continue
        elif not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            generate_report()
            display_report()
        else:
            display_report()
            print("\n-----------------------------------")

    elif menu == "ds" and curr_user != "admin":
        print("You do not have access to this function. Please contact the administrators.")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again.")