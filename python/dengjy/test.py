# encoding: utf-8
import hashlib
import random
import string
import time
from cgi import parse_qs
from typing import Iterable, Union
# 导入wsgi包
from wsgiref.simple_server import make_server
from jinja2 import Template
ADDRESS = '127.0.0.1'
PORT = 8080
USERNAME = 'joe'
PASSWORD = '123456'
SESSION_COOKIE_NAME = 'sessionid'
# 存内存，生产环境勿用
SESSION = {}


class Session:
    __slots__ = ('session_key', 'session_data')

    def __init__(self):
        self.session_key = self.generate_session_key()
        self.session_data = {}

        SESSION[self.session_key] = self

    def generate_session_key(self, length=32,
                             allowed_chars='abcdefghijklmnopqrstuvwxyz'
                             'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        allowed_chars = string.ascii_lowercase + string.digits
        SECRET_KEY = 'qewffwfzad3esla;ss'
        random.seed(
            hashlib.sha256(
                ('%s%s%s' % (random.getstate(), time.time(), SECRET_KEY)).encode()
            ).digest()
        )
        return ''.join(random.choice(allowed_chars) for i in range(length))

    def __setitem__(self, key, value):
        self.session_data[key] = value

    def __getitem__(self, key):
        return self.session_data.get(key)


class Application:
    __slots__ = ('name', 'headers', 'routes', 'environ', 'start_response')

    def __init__(self, environ: dict, start_response: callable):
        self.name = 'miniweb'
        self.headers = [('server', self.name)]
        self.routes = {}
        self.environ = environ
        self.start_response = start_response

        # 添加路由规则
        self.add_route('/', self.index_handler)
        self.add_route('/login', self.login_handler)
        self.add_route('/logout', self.logout_handler)

    def add_route(self, url: str, handler: callable):
        self.routes[url] = handler

    @property
    def is_authenticated(self) -> bool:
        try:
            if self.session['user'] == USERNAME:
                return True
        except KeyError:
            return False
        return False

    @property
    def session(self):
        session_id = self.cookies.get(SESSION_COOKIE_NAME)
        if session_id:
            return SESSION.get(session_id, {})
        else:
            return {}

    @property
    def cookies(self):
        cookie = self.environ.get('HTTP_COOKIE', '')
        if not cookie:
            return {}
        parsed_cookie = {}
        for item in cookie.split('; '):
            k, v = item.split('=')
            parsed_cookie[k] = v
        return parsed_cookie

    def login_handler(self) -> Union[str, Iterable]:
        """登入"""
        if self.is_authenticated:
            return self.redirect('/')

        if self.request_method == 'GET':
            path = 'miniweb/login.html'
            kwargs = {'is_authenticated': self.is_authenticated}
            return self.render(path, **kwargs)
        else:
            # POST
            body = self.request_body
            if body['name'][0] == USERNAME and body['password'][0] == PASSWORD:
                session = Session()
                session['user'] = USERNAME
                # 关闭浏览器失效
                self.headers += [('Set-Cookie',
                                  f'{SESSION_COOKIE_NAME}={session.session_key}; httpOnly')]
                return self.redirect('/')
            else:
                return self.redirect('/login')

    def redirect(self, url: str) -> Iterable:
        status_code = '302 Found'
        self.headers += [('Location', url)]
        self.start_response(status_code, self.headers)
        yield b''

    def render(self, template_path, **kwargs) -> str:
        self.headers += [('Content-type', 'text/html')]
        with open(template_path, 'r') as f:
            template = Template(f.read())
            output = template.render(**kwargs)

        return output

    def logout_handler(self) -> Union[str, Iterable]:
        """登出"""
        sessionid = self.session.session_key
        del SESSION[sessionid]
        return self.redirect('/')

    def index_handler(self) -> Union[str, Iterable]:
        """首页"""
        if self.is_authenticated:
            return 'Hello ' + self.session['user']
        else:
            return self.redirect('/login')

    @property
    def request_method(self) -> str:
        return self.environ['REQUEST_METHOD']

    @property
    def request_path(self) -> str:
        return self.environ['PATH_INFO']

    @property
    def request_body(self) -> dict:
        try:
            request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = self.environ['wsgi.input'].read(request_body_size)
        return parse_qs(request_body.decode())

    def error_404(self) -> Iterable:
        """404处理函数"""
        status_code = '404 Not Found'
        self.start_response(status_code, self.headers)
        yield b'404 Not Found'

    def error_405(self) -> Iterable:
        """405处理函数"""
        status_code = '405 Method Not Allowed'
        self.start_response(status_code, self.headers)
        yield b'405 Method Not Allowed'

    def handle(self) -> Iterable:
        # 仅支持GET, POST方法
        if self.request_method not in ['GET', 'POST']:
            yield from self.error_405()
        if self.request_path in self.routes:
            handler = self.routes[self.request_path]
            response = handler()
            if isinstance(response, str):
                status_code = '200 OK'
                self.start_response(status_code, self.headers)
                yield response.encode()
            else:
                yield from response
        else:
            yield from self.error_404()

    def __iter__(self) -> Iterable:
        return self.handle()


if __name__ == '__main__':
    httpd = make_server(ADDRESS, PORT, Application)
    print(f'Listening on http://{ADDRESS}:{PORT} ...')
    httpd.serve_forever()
