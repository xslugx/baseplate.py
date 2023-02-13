import unittest

from importlib import reload

import gevent.monkey

from baseplate.lib.message_queue import create_queue
from baseplate.lib.message_queue import MessageQueue
from baseplate.lib.message_queue import QueueType
from baseplate.sidecars import publisher_queue_utils


class GeventPatchedTestCase(unittest.TestCase):
    def setUp(self):
        gevent.monkey.patch_socket()

    def tearDown(self):
        import socket

        reload(socket)
        gevent.monkey.saved.clear()


class PublisherQueueUtilTests(GeventPatchedTestCase):
    def test_posix_queue_get_put(self):
        queue: MessageQueue = create_queue(QueueType.POSIX, "/test", 5, 1000)

        test_message = bytes("message", "utf-8")
        test_message_2 = bytes("2nd message", "utf-8")
        queue.put(test_message)
        queue.put(test_message_2)
        output = queue.get()
        assert output == test_message
        output = queue.get()
        assert output == test_message_2

    def test_in_memory_queue_get_put(self):
        with publisher_queue_utils.start_queue_server(host="127.0.0.1", port=9090):
            queue: MessageQueue = create_queue(QueueType.IN_MEMORY, "/test", 5, 1000)

            test_message = bytes("message", "utf-8")
            test_message_2 = bytes("2nd message", "utf-8")
            queue.put(test_message)
            queue.put(test_message_2)
            output = queue.get()
            assert output == test_message
            output = queue.get()
            assert output == test_message_2

    def test_in_memory_queue_alternate_port(self):
        with publisher_queue_utils.start_queue_server(host="127.0.0.1", port=9091):
            queue: MessageQueue = create_queue(QueueType.IN_MEMORY, "/test", 5, 1000, port=9091)

            test_message = bytes("message", "utf-8")
            test_message_2 = bytes("2nd message", "utf-8")
            queue.put(test_message)
            queue.put(test_message_2)
            output = queue.get()
            assert output == test_message
            output = queue.get()
            assert output == test_message_2
