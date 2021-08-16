import json
import logging

from .error import InvalidFileException
from flask import Flask
from flask import Response


logger = logging.getLogger()


def create_route_method(url):
    def m():
        response = Response(url.content, mimetype=url.content_type,
            status=url.status)

        response.headers['Content-type'] = url.content_type
        for h in url.headers:
            response.headers[h.name] = h.value

        return response
    return m


def build_server(server):
    app = Flask(server.server_name)

    for url in server.urls:
        logger.debug(f'adding pattern {url.pattern}')

        app.add_url_rule(url.pattern, view_func=create_route_method(url),
            endpoint=url.pattern, methods=url.method_list)
    return app


class Header(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Url(object):
    def __init__(self, pattern, status, content, content_file, content_type,
            headers, method_list):
        if content is None and content_file is None:
            raise Exception('urls need content or content_file defined')

        self.content = content
        if content_file is not None:
            with open(content_file) as f:
                self.content = f.read()

        self.method_list = method_list
        self.pattern = pattern
        self.status = status
        self.content_type = content_type
        self.headers = [Header(h[0], h[1]) for h in headers]


class Server(object):
    def __init__(self, server_name):
        self.urls = []
        self.server_name = server_name

    def add_url(self, url: Url):
        self.urls.append(url)

    def build(self):
        self.app = build_server(self)
        return self.app

    def start(self, debug, host, port):
        app = self.build()
        app.run(host=host, port=port, debug=debug)


def parse_file(file_path):
    try:
        with open(file_path) as f:
            data = json.loads(f.read())
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        raise InvalidFileException()

    server = Server(server_name=data['server_name'])
    used_pattern = []

    for url_data in data['urls']:
        pattern = url_data['pattern']

        if pattern in used_pattern:
            logger.warning(f'ignoring pattern {pattern}')
            continue
        used_pattern.append(pattern)

        url = Url(pattern=url_data['pattern'],
            status=url_data.get('status', 200),
            method_list=url_data.get('method_list', ['GET']),
            content=url_data.get('content'),
            content_file=url_data.get('content_file'),
            content_type=url_data.get('content_type', 'application/json'),
            headers=url_data.get('headers', []))
        server.add_url(url)
    return server
