import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado.web import RequestHandler

define("port", default=8000, help="run on the giver port", type=int)


class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class InfoPageHandler(RequestHandler):
    def post(self):
        name = self.get_argument('name')
        age = self.get_argument('age')
        username = self.get_argument('username')
        password = self.get_argument('password')
        self.render('info.html', name=name, age=age, username=username, password=password)


class RegisterHandler(RequestHandler):

    def get(self):
        self.render('register.html')

    def post(self):
        if self.check_arguement():
            username = self.get_argument('username')
            password1 = self.get_argument('password1')
            password2 = self.get_argument('password2')
            if username and password1 and (password1 == password2):
                pass
            else:
                self.render('register.html', error='注册失败')
        else:
            self.render('register.html', error='输入错误')

    def check_arguement(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if len(username) < 10 and len(password) < 10:
            return True
        else:
            return False

    def create_user(self):
        pass


class LoginHandler(RegisterHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        # 验证


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/info', InfoPageHandler),
            (r'/register', RegisterHandler),
            (r'/login', LoginHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


