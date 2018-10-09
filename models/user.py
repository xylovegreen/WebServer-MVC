from models import Model
from utils import log
from models.user_role import UserRole


class User(Model):
    """
    User 是保存用户数据的 model
    继承了 Model
    从而继承 Model 的 save 和 new 方法
    """
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', UserRole.normal)

    def validate_login(self):
        users = User.all()
        log('all users in validation login', users)
        for user in users:
            if user.username == self.username:
                if user.password == self.password:
                    return True
        return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

    @classmethod
    def login_user(cls, form):
        u = User.find_by(username=form['username'], password=form['password'])
        return u

    @staticmethod
    def guest():
        form = dict(
            role=UserRole.guest,
            username='【游客】',
        )
        u = User(form)
        return u

    def is_admin(self):
        return self.role == UserRole.admin
