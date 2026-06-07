import json
import os
from rich.console import Console
from rich.table import Table  
import datetime

console = Console()
DB_FILE = "to_do.json"


def init_db():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_tasks():
    init_db()
    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def show_tasks():
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]Δεν υπάρχουν εργασίες στη λίστα![/yellow]")
        return

    table = Table(title="📋 Η To-Do Λίστα Μου", title_style="bold magenta")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Τίτλος", style="white")
    table.add_column("Κατάσταση", justify="center")
    table.add_column("Ημερομηνία", justify="center")


    for idx, task in enumerate(tasks, start=1):
        status = (
            "[green]✔ Ολοκληρώθηκε[/green]"
            if task["status"] == "complete"
            else "[red]❌ Εκκρεμεί[/red]"
        )
        table.add_row(str(idx), task["title"], status, task["datetime"])

    console.print(table)


def show_uncompleted_tasks():
    count = 0
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]Δεν υπάρχουν εργασίες στη λίστα![/yellow]")
        return

    table = Table(title="📋 Η To-Do Λίστα Μου", title_style="bold magenta")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Τίτλος", style="white")
    table.add_column("Κατάσταση", justify="center")
    table.add_column("Ημερομηνία", justify="center")
    

    for idx, task in enumerate(tasks, start=1):
        if task["status"] != "complete":
         table.add_row(str(idx), task["title"], "✔ Ολοκληρώθηκε", task["datetime"])
         count +=1
    
    if count > 1:
     console.print(table)
    else:
      console.print("[green]Όλλες οι εργασίες έχουν ολοκληρωθεί![/green]")

def clear_all_tasks():
    with open("to_do.json","w",encoding="utf-8") as f:
            json.dump([], f)
    
    console.print(
                f"[green]Όλλες οι εργασίες έχουν διαγραφεί![/green]"
            )


def create_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "status": "uncomplete", "datetime":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    save_tasks(tasks)
    console.print(
        f"[green]✔ Η εργασία '{title}' δημιουργήθηκε με επιτυχία![/green]"
    )


def complete_task(task_id):
    tasks = load_tasks()
    try:
        idx = int(task_id) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["status"] = "complete"
            save_tasks(tasks)
            console.print(
                f"[green]✔ Η εργασία '{tasks[idx]['title']}' ολοκληρώθηκε![/green]"
            )
        else:
            console.print("[red]Λάθος ID. Δεν βρέθηκε η εργασία.[/red]")
    except ValueError:
        console.print("[red]Παρακαλώ δώσε έναν έγκυρο αριθμό (ID).[/red]")


def delete_task(task_id):
    tasks = load_tasks()
    try:
        idx = int(task_id) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            save_tasks(tasks)
            console.print(
                f"[green]🗑 Η εργασία '{removed['title']}' διαγράφηκε![/green]"
            )
        else:
            console.print("[red]Λάθος ID. Δεν βρέθηκε η εργασία.[/red]")
    except ValueError:
        console.print("[red]Παρακαλώ δώσε έναν έγκυρο αριθμό (ID).[/red]")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


init_db()

while True:
    console.print("\n[bold blue]=== MENU ===[/bold blue]")
    console.print("1. 📋 Προβολή εργασιών")
    console.print("2. ➕ Προσθήκη εργασίας")
    console.print("3. ✔ Ολοκλήρωση εργασίας (με ID)")
    console.print("4. 🗑 Διαγραφή εργασίας (με ID)")
    console.print("5. 🧼 Καθαρισμός Terminal")
    console.print("6. 🔍 Προβολή εκρεμής εργασιών")
    console.print("[red]7. 🧹Διαγραφή όλλων[/red]")
    console.print("[red]8. 🚪 Έξοδος[/red]")

    select = input("\nΕπιλογή: ").strip()

    if select == "8":
        console.print("[bold yellow]Αντίο![/bold yellow]")
        break
    if select == "7":
        clear_all_tasks()
    elif select == "1":
        show_tasks()
    elif select == "2":
        title = input("Τίτλος εργασίας: ")
        if title.strip():
            create_task(title)
        else:
            console.print("[red]Ο τίτλος δεν μπορεί να είναι κενός![/red]")
    elif select == "3":
        show_tasks()
        task_id = input("Δώσε το ID της εργασίας που ολοκλήρωσες: ")
        complete_task(task_id)
    elif select == "4":
        show_tasks()
        task_id = input("Δώσε το ID της εργασίας για διαγραφή: ")
        delete_task(task_id)
    elif select == "5":
        clear()
    elif select == "6":
        show_uncompleted_tasks()
    else:
        console.print("[red]Μη έγκυρη επιλογή![/red]")