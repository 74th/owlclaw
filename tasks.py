from owl import task, Context


@task
def do_something(c: Context):
    c.run(["ls"])
