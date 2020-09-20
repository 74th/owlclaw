import unittest

import owl


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        c = owl.Context()
        with c.cd("tests"):
            result = c.run("ls")
            assert result.ok
            assert not result.failed
            assert isinstance(result.stdout, str)
            assert len(result.stdout) > 0
            print(result.stdout)
            print(result.stdout_lines)
        print(c.cwd)


if __name__ == "__main__":
    unittest.main()
