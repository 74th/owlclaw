import unittest

import owl.tasks


class TestTasks(unittest.TestCase):
    def test_task(self):
        from tests import tasks

        c = owl.tasks.load_module("task", tasks)
        assert "task1" in c.tasks
