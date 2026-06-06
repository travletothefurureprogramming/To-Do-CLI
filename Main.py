from rich.console import Console
import json

console = Console()

def show_tasks():
  tasks = json.load(open("to_do.json"))
  title = []
  status = []
  for task in tasks:
   title.append(task['title'])
   status.append(task['status'])

  return title,status

while True:
 console.print("[underline]1. Show tasks[/underline]")
 console.print("[underline]2. Create task[/underline]")
 console.print("[underline]3. Complete task[/underline]")
 console.print("[red underline]4. Exit[/red underline]")

 select = input("Select number: ")

 if select in "4":
   exit()
 elif select in "1":
   title,status = show_tasks()
   number = 0
   for i in title:
     
     console.print(f"Title:{i}")
     if status[number] == "complete":
       console.print("[green]Completed[/green]")
     elif status[number] == "uncomplete":
        console.print("[red]Uncompleted[\red]")
     number+=number

   


