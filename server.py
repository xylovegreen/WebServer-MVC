import socket
import _thread
import urllib.parse
from utils import log

from routes import route_dict
from routes import error
from routes_todo import route_dict as routes_todo


class Request(object):
    """
     Request 类，临时保存接收到的请求
     得到 header 和 body
     得到 method, headers, path, query, form
    """
    def __init__(self, raw_data):
        # 只能 split 一次，因为 body 中可能有换行
        header, self.body = raw_data.split('\r\n\r\n', 1)
        h = header.split('\r\n')

        parts = h[0].split()
        self.method = parts[0]
        path = parts[1]
        self.path = ""
        self.query = {}
        self.parse_path(path)
        log('Request: path 和 query', self.path, self.query)

        self.headers = {}
        self.cookies = {}
        self.add_headers(h[1:])
        log('Request: headers 和 cookies', self.headers, self.cookies)

    def add_headers(self, header):
        """
        Cookie: user=xylov
        """
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v

        if 'Cookie' in self.headers:
            cookies = self.headers['Cookie']
            k, v = cookies.split('=')
            self.cookies[k] = v

    def form(self):
        body = urllib.parse.unquote_plus(self.body)
        log('form', self.body)
        log('form', body)
        args = body.split('&')
        f = {}
        log('args', args)
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        log('form() 字典', f)
        return f

    def parse_path(self, path):
        """
        输入: /xxx?aaa=bbb&ccc=ddd
        返回
        (xxx, {
            'aaa': 'bbb',
            'ccc': 'ddd',
        })
        """
        index = path.find('?')
        if index == -1:
            self.path = path
            self.query = {}
        else:
            path, query_string = path.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            self.path = path
            self.query = query


def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {}
    r.update(route_dict())
    r.update(routes_todo())

    response = r.get(request.path, error)

    return response(request)


def process_request(connection):
    with connection:
        r = connection.recv(1024)
        log('request: \n{}'.format(r.decode()))

        raw_data = r.decode()
        request = Request(raw_data)
        response = response_for_path(request)

        connection.sendall(response)


def run(host='127.0.0.1', port=3000):
    """
    启动服务器
    """
    # 初始化 socket
    # 使用 with 保证程序中断时能正确关闭 socket 释放占用端口
    with socket.socket() as s:
        # 绑定
        s.bind((host, port))
        # 监听
        s.listen()

        # 用无限循环来处理请求
        while True:
            # 接受
            connection, address = s.accept()
            log('ip: {}'.format(address))
            # 开启新线程处理请求
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    run()