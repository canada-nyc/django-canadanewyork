from configs.jobs import transform_task


def enqueue(function, *args, **kwargs):
    transform_task.delay(*args, **kwargs)
