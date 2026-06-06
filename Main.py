import json
from rich.console import Console

console = Console()

def show_tasks():
    with open("to_do.json", "r") as file:
        tasks = json.load(file)  
    return tasks  

def create_task(title):
    with open("to_do.json", "r") as file:
        current_data = json.load(file)

    data = {
        "title": title,
        "status": "uncomplete"  
    }

    current_data.append(data)

    with open("to_do.json", "w") as file:
        json.dump(current_data, file, indent=4) 


def complete_task(title):
    try:
        with open("to_do.json", "r") as file:
            current_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        console.print("[red]Error: No tasks found or file is empty![/red]")
        return

    task_found = False
    
    for data in current_data:
        if data["title"] == title:  
            data["status"] = "complete"  
            task_found = True
            break  

    if task_found:
        with open("to_do.json", "w") as file:
            json.dump(current_data, file, indent=4)
        console.print(f"[green]Task '{title}' marked as complete![/green]")
    else:
        console.print(f"[yellow]Task '{title}' not found.[/yellow]")
            

while True:
    console.print("\n[underline]1. Show tasks[/underline]")
    console.print("[underline]2. Create task[/underline]")
    console.print("[underline]3. Complete task[/underline]")
    console.print("[red underline]4. Exit[/red underline]")

    select = input("Select number: ")

    if select == "4":
        exit()
        
    elif select == "1":
        tasks = show_tasks()
        
        for task in tasks: 
            console.print(f"Title: {task['title']}")
            if task['status'] == "complete":
                console.print("[green]Completed[/green]")
            else:
                console.print("[red]Uncompleted[/red]") 

    elif select == "2":
        title = input("Enter title: ")
        create_task(title)
        console.print("[green]Task created successfully![/green]")
    
    elif select == "3":
        title = input("Enter title: ")
        complete_task(title)
