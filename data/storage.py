# data/storage.py

import json
import os

class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title):
        self.tasks.append({"title": title, "details": []})
        self.save()

    def edit_task(self, index, new_title):
        self.tasks[index]["title"] = new_title
        self.save()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save()

    def add_detail(self, task_index, detail):
        self.tasks[task_index]["details"].append(detail)
        self.save()

    def edit_detail(self, task_index, detail_index, new_detail):
        self.tasks[task_index]["details"][detail_index] = new_detail
        self.save()

    def delete_detail(self, task_index, detail_index):
        self.tasks[task_index]["details"].pop(detail_index)
        self.save()
