import socket
import _thread


def log(*args, **kwargs):
    """
    log 替代 print
    """
    print('log', *args, **kwargs)


def process_request(connection):
    r = connection.recv(1024)
    log('request: \n{}'.format(r.decode()))

    response = b'HTTP/1.1 200 OK\r\n\r\n<h1>Hello, World!</h1>'
    connection.sendall(response)
    connection.close()


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