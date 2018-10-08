from models import Model
import time


class Todo(Model):
    """
    继承自 Model 的 Todo 类
    """

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time', -1)
        self.updated_time = form.get('updated_time', -1)

    @classmethod
    def update(cls, form):
        todo_id = int(form['id'])
        t = Todo.find_by(id=todo_id)
        t.title = form['title']
        t.updated_time = int(time.time())
        t.save()