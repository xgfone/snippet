import logging
import traceback
import falcon

LOG = logging.getLogger("gunicorn.error")


def _add_route(app, uri_template, resource, *args):
    if not app:
        app = globals()["application"]
    if callable(resource):
        method_map = {method.upper(): resource for method in args or ["GET"]}
        falcon.routing.set_default_responders(method_map)
        app._router.add_route(uri_template, method_map, resource)
    else:
        app.add_route(uri_template, resource)


def add_route(uri_template, resource, *args, app=None):
    _add_route(app or globals()["application"], uri_template, resource, *args)


def append_exception_handler(app, handler, exc=Exception):
    app._error_handlers.append((exc, handler))


def falcon_default_exception_handler(ex, req, resp, params):
    resp.content_type = falcon.MEDIA_TEXT
    resp.status = falcon.HTTP_500
    resp.body = str(ex)
    LOG.error("Get an exception: method=%s, url=%s, err=%s, traceback=\n%s",
              req.method, req.path, ex, traceback.format_exc())
