
```python
from oslo_config import cfg
import oslo_messaging
import time


class ServerControlEndpoint(object):
    # `target` is used to match the endpoint to handle the message.
    # Only the namespace and the version of the message match that of this `target`,
    # this `Endpoint` handle the message.
    # Generally, please set the attribution.
    target = oslo_messaging.Target(namespace='control',
                                   version='2.0')

    def __init__(self, server):
        self.server = server

    def stop(self, ctx):
        if self.server:
            self.server.stop()


class TestEndpoint(object):
    # If no the attribution, `target`, the default is
    # Target(exchange=None, topic=None, namespace=None, version=None,
    #        server=None, fanout=None, legacy_namespaces=None)

    def test(self, ctx, arg):
        return arg


# `Transport` is the capsulation of the Message Queue, such as RabbitMQ.
# If no @url, it will use `CONF.transport_url`.
# the specification of `url` is "transport://user:pass@host1:port[,hostN:portN]/virtual_host"
#transport = oslo_messaging.get_transport(cfg.CONF, url="rabbit://me:passwd@host:5672/virtual_host")
transport = oslo_messaging.get_transport(cfg.CONF)

# This is used to create the exchange, the message queue, for example, the message queue based on topic, fanout, or direct.
# It'll create two the topic message queue, whose routing_keys are "test" and "test.server1", and one the fanout queue, whose routing_key is "test".
target = oslo_messaging.Target(topic='test', server='server1')

endpoints = [
    ServerControlEndpoint(None),
    TestEndpoint(),
]
server = oslo_messaging.get_rpc_server(transport, target, endpoints,
                                       executor='blocking')
try:
    server.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping server")

server.stop()
server.wait()
```
