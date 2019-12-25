import http.server
import functools
import re


def make_handler_class_from_function_map(path_to_function_map):
    class HTTPServerHandler(http.server.BaseHTTPRequestHandler):

        def _init__(self, *args, **kwargs):
            super(HTTPServerHandler, self).__init__(*args, **kwargs)

        def do_GET(self):
            requested_path = self.path
            response = 0
            body = ''
            if "favicon.ico" in requested_path:
                return
            if requested_path in path_to_function_map:
                response, body = path_to_function_map[requested_path]()
            else:
                for path in path_to_function_map:
                    exact_pattern = f"^{path}$"
                    if matched := re.search(exact_pattern, requested_path):
                        response, body = path_to_function_map[path](*matched.groups())
                        break
            if not (response and body):
                response = 404
                body = ""
            self.send_response(response)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return

    return HTTPServerHandler


class Website:

    def __init__(self):
        self.path_to_function_map = {}

    def route(self, path):
        def decorator(f):
            self.path_to_function_map[path] = f
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper
        return decorator

    def run(self, address):
        handler = make_handler_class_from_function_map(self.path_to_function_map)
        try:
            httpd = http.server.HTTPServer(address, handler)
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.socket.close()
