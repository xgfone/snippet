# encoding: utf-8
import urlparse


class URL(object):
    DEFAULT_SCHEME = ["http", "https"]

    def __init__(self, url, allowed_scheme=None):
        self._url = url
        self.url = urlparse.urlparse(self._url)
        self._scheme = allowed_scheme if allowed_scheme else self.DEFAULT_SCHEME

    def geturl(self):
        scheme = self.scheme if self.scheme else self.url.scheme
        netloc = self.netloc if self.netloc else self.url.netloc
        url = self.path if self.path else self.url.path
        params = self.params if self.params else self.url.params
        query = self.query if self.query else self.url.query
        fragment = self.fragment if self.fragment else self.url.fragment

        if params:
            url = "%s;%s" % (url, params)
        return urlparse.urlunsplit((scheme, netloc, url, query, fragment))

    def get_full_url(self, base=None):
        return self.s_get_full_url(self, base)

    @staticmethod
    def s_get_full_url(url, base=None):
        if not base:
            if url.scheme in url._scheme:
                return url.geturl()
            return None

        if not url.scheme:
            url.scheme = base.scheme
        if url.scheme not in url._scheme:
            return None
        if not url.netloc:
            url.netloc = base.netloc
        if len(url.path) == 1 and url.path == '/':
            return None
        if url.path[0] != '/':
            path = base.path.split('/')[:-1]
            path.append(url.path)
            url.path = '/'.join(path)

        return url.geturl()

    def __getattr__(self, name):
        if name == "path":
            path = getattr(self.url, name)
            if not path:
                return '/'
            return path
        return getattr(self.url, name)

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def __repr__(self):
        s = "URL(scheme='%s', netloc='%s', path='%s', params='%s', query='%s', fragment='%s')"
        p = (self.scheme, self.netloc, self.path, self.params, self.query, self.fragment)
        return s % p
