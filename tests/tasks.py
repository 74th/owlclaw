from owl import task, Context


@task
def task1(c: Context, aaa: int):
    c.run("ls")
