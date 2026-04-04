# todocli

A fast, minimal, and powerful terminal-based TODO manager written in Python.

`todocli` helps you manage tasks directly from your terminal with:

* Tags
* Priorities
* Due dates
* Search
* Stats
* Sorting
* Multi-tag filtering
* Cross-platform support (Linux + Windows)

---

# Features

## Task Management

* Add tasks
* Edit tasks
* Delete tasks
* Mark tasks complete
* Clear completed tasks

## Organization

* Tags (`--tag school,exam`)
* Priority levels (`high`, `medium`, `low`)
* Due dates
* Search by title or tags

## Viewing & Sorting

* Sort by priority
* Sort by due date
* Sort by completed
* Sort by pending
* Filter by tags (AND / OR logic)

## Statistics

* Completed vs Pending
* Priority breakdown
* Tag distribution
* Progress bar

---

# Installation
## Linux
```bash
git clone https://github.com/0IOS/todocli
cd todocli
chmod +x install.sh
```
Then:
```bash
./install.sh
```
Restart your Terminal,then run:
```bash
todocli
```
## Windows
```bash
git clone https://github.com/0IOS/todocli
cd todocli
```
Then:
```powershell
./install.ps1
```
If you get a execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then run again:
```powershell
./install.ps1
```
Restart Terminal/Powershell,then run:
```bash
todocli
```

## Requirements

* Python 3.8+
* Git
* colorama

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Usage

## Add Task

```bash
todocli add "Study Physics" --priority high --tag school,exam --due 2026-04-01
```

---

## View Tasks

```bash
todocli view
```

---

## Sort Tasks

```bash
todocli view --sort priority
todocli view --sort due_dates
todocli view --sort pending
todocli view --sort completed
```

---

# Tag Filtering

`todocli` supports **OR** and **AND** tag filtering.

## OR Filtering (comma separated)

Shows tasks matching **any** tag:

```bash
todocli view --tag school,exam
```

Matches:

* school
* exam
* school + exam

---

## AND Filtering (multiple --tag)

Shows tasks matching **all** tag groups:

```bash
todocli view --tag school --tag exam
```

Matches only tasks that contain:

* school
  AND
* exam

---

## Combined Filtering

You can combine AND + OR:

```bash
todocli view --tag school,exam --tag urgent
```

Meaning:

```
(school OR exam) AND urgent
```

This gives very powerful filtering.

---

# Edit Task

Edit everything:

```bash
todocli edit <id> "New Title" --priority high --tag school --due 2026-04-02 --done
```

Example:

```bash
todocli edit a9c5e2f2 "Study Maths" --tag exam --priority high
```

---

# Complete Task

```bash
todocli complete <id>
```

---

# Delete Task

```bash
todocli delete <id>
```

---

# Search Tasks

```bash
todocli search physics
```

Search checks:

* Title
* Tags

---

# Statistics

```bash
todocli stats
```

Shows:

* Completed tasks
* Pending tasks
* Priority breakdown
* Tag distribution
* Progress bar

---

# Clear Completed Tasks

```bash
todocli clear_completed
```

---

# Example

```bash
todocli add "Math Homework" --priority high --tag school --due 2026-04-01
todocli add "Python Project" --priority medium --tag coding
todocli view --tag school
todocli stats
```

---

# Project Structure

```
todocli/
├── todocli
├── todocli_main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Cross Platform

Works on:

* Linux
* Windows
* macOS

Windows users can run:

```bash
python todocli_main.py
```

---

# Roadmap

Planned Features

* Config system
* Themes
* Subtasks
* Recurring tasks
* Export / Import
* Interactive mode
* Custom columns

---

# License

MIT License

---

# Author

Saurabh Gupta

---

# Why todocli?

* Fast
* Lightweight
* No dependencies
* Terminal friendly
* Cross-platform
* Highly customizable