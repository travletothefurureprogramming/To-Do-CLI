import json
import os
from rich.console import Console
from rich.table import Table  
import datetime
import questionary

console = Console()
DB_FILE = "to_do.json"
SETTINGS_FILE = "settings.json"


def init_db():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def init_settings():
    if not os.path.exists(SETTINGS_FILE) or os.path.getsize(SETTINGS_FILE) == 0:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"labels": []}, f, indent=4)



def load_tasks():
    init_db()
    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def load_settings():
    init_settings()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
            return {"labels": []}


def save_tasks(tasks):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def save_settings(label):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(label, file, indent=4, ensure_ascii=False)


def show_tasks():
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]There are no tasks in the list![/yellow]")
        return

    table = Table(title="📋 My To-Do List", title_style="bold magenta")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Label", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Date", justify="center")
    table.add_column("Priority", justify="center")

    for idx, task in enumerate(tasks, start=1):
        status = (
            "[green]✔ Complete[/green]"
            if task["status"] == "complete"
            else "[red]❌ Pending[/red]"
        )
        table.add_row(str(idx), task["title"],task["label"],status, task["datetime"], task["priority"])

    console.print(table)


def show_uncompleted_tasks():
    count = 0
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]There are no tasks in the list![/yellow]")
        return

    table = Table(title="📋 My To-Do List", title_style="bold magenta")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Label", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Date", justify="center")
    table.add_column("Priority", justify="center")

    for idx, task in enumerate(tasks, start=1):
        if task["status"] != "complete":
            table.add_row(str(idx), task["title"],task["label"],"[red]❌ Pending[/red]", task["datetime"], task["priority"])
            count += 1
    
    if count >= 1:
        console.print(table)
    else:
        console.print("[green]All tasks have been completed![/green]")


def clear_all_tasks():
    with open("to_do.json", "w", encoding="utf-8") as f:
        json.dump([], f)
    
    console.print(
        f"[green]All tasks have been deleted![/green]"
    )


def create_task(title,label,priority):
    tasks = load_tasks()
    tasks.append({"title": title,"label": label,"status": "uncomplete", "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "priority": priority})
    save_tasks(tasks)
    console.print(
        f"[green]✔ Task '{title}' was created successfully![/green]"
    )

def filter_tasks(label):
    count = 0
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]There are no tasks in the list![/yellow]")
        return

    table = Table(title="📋 My To-Do List", title_style="bold magenta")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Label", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Date", justify="center")
    table.add_column("Priority", justify="center")

    for idx, task in enumerate(tasks, start=1):
        if task["label"] == label:
            table.add_row(str(idx), task["title"],task["label"],"[red]❌ Pending[/red]", task["datetime"], task["priority"])
            count += 1
    
    if count >= 1:
        console.print(table)
    else:
        pass

def complete_task(task_id):
    tasks = load_tasks()
    try:
        idx = int(task_id) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["status"] = "complete"
            save_tasks(tasks)
            console.print(
                f"[green]✔ Task '{tasks[idx]['title']}' completed![/green]"
            )
        else:
            console.print("[red]Wrong ID. Task not found.[/red]")
    except ValueError:
        console.print("[red]Please enter a valid ID number.[/red]")


def delete_task(task_id):
    tasks = load_tasks()
    try:
        idx = int(task_id) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            save_tasks(tasks)
            console.print(
                f"[green]🗑 Task '{removed['title']}' was deleted![/green]"
            )
        else:
            console.print("[red]Wrong ID. Task not found.[/red]")
    except ValueError:
        console.print("[red]Please enter a valid ID number.[/red]")


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def create_label(label):
    labels = load_settings()

    labels["labels"].append(label)

    save_settings(labels)

def get_labbels():
    labels = load_settings()
    return labels["labels"]


init_db()
init_settings()

while True:
    console.print("\n[bold blue]=== MENU ===[/bold blue]")
    console.print("1. 📋 View tasks")
    console.print("2. ➕ Add task")
    console.print("3. ✔ Complete task (by ID)")
    console.print("4. 🗑 Delete task (by ID)")
    console.print("5. ➕ Create Label")
    console.print("6. 🧼 Clear Terminal")
    console.print("7. 🔍 View pending tasks")
    console.print("8. 📌 Filter tasks based on label")
    console.print("[red]9. 🧹 Delete all[/red]")
    console.print("[red]10. 🚪 Exit[/red]")

    select = input("\nSelect option: ").strip()

    if select == "10":
        console.print("[bold yellow]Goodbye![/bold yellow]")
        break
    elif select == "9":
        clear_all_tasks()
    elif select == "1":
        show_tasks()
    elif select == "2":
        labels = get_labbels()

        if not labels:
            console.print("[red]No labels available. Create a label first![/red]")
            continue

        title = input("Task title: ")

        priority = questionary.select(
            "Select Priority Level:",
            choices=["Low", "Medium", "High"]
        ).ask()

        label = questionary.select(
            "Select label",
            choices=labels,
        ).ask()

        if title.strip():
            create_task(title, label, priority)
        else:
            console.print("[red]Title cannot be empty![/red]")
    elif select == "3":
        show_tasks()
        task_id = input("Enter the ID of the task you completed: ")
        complete_task(task_id)
    elif select == "4":
        show_tasks()
        task_id = input("Enter the ID of the task to delete: ")
        delete_task(task_id)
    elif select == "5":
        label_name = input("Enter label name: ")
        if label_name in get_labbels():
            console.print("[yellow]Label already exists![/yellow]")
        else:
            create_label(label_name)
    elif select == "6":
        clear()
    elif select == "7":
        show_uncompleted_tasks()
    elif select == "8":
        labels = get_labbels()

        if not labels:
            console.print("[red]No labels available![/red]")
            continue

        label = questionary.select(
            "Select label",
            choices=labels,
        ).ask()

        filter_tasks(label)
    else:
        console.print("[red]Invalid option![/red]")
