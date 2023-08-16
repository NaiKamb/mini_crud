import json
import datetime


def log_activity(method):
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now()
        args_str = ", ".join([repr(arg) for arg in args])
        kwargs_str = ", ".join([f"{key}={repr(value)}" for key, value in kwargs.items()])
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        print(f"[{timestamp}] Выполнен метод {method.__name__} с аргументами: {all_args}")
        return method(*args, **kwargs)
    return wrapper


class Task:
    def __init__(self, title, description, done=False):
        self.title = title
        self.description = description
        self.done = done

    @log_activity
    def mark_as_done(self):
        self.done = True

    @log_activity
    def mark_as_undone(self):
        self.done = False

    def edit_description(self, new_description):
        self.description = new_description

    def __str__(self):
        status = "Выполнено" if self.done else "Не выполнено"
        return f"Задача: {self.title}\nОписание: {self.description}\nСтатус: {status}"


class TaskList:
    def __init__(self):
        self.tasks = []

    @log_activity
    def create_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)

    @log_activity
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    @log_activity
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
        else:
            print("Недопустимый номер задачи.")

    def get_all_tasks(self):
        return self.tasks

    def save_to_json(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            task_data = [{"title": task.title, "description": task.description, "done": task.done} for task in self.tasks]
            json.dump(task_data, f, indent=4, ensure_ascii = False)

    def load_from_json(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                task_data = json.load(f)
                self.tasks = [Task(task["title"], task["description"], task["done"]) for task in task_data]
        except FileNotFoundError:
            pass


def main():
    task_list = TaskList()
    task_list.load_from_json()

    while True:
        print("1. Создать задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Отметить задачу как не выполненную")
        print("5. Удалить задачу")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            task_list.create_task(title, description)
            task_list.save_to_json()
        elif choice == "2":
            tasks = task_list.get_all_tasks()
            for index, task in enumerate(tasks):
                status = "Выполнено" if task.done else "Не выполнено"
                print(f"{index + 1}. {task.title} ({status})")
        elif choice == "3":
            index = int(input("Введите номер задачи для отметки как выполненной (начиная с 1): ")) - 1
            if 0 <= index < len(task_list.tasks):
                task_list.tasks[index].mark_as_done()
                task_list.save_to_json()
            else:
                print("Недопустимый номер задачи.")
        elif choice == "4":
            index = int(input("Введите номер задачи для отметки как не выполненной (начиная с 1): ")) - 1
            if 0 <= index < len(task_list.tasks):
                task_list.tasks[index].mark_as_undone()
                task_list.save_to_json()
            else:
                print("Недопустимый номер задачи.")
        elif choice == "5":
            index = int(input("Введите номер задачи для удаления (начиная с 1): ")) - 1
            task_list.delete_task(index)
            task_list.save_to_json()
        elif choice == "6":
            break
        else:
                print("Недопустимый выбор. Пожалуйста, выберите снова.")


if __name__ == "__main__":
    main()
