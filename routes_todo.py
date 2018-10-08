from models.todo import Todo
from routes import (
    current_user,
    template,
    response_with_headers,
    redirect,
)
from utils import log

import time


def formatted_time(unix_time):
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(unix_time)
    formatted = time.strftime(time_format, value)
    return formatted


def index(request):
    """
    todo 首页的路由函数
    """
    u = current_user(request)
    log('todo index', u)
    todo_list = Todo.find_all(user_id=u.id)
    # 生成一个 todo 项的 html 字符串
    todo_html = """
    <h3>
        {} : {}
        <a href="/todo/edit?id={}">编辑</a>
        <a href="/todo/delete?id={}">删除</a>
        创建 {}
        最近修改 {}
    </h3>
    """
    todo_html = ''.join([
        todo_html.format(
            t.id, t.title, t.id, t.id, formatted_time(t.created_time), formatted_time(t.updated_time),
        ) for t in todo_list
    ])

    # 替换模板文件中的标记字符串
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)

    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    u = current_user(request)

    t = Todo.new(form)
    t.user_id = u.id
    t.created_time = int(time.time())
    t.updated_time = t.created_time
    t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo')


def edit(request):
    todo_id = int(request.query['id'])
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    if u.id == t.user_id:
        body = template('todo_edit.html')
        body = body.replace('{{todo_id}}', str(todo_id))
        body = body.replace('{{todo_title}}', t.title)

    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def update(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    t = Todo.find_by(id=int(form['id']))
    u = current_user(request)

    if u.id == t.user_id:
        Todo.update(form)

    return redirect('/todo')


def route_dict():
    """
    todo的路由字典
    """
    d = {
        '/todo': index,
        '/todo/add': add,
        '/todo/edit': edit,
        '/todo/update': update,
        '/todo/delete': delete,
    }
    return d