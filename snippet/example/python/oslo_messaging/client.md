# encoding: utf8

import oslo_messaging


class TestClient(object):
    def __init__(self, transport):
        target = oslo_messaging.Target(topic='test', version='2.0')
        self._client = oslo_messaging.RPCClient(transport, target)

    def test(self, ctxt, arg):
        #cctxt = self._client.prepare(version='2.5')
        return self._client.call(ctxt, 'test', arg=arg)


transport = oslo_messaging.get_transport(cfg.CONF)
target = oslo_messaging.Target(topic='test', version='2.0')

client = oslo_messaging.RPCClient(transport, target)
client.call(ctxt, 'test', arg=arg)

client = oslo_messaging.RPCClient(transport, target, retry=None)
try:
    client.prepare(retry=0).cast(ctxt, 'ping')
except oslo_messaging.MessageDeliveryFailure:
    LOG.error("Failed to send ping message")
