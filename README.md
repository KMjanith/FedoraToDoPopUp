# Floating To-Do List (Tkinter + Docker)

A minimal floating to-do list app with support for subtasks, built using Python's Tkinter and packaged into a Docker container. This app runs as a small draggable widget on your screen and pops up a task manager when clicked.

---

##  Features

-  Floating draggable button on your screen
-  Double-click tasks to toggle subtasks window
-  Add/edit/delete tasks and subtasks
-  Persistent storage using `tasks.json`
-  Dockerized for easy sharing and usage

---

##  Docker Image

The application is published on Docker Hub:

 **[Docker Hub – mjanith/todo-widget](https://hub.docker.com/r/mjanith/todo-widget/tags)**

---

## How to Run (Linux with X11)

These steps assume you're on **Linux with X11** (Ubuntu, Fedora, Arch, etc).

### 1. pull the doccker image
```bash
docker pull mjanith/todo-widget
```
### 2. Allow Docker access to your X11 display
```bash
xhost +local:docker
```
### 3. Run docker container
```
docker run --rm -d\
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $HOME/.todo_widget_data:/app \
    --name todo-widget \
    mjanith/todo-widget:1.0
```
## 3. Or you can make a shortcut command as a alias

### 3.1 open `bashrc` file
```
nano ~/.bashrc
```
### 3.2 make the alis
```
alias starttodo='xhost +local:docker && docker run --rm -d -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name todo-widget mjanith/todo-widget:1.0'

```
### 3.3 save and exit
### 3.4 source the file
```
source ~/.bashrc
```
### 3.5 then open a terminal and type 
```
starttodo
```
* Then a icon will show in your desktop. you can `right click on it and hold to drag anywhere in your desktop`

# samples
![the draggable icon](<Screenshot from 2025-05-07 12-44-12.png>)
![main topic enter page](<Screenshot from 2025-05-07 12-44-22.png>)
![add a new topic](<Screenshot from 2025-05-07 12-44-34.png>)
![add details](<Screenshot from 2025-05-07 12-44-45.png>)
![edit details](<Screenshot from 2025-05-07 12-44-55.png>)
