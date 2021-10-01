from celery import task
from celery.result import AsyncResult


result = AsyncResult(task_id)
print(result.state)  # will be set to PROGRESS_STATE
print(result.info)  # metadata will be here

# this decorator is all that's needed to tell celery this is a worker task
@task
def do_work(self, list_of_work, progress_observer):
    total_work_to_do = len(list_of_work)
    for i, work_item in enumerate(list_of_work): 
        do_work_item(work_item)
        # tell the progress observer how many out of the total items we have processed
        progress_observer.set_progress(i, total_work_to_do)
    return 'work is complete'

task.update_state(
    state=PROGRESS_STATE,
    meta={
        'current': current,
        'total': total,
    }
)