import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

from colorama import Fore, Back, Style, init

# Initialize colorama
init()

conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

def add_task(task_name, description):
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
                   INSERT INTO tasks (task_name, description, status, date_added)
                   VALUES (?, ?, 'pending', ?)
                   ''', (task_name, description, date_added))
    conn.commit()
    messagebox.showinfo("Success", f"Task '{task_name}' added successfully.")
    print(Fore.GREEN + f"Task '{task_name}' added successfully." + Style.RESET_ALL)

def view_tasks():
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    print(Fore.CYAN + "\nCurrent Tasks:" + Style.RESET_ALL)
    for task in tasks:
        print(f"ID: {task[0]}, Name: {task[1]}, Status: {task[3]}, Added: {task[4]}")


def update_task_status(task_id, new_status):
    cursor.execute('''
                   UPDATE tasks
                   SET status = ?
                   WHERE id = ?
                   ''', (new_status, task_id))
    conn.commit()
    print(f"Task ID {task_id} updated to '{new_status}'.")


def view_tasks_by_status(status):
    cursor.execute('SELECT * FROM tasks WHERE status = ?', (status,))
    tasks = cursor.fetchall()
    print(f"\nTasks with status '{status}':")
    for task in tasks:
        print(f"ID: {task[0]}, Name: {task[1]}, Added: {task[4]}")

while True:
    print(Fore.YELLOW + "\nOptions: \n1) Add Task \n2) View Tasks \n3) Update Task Status \n4) View Task By Status \n5)Exit" + Style.RESET_ALL)
    choice = input("Choose an option: ")
    
    if choice == '1':
        task_name = input("Enter task name: ")
        description = input("Enter task description: ")
        add_task(task_name, description)
    elif choice == '2':
        view_tasks()
    elif choice == '3':
        task_id = input("Enter the ID of the task to update: ")
        new_status = input("Enter new status (pending, in-progress, complete): ")
        update_task_status(task_id, new_status)
    elif choice == '4':
        status = input("Filter by (pending, in-progress, complete): ")
        view_tasks_by_status(status)      
    elif choice == '5':
        break
    else:
        print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)

conn.close()
