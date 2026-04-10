#!/usr/bin/env python3
import json
import os
import sys
import argparse
import uuid
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

FILE = os.path.expanduser("~/.todocli.json")
UNDOFILE = os.path.expanduser("~/.todocliundo.json")

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".todocli")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "theme": "default",
    "date_format": "%Y-%m-%d",
    "show_completed": True,
    "default_priority": "medium",
    "progress_bar": True,
    "color": True,
    "compact_view": False,
    "sort_default": "pending",
    "Max_undo": 25
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

    with open(CONFIG_PATH, "r") as f:

        return json.load(f)
config=load_config()

def load_data():
    if not os.path.exists(FILE):
        return {"tasks": []}
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_undo_data(data):
    history = []
    config=load_config()
    MAX_UNDO=config["Max_undo"]

    if os.path.exists(UNDOFILE):
        with open(UNDOFILE, "r") as f:
            history = json.load(f)

    history.append(data)

    if len(history) > MAX_UNDO:
        history.pop(0)
    with open(UNDOFILE, "w") as f:
        json.dump(history, f, indent=4)

def load_undo_data():
    if not os.path.exists(UNDOFILE):
        return None

    with open(UNDOFILE, "r") as f:
        history = json.load(f)

    if not history:
        return None

    return history

def add_task(title,priority=config["default_priority"],due=None,tags=None):
    data = load_data()
    save_undo_data(data)
    task_id=str(uuid.uuid4())[:8]
    data["tasks"].append({"id":task_id,"title": title, "done": False,"priority":priority,"due":due,"tags":tags})
    save_data(data)

def view_tasks(sort=None,tag=None):
    data = load_data()
    tasks=data["tasks"]
    if tag:
        tag_groups = []

        for group in tag:
            tag_groups.append(
                [t.strip().lower() for t in group.split(",")]
            )

        filtered_tasks = []

        for task in tasks:
            task_tags = [t.lower() for t in task.get("tags", [])]

            for group in tag_groups:
                if all(t in task_tags for t in group):
                    filtered_tasks.append(task)
                    break

        tasks = filtered_tasks

    priority_order={"high":0,"medium":1,"low":2}
    if sort=="completed":
            tasks=sorted(tasks,key=lambda x: not x["done"])
    elif sort=="pending":
        tasks=sorted(tasks,key=lambda x: x["done"])
    elif sort=="priority":
        tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority","medium")))
    elif sort=="due_dates":
        tasks=sorted(tasks, key=lambda x: datetime.strptime(x["due"],"%Y-%m-%d").date() if x.get("due") else datetime.max.date())
    elif sort=="tag":
        tasks=sorted(tasks,key=lambda x:",".join(x.get("tags",[])))

    print()
    print("\n#   ID        TITLE                       STATUS   PRIORITY   TAGS                    DUE")
    print("-"*130)
    for i, task in enumerate(tasks):
        if task["done"]:
            status=Fore.GREEN + "[✔]"
        else:
            status=Fore.RED + "[✘]"
        due=task.get("due")
        delta = None
        overdue=False
        if due and not task["done"]:
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
            today = datetime.today().date()
            delta=(due_date-today).days
            if due_date < today and not task["done"]:
                overdue = True
        if due:
            if task["done"]:
                due_display = Fore.GREEN + f"{{due:{due} | completed}}"
            elif overdue:
                due_display=Fore.RED+f"{{due:{due} | overdue by {abs(delta)} days}}"
            elif delta ==0:
                due_display=Fore.YELLOW+"{due today}"
            else:
                due_display=Fore.CYAN+f"{{due:{due} | due in {delta} days}}"
        else:
            due_display=""

        priority=task.get("priority","medium")
        priority_colours={"high":Fore.LIGHTRED_EX,"medium":Fore.YELLOW,"low":Fore.GREEN}
        priority_coloured = priority_colours.get(priority, Fore.WHITE) + f"({priority})"
        tags = ", ".join(task.get("tags", []))
        tags_coloured=Fore.LIGHTMAGENTA_EX+f"|{tags}|"
        
        print(f"{i+1:<3} {task['id']:<10} {task['title']:<27} {status:<13} {priority_coloured:<15} {tags_coloured:<27} {due_display}")
        print()

    if not data["tasks"]:
        print("No tasks found")
        return

def complete_task(task_id):
    data = load_data()
    save_undo_data(data)
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["done"] = True
            save_data(data)
            return
    print("Invalid ID")

def delete_task(task_id):
    data = load_data()
    save_undo_data(data)
    for i, task in enumerate(data["tasks"]):
        if task["id"] == task_id:
            del data["tasks"][i]
            save_data(data)
            return

def edit_task(task_id, title=None, priority=None, due=None, tags=None, done=None):
    data = load_data()
    save_undo_data(data)
    tasks = data["tasks"]

    for task in tasks:
        if task["id"] == task_id:

            if title:
                task["title"] = " ".join(title)

            if priority:
                task["priority"] = priority

            if due:
                task["due"] = due

            if tags is not None:
                task["tags"] = tags

            if done is not None:
                task["done"] = done

            save_data(data)
            print("Task updated")
            return

    print("Task not found")

def stats_task():
    today=datetime.today().date()
    data=load_data()
    tasks=data["tasks"]
    total=len(tasks)
    completed=sum(1 for i in tasks if i["done"])
    remaining=total-completed
    high = sum(1 for t in tasks if t.get("priority") == "high")
    medium = sum(1 for t in tasks if t.get("priority") == "medium")
    low = sum(1 for t in tasks if t.get("priority") == "low")
    overdue = sum(1 for t in tasks if t.get("due") and not t["done"] and datetime.strptime(t["due"], "%Y-%m-%d").date() < today)
    due_today = sum(1 for t in tasks if t.get("due") and datetime.strptime(t["due"], "%Y-%m-%d").date() == today)
    completion_rate = (completed / total * 100) if total else 0
    bar_length = 20
    filled = int(bar_length * completed / total) if total else 0
    bar = "█" * filled + "░" * (bar_length - filled)

    print(Fore.CYAN + "TASK STATISTICS")
    print("-" * 30)
    print(f"{'Total tasks':<18}: {total}")
    print(f"{'Completed':<18}: {Fore.GREEN}{completed}")
    print(f"{'Remaining':<18}: {Fore.YELLOW}{remaining}")
    print()
    print(Fore.CYAN + "PRIORITY")
    print("-" * 30)
    print(f"{'High':<18}: {Fore.LIGHTRED_EX}{high}")
    print(f"{'Medium':<18}: {Fore.YELLOW}{medium}")
    print(f"{'Low':<18}: {Fore.GREEN}{low}")
    print()
    print(Fore.CYAN + "DUE DATES")
    print("-" * 30)
    print(f"{'Overdue':<18}: {Fore.RED}{overdue}")
    print(f"{'Due today':<18}: {Fore.CYAN}{due_today}")
    print()
    print(Fore.CYAN + "TAGS")
    print("-"*30)
    tag_counts = {}

    for task in tasks:
        for tag in task.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    if tag_counts:
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{tag:<18}: {Fore.LIGHTMAGENTA_EX}{count}")
    else:
        print("No tags found")

    print(Fore.CYAN + "PROGRESS")
    print("-" * 30)
    print(f"[{bar}] {completion_rate:.1f}%")

def clear_completed():
    data=load_data()
    save_undo_data(data)
    tasks=data["tasks"]
    new_tasks=[j for j in tasks if not j["done"]]
    data["tasks"]=new_tasks
    removed = len(tasks) - len(new_tasks)
    save_data(data)
    return removed

def search_task(keyword):
    data = load_data()
    tasks = data["tasks"]
    found=False

    print()
    print("\n#   ID        TITLE                       STATUS   PRIORITY   TAGS                    DUE")
    print("-"*130)

    for i, task in enumerate(tasks):
        if (
            keyword.lower() in task["title"].lower()
            or keyword.lower() in " ".join(task.get("tags", [])).lower()
        ):

            if task["done"]:
                status=Fore.GREEN + "[✔]"
            else:
                status=Fore.RED + "[✘]"

            due=task.get("due")
            overdue=False
            delta=None

            if due and not task["done"]:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
                today = datetime.today().date()
                delta=(due_date-today).days
                if due_date < today:
                    overdue = True
                    
            if due:
                if task["done"]:
                    due_display = Fore.GREEN + f"{{due:{due} | completed}}"
                elif overdue:
                    due_display=Fore.RED+f"{{due:{due} | overdue by {abs(delta)} days}}"
                else:
                    due_display=Fore.CYAN+f"{{due:{due} | due in {delta} days}}"
            else:
                due_display=""

            priority=task.get("priority",config["default_priority"])
            priority_colours={"high":Fore.LIGHTRED_EX,"medium":Fore.YELLOW,"low":Fore.GREEN}
            priority_coloured = priority_colours.get(priority, Fore.WHITE) + f"({priority})"
            tags = ", ".join(task.get("tags", []))
            tags_coloured=Fore.LIGHTMAGENTA_EX+f"|{tags}|"
        
            print(f"{i+1:<3} {task['id']:<10} {task['title']:<27} {status:<13} {priority_coloured:<15} {tags_coloured:<27} {due_display}")
            print()

            found=True

    if not found:
        print("No matching tasks")

def undo():
    history = load_undo_data()

    if not history:
        print("Nothing to undo")
        return

    last = history.pop()

    with open(UNDOFILE, "w") as f:
        json.dump(history, f, indent=4)

    save_data(last)


def main():
    parser=argparse.ArgumentParser(prog="todocli")

    subparser=parser.add_subparsers(dest="command", required=True)

    add_parser=subparser.add_parser("add")
    add_parser.add_argument("title", nargs="+")
    add_parser.add_argument("--priority",type=str,choices=["low","medium","high"],default=config["default_priority"])
    add_parser.add_argument("--due",help="Due date in YYYY-MM-DD format")
    add_parser.add_argument("--tag")

    view_parser=subparser.add_parser("view")
    view_parser.add_argument("--sort",choices=["completed","pending","priority","due_dates","tag"])
    view_parser.add_argument("--tag",action="append",help="Filter by tag")

    complete_parser=subparser.add_parser("complete")
    complete_parser.add_argument("id")

    edit_parser=subparser.add_parser("edit")
    edit_parser.add_argument("id")
    edit_parser.add_argument("--title", nargs="+")
    edit_parser.add_argument("--due",help="Due date in YYYY-MM-DD format")
    edit_parser.add_argument("--priority")
    edit_parser.add_argument("--tag", action="append")
    edit_parser.add_argument("--done", action="store_true")
    edit_parser.add_argument("--undone", action="store_true")

    delete_parser=subparser.add_parser("delete")
    delete_parser.add_argument("id")

    stats_parser=subparser.add_parser("stats")

    clear_parser=subparser.add_parser("clear_completed")

    search_parser=subparser.add_parser("search")
    search_parser.add_argument("keyword", nargs="+")

    undo_parser=subparser.add_parser("undo")

    args=parser.parse_args()

    if args.command=="add":
        title=" ".join(args.title)
        tags = args.tag.split(",") if args.tag else []
        tags = [t.strip() for t in tags]
        add_task(title,args.priority,args.due,tags)
        print("Task added")

    elif args.command=="view":
        view_tasks(args.sort,args.tag)

    elif args.command == "complete":
        complete_task(args.id)
        print("Task completed")

    elif args.command == "delete":
        run2=True
        run1=True
        while run1:
            confirm=input("Confirm deletion? (y/n): ")
            if confirm == "y":
                delete_task(args.id)
                print("Task deleted")
                run1=False
            elif confirm == "n":
                print("Task not deleted")
                run1=False
            else:
                while run2:
                    re=input("Invalid input, Try again: ")
                    if re=="n":
                        print("Task not deleted")
                        run1=False
                        run2=False
                    elif re=="y":
                        print("Task deleted")
                        delete_task(args.id)
                        run1=False
                        run2=False
                    else:
                        run2=True

    elif args.command == "edit":
        tags = None

        if args.tag:
            tags = []
            for tag_group in args.tag:
                tags.extend(tag_group.split(","))

            tags = [t.strip() for t in tags if t.strip()]

        done = None
        if args.done:
            done = True
        elif args.undone:
            done = False

        edit_task(args.id,args.title,args.priority,args.due,tags,done)

    elif args.command == "stats":
        stats_task()

    elif args.command == "clear_completed":
        removed=clear_completed()
        print(f"Removed {removed} completed tasks")

    elif args.command == "search":
        keyword=" ".join(args.keyword)
        search_task(keyword)

    elif args.command == "undo":
        undo()
        print("Un-did the last operation")
if __name__ == "__main__":
    main()
