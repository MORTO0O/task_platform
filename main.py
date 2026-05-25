from .receiver import TaskReceiver
from .sources.file_source import FileTaskSource
from .sources.generator_source import GeneratorTaskSource
from .sources.API_source import APITaskSource
from .exceptions import TaskError
from .queue import TaskQueue

if __name__ == '__main__':
    receiver = TaskReceiver()

    receiver.add_source(FileTaskSource("src/tasks.json"))
    receiver.add_source(GeneratorTaskSource(count=8))
    receiver.add_source(APITaskSource())

    queue = TaskQueue()

    print("\nЗагрузка задач в очередь...")
    queue.add_tasks(receiver.stream_tasks())

    print('\n<<<<< Все задачи >>>>>')
    for task in queue:
        print(f"[{task.id}] Приоритет: {task.priority}, Статус: {task.status}")

    print("<<<<< Фильтрация от приоритета 4+ >>>>>")
    high_priority = queue.filter_by_priority(4)
    for task in high_priority:
        print(f"ВАЖНАЯ ЗАДАЧА: {task.id} Приоритет: {task.priority}")

    print("Фильтрация по статусу")
    ready_status = queue.filter_by_status("ready")
    for task in ready_status:
        print(f"ГОТОВЫЕ ЗАДАЧИ: {task.id}. Статус: {task.status}")

    all_tasks_list = list(queue)
    print(f"\nВсего задач в очереди: {len(all_tasks_list)}")