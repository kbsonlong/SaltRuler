from celery import task

@task
def add(x,y):
    return x + y


if __name__ == '__main__':
    result = add.delay(2,2)

