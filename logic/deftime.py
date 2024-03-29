import logging
from random import randrange
import datetime
import pytz

from todoist_api_python.models import Task, Due
from todoist_service.todoist_wrapper.todoist_wrapper import TodoistWrapper

STRIKE = "\u0336"


def get_time(task_time: str):
    current = datetime.datetime.now(pytz.timezone("Asia/Jerusalem"))
    current_date = "{year}-{month}-{day}".format(
        year=current.year, month=current.month, day=current.day
    ).replace("0", "")
    logging.info(
        "current date {current} and got date {task_time}".format(
            current=current_date, task_time=task_time.replace("0", "")
        )
    )
    if current_date == task_time.replace("0", ""):
        logging.info("using current date since it's today: %s" % current.hour)
        hour = current.hour + 1 + abs(randrange(0, 24 - current.hour))
    else:
        # between 8 am to 6 pm, reasonable time for TODOs
        hour = 8 + randrange(0, 10)

    if hour < 10:
        hour = "0%s" % hour
    desired_date_time = task_time + "T%s:00:00.000000" % hour
    return desired_date_time


def has_time(task_time: str):
    return ":" in task_time


class TimeSetter:
    def __init__(self, doist: TodoistWrapper):
        self.doist = doist

    def set_time(self, task: Task):
        title = task.content
        task_due = task.due
        logging.info("got task due: %s", task_due)
        if task_due is None:
            logging.info("skipping %s. doesn't have due date" % task_due)
            return

        task_date = task_due.date
        if task_due is None:
            logging.info("skipping %s. doesn't have due date" % task_due)
            return

        if task_due.datetime is not None and has_time(task_time=task_due.datetime):
            logging.info("skipping %s. already has time" % task_date)
            return

        try:
            new_task_time = get_time(task_time=task_date)
            logging.info(
                "set {title} to {task_time}".format(
                    title=title, task_time=new_task_time
                )
            )
            self.doist.update_task(task.id, due_date=new_task_time)
        except BaseException as e:
            logging.error("got error %s" % e)
