from models import User


def test_save():
    # 数据清理
    with open(User.db_path(), 'w') as f:
        f.write('[]')

    # 数据准备
    form = dict(
        username='xylov',
        password='123',
    )

    # 测试 id 赋值
    for i in range(1, 5):
        form['username'] = 'xylov{}'.format(i)
        u = User.new(form)
        u.save()
        assert u.id == i

    # 测试保存的数据
    for i, u in enumerate(User.all()):
        assert u.id == i + 1

    # 测试更新数据
    u = User.find_by(username='xylov1')
    u.password = '123456'
    u.save()
    assert u.password == '123456'