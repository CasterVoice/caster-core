import gevent.queue

from castervoice.core.controller import Controller

consumer_queues = []


class RecognitionEvent:

    def __init__(self, plugin_name, words, rule, node):
        self.plugin_name = plugin_name
        self.words = words
        self.rule = rule
        self.node = node


def new_queue():
    queue = gevent.queue.Queue()
    consumer_queues.append(queue)
    return queue


def on_recognition(words, rule, node):
    plugin_name = None
    for plugin_name, plugin in Controller.get().plugin_manager.plugins.items():
        if rule.grammar in plugin.grammars:
            break

    # It would be odd recognizing a rule which is not present in
    # any plugin's grammar
    assert plugin_name

    recognition_event = RecognitionEvent(plugin_name, words, rule, node)
    for queue in consumer_queues:
        queue.put_nowait(recognition_event)


def on_begin():
    print("Speech start detected.")


def on_failure():
    print("Sorry, what was that?")


def log():
    queue = new_queue()
    while True:
        reco = queue.get()
        print("Recognized: %s" % " ".join(reco.words))
        print("    Executing rule: %s" % (reco.rule))
        print("    Action: %s" % (reco.node.value()))


def stream_recognitions():
    queue = new_queue()

    while True:
        reco = queue.get()
        s = "%s: %s" % (reco.plugin_name, " ".join(reco.words))
        yield "data: %s\n\n" % s
