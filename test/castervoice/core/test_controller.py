import unittest

from castervoice.core.controller import Controller


class TestController(unittest.TestCase):
    # pylint: disable=import-outside-toplevel

    def test_speech_recogition(self):
        import sys
        from io import StringIO
        config = {'engine': {'name': 'text'}}
        controller = Controller(config)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            controller.engine.speak("test words")
            output = out.getvalue().strip()
            self.assertEqual('test words', output)
        finally:
            sys.stdout = saved_stdout
