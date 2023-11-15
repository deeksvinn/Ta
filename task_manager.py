'''Capstone project -- Task Manager program which uses functions to maintain the functionality of the program. 
main_menu function -- to display menu options
reg_user function -- to register new users
add_task function -- to add new tasks to the users
view_all function -- to view all the tasks assigned 
view_mine function -- to view tasks assigned to the current user
generate_reports function -- to generate reports in two text files task_overview and user_overview
display_statistics function -- reports are generated and displayed on the screen
read_from_task_text_file function and read_from_user_textfile function are used to read data from tasks.txt and user.txt files 
respectively and are used in view_mine function,generate_reports function and display statistics functions '''

# Function to display menu options

def main_menu():
    while True:
        # Presenting the menu to the user and making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following Options below:
                        r - Registering a user
                        a - Adding a task
                        va - View all tasks
                        vm - View my task
                        gr - generate reports
                        ds - Display statistics
                        e - Exit
                        : ''').lower()  
        if menu == 'r':
            reg_user()   
        elif menu == 'a':
            add_task()    
        elif menu == 'va':
            view_all()
        elif menu == 'vm':
            view_mine()    
        elif menu == 'gr':
            generate_reports()
        elif menu == 'ds':
            display_statistics()       
        elif menu == 'e':
            print("Goodbye")   
            exit()
        else:
            print("You have made a wrong choice. Please try again.")    

# Function to register a new user.

def reg_user():

    # Request input of a new username. 
    new_username = input("New Username: ").lower()

    # To Check if the username already exists in user.txt.
    with open("user.txt", 'r') as user_file:
        if new_username in user_file.read():
            print("Username already exists. Try a new one")

        # If username already doesn't exist, create new one.    
        else:          
            new_password = input("New Password: ").lower()
            confirm_password = input("Confirm Password: ").lower()
            if new_password == confirm_password:
                print("New user added")

                # Add the new user to the user.txt file.
                username_password[new_username] = new_password 
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
            else:
                print("Passwords do no match")

# Function to add a new task.

def add_task():
 
    task_username = input("Name of the person to be assigned to the task: ").lower()

    # To check if the entered user exists.
    if task_username not in username_password.keys():
        print("User does not exist.")
        main_menu()

    # To take details of the task as input.
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # To check if the entered date is in right format.
    while True:
        try:
            task_due_date = input("Due date of task in (YYYY-MM-DD) format: ")
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

    # Append the entered new task details to task_list.
    task_list.append(new_task)

    # Writing the entered new task details to the tasks.txt.
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

# Function to view all the tasks.

def view_all():

    '''Reads the task from task.txt file and prints to the console in the 
           format of Output presented in the task pdf (i.e. includes spacing
           and labelling) 
    '''
    file_tasks = "tasks.txt" 
    if os.stat(file_tasks).st_size == 0:
        print("No tasks are set yet.")

    else:
        
        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description:  {t['description']}\n"
            print(disp_str)

# Function to read data from tasks.txt to get details of tasks.

def read_from_tasks_textfile():
    user_tasks = []

    # To calculate the number of tasks.
    with open('tasks.txt','r') as tasks:
        tasks_details = tasks.readlines()
        number_of_tasks = len(tasks_details)
        task_data = [x.strip().split(", ") for x in tasks_details]

        # To find the details of users who are assigned tasks. 
        for task in task_data:
            for user_task in task:
                task_split = user_task.strip().split(";") 
                if task_split[0] in username_password.keys():
                    user_tasks.append(task_split[0])
        return number_of_tasks,task_data,user_tasks

# Function to read data from user.txt file to get details of users.

def read_from_user_textfile():
   with open('user.txt','r') as users:
        
        # To calculate the number of users.
        users_details = users.readlines()
        number_of_users = len(users_details)
        users_details = [x.strip().split(", ") for x in users_details]
        return number_of_users,users_details

# Function to view and make changes to the task of the current user logged in. 
def view_mine():
     
    number_of_tasks,task_data,user_tasks = read_from_tasks_textfile()

    #To check if tasks are assigned to the current user
    if curr_user not in user_tasks:
        print("Tasks are not yet assigned to this user.")
        main_menu() 

    # To view tasks assigned to the current user who is logged in.
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task Number: \t\t{task_list.index(t)+1}\n"    
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Task Completion:\t{t['completed']}\n"
            print(disp_str) 

    # To edit the task of the current user.
    while True:
        try:
            # Take input as task number to be changed or -1 to go to the main menu.
            select_task = int(input('''Please enter the task number you would like to edit or 
                            -1 to go to the main menu:\n '''))
            # If -1 is selected, go to the main menu
            if select_task == -1:
                main_menu()

            # After task number is entered, choose to mark the task complete or edit the task.
            else:
                choose = input('''Please choose, what would you like to do. 
                To mark the task as complete,enter "mark" or 
                To edit the task,enter "edit"\n"''').lower()

                # To mark the task as complete.
                if choose == 'mark':
                    for d in task_list:
                        if d['username'] == curr_user:
                            if d['completed'] == "No":
                                d['completed'] = "Yes"
                                print("The task completion value changed to ",d['completed']) 
                            else:
                                print("Task already completed")  

                # To edit the task.                 
                elif choose == 'edit':
                    for task in task_list:
                        # If the task is not completed for the current user, change username or due date.
                        if task['username'] == curr_user:
                            if task['completed'] == "No":
                                change_task = input("Would you like to change the username or due date: ")
                                if change_task == 'username':
                                    task['username'] = input("Enter the new user who has to complete the task: ")
                                    print(task['username'])
                                elif change_task == 'due date':
                                    new_date = input("Enter due date: ")
                                    task['due_date'] = (datetime.strptime(new_date,DATETIME_STRING_FORMAT)).date()
                                    print(task['due_date'])  
                                else:
                                    print("No other option to change.Only username or due date can be changed.")  
                            else:
                                print("You can't make any changes. Task is already completed.")  
                            break           
                else:
                    print("Wrong Choice")    

        # If something is entered apart from task number.                             
        except ValueError:
            print("Enter only the task number or -1")  
        break 

# Function to generate reports task_overview and user_overview text files.

def generate_reports():

    incomplete_count = 0
    complete_count = 0
    overdue_count = 0
    user_tasks = []
    users_list = []
    number_of_tasks,task_data,user_tasks = read_from_tasks_textfile()
        
    # To write data to task_overview.txt.
    with open('task_overview.txt', 'w') as overview:

        # To check the completed status of the tasks and increment the corresponding counter.
        for task in task_list: 
            if task['completed'] == 'No':
                incomplete_count += 1    
                curr_date = datetime.now() 
                if curr_date >= task['due_date']:
                    overdue_count +=1
                else:
                    continue    
            else:
                complete_count += 1 

        percent_tasks_incomplete =  (incomplete_count/number_of_tasks)*100 
        percent_tasks_overdue = (overdue_count/number_of_tasks)*100 

        # Writing data to the file task_overview.txt.
        data_in_file = f"Number of tasks generated are {number_of_tasks}\n"            
        data_in_file += f"Number of completed tasks is {complete_count}\n"
        data_in_file += f"Number of incompleted tasks is {incomplete_count}\n"
        data_in_file += f"Number of incompleted and overdue tasks is {overdue_count}\n"
        data_in_file += f"The percentage of tasks that are incomplete is {percent_tasks_incomplete}\n"
        data_in_file += f"The percentage of tasks that are overdue is {percent_tasks_overdue}"
        overview.write(data_in_file)  

        # To write data to user_overview.txt.

        # To read data from user.txt.
        number_of_users,users_details = read_from_user_textfile()

        # To find the details of users.
        for login_details in users_details:
            for user in login_details:
                users_details_split = user.strip().split(";") 
                users_list.append(users_details_split[0] )  
        
        # Creation of user_overview.txt.
        with open('user_overview.txt', 'w') as overview:
            data_in_file = f"Number of users registered is {number_of_users}\n"
            data_in_file += f"Number of tasks generated are {number_of_tasks}\n\n"
            data_in_file += f"Tasks details for each user are as follows.\n"
            data_in_file += f"\n"
            
            # To calculate the total number of tasks assigned to each user.
            for user in users_list:
                count = 0
                incomplete_count_user = 0
                overdue_count_user = 0
                complete_count_user = 0  

                # To check if the user is in user_tasks list which has the names of the users who are assigned tasks.
                for user_task in user_tasks:
                    if user not in user_task:
                        count += 0
                        incomplete_count_user = 0
                        overdue_count_user = 0
                        complete_count_user = 0 
                    else:
                        count += 1 

                # To check the status of task -- completed,incomplete or overdue.
                for task in task_list: 
                    if task['username'] == user:
                        if task['completed'] == 'No':
                            incomplete_count_user += 1    
                            curr_date = datetime.now() 
                            if curr_date >= task['due_date']:
                                overdue_count_user += 1
                            else:
                                continue    
                        else:
                            complete_count_user += 1

                percent_tasks_complete_user = 0
                percent_tasks_incomplete_user = 0
                percent_tasks_overdue_user = 0               

                # To calculate percentages.
                try:
            
                    percent_total_tasks_assigned = round((count/number_of_tasks)*100)
                    percent_tasks_incomplete_user =  round((incomplete_count_user/count)*100)
                    percent_tasks_overdue_user = round((overdue_count_user/count)*100)  
                    percent_tasks_complete_user = round((complete_count_user/count)*100) 

                except ZeroDivisionError:
                    print("")

                # To write to the file user_overview.txt
                data_in_file += f"User : {user}\n"
                data_in_file += f"The total number of tasks assigned is {count}\n"
                data_in_file += f"The percentage of total number of tasks assigned is {percent_total_tasks_assigned}%\n"           
                data_in_file += f"The percentage of completed tasks is {percent_tasks_complete_user}%\n"
                data_in_file += f"The percentage of tasks that are incomplete is {percent_tasks_incomplete_user}%\n"
                data_in_file += f"The percentage of tasks that are overdue is {percent_tasks_overdue_user}%\n"   
                data_in_file +=  f"\n"        
            overview.write(data_in_file) 
   
    print('''Two reports are generated.\n 
        For details of tasks -- task_overview.txt\n 
        For details of tasks assigned to users -- user_overview.txt\n''')
    
# Function to display statistics on the terminal.
    
def display_statistics():

    # Statistics will be displayed only to admin user.    
    if curr_user == 'admin': 

        # If tasks.txt file doesn't exist or not generated yet, create one.    
        if not os.path.exists("tasks.txt"):  
            with open("tasks.txt", "w") as default_file:
                pass

        # If user.txt file doesn't exist or not generated yet, create one with a default account. 
        if not os.path.exists("user.txt"): 
            with open("user.txt", "w") as default_file:
                default_file.write("admin;password")

        # To get the details about tasks from tasks.txt.        
        number_of_tasks,task_data,user_tasks = read_from_tasks_textfile()
        print("Number of tasks generated: ",number_of_tasks)

        # To get the details about users from user.txt.  
        number_of_users,user_details = read_from_user_textfile()  
        print("number of users: ",number_of_users)    

        # To print all task details in user friendly manner.
        for task in task_data:
            for item in task:
                task_split = item.strip().split(";") 
                
                print("------------------------------------------")
                print("user is:",task_split[0])
                print("Title of the task is :",task_split[1])
                print("Description of the task is :",task_split[2])
                print("Due date of the task is :",task_split[3])
                print("task assigned date is :",task_split[4])
                print("Task completion status is :",task_split[5])  
        
    else:
        print("Only admin user is allowed to view details of tasks.")        

# Main program

import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist.
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component to task_list.
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = "Yes" if task_components[5] == "Yes" else "No"

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account.
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

# Input login details
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist.Username and password are case sensitive.They can only be lower case letters.")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True
                    
main_menu()

                            