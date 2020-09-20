# owl claw : Simple Task Runner

## feature

- easier and more maintainable than shell scripts
- familiar editor completions

## Sample

```python
from owl import task, Context


@task
def ls(c: Context):
    result = c.run(["ls", "-al")
```
