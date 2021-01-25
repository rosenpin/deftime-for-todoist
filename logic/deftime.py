import logging
from random import randrange

from todoist_service.consts import TaskFields, Due
from todoist_service.todoist_wrapper.todoist_wrapper import TodoistWrapper

STRIKE = "\u0336"


def get_time(task_time: str):
    # between 8 am to 6 pm, reasonable time for TODOs
    hour = 8 + randrange(0, 10)
    if hour < 10:
        hour = "0%s" % hour
    return task_time + "T%s:00:00" % hour


def has_time(task_time: str):
    return ":" in task_time


class TimeSetter:
    def __init__(self, doist: TodoistWrapper):
        self.doist = doist

    def set_time(self, task):
        title = task[TaskFields.Title]
        task_date = task[TaskFields.Due]
        if task_date is None:
            logging.info("skipping %s. doesn't have due date" % task_date)
            return

        task_time = task_date[Due.Date]
        if has_time(task_time=task_time):
            logging.info("skipping %s. already has time" % task_time)
            return

        new_task_time = get_time(task_time=task_time)
        logging.info("set {title} to {task_time}".format(title=title, task_time=new_task_time))
        task.update(due={'date': new_task_time})
        self.doist.commit()
