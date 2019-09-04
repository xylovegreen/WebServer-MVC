## WebServer-MVC
基于 Socket 和 HTTP 协议编写的 Web MVC 框架，并实现一个 TodoList 功能的应用。

## 效果图
![](WebServer-MVC.gif)

## 实现功能
- user 登录 和 注册
- todo 增删改查(CRUD)
- todo 和 user 数据关联
- admin 角色 对用户数据进行修改

## 项目架构
### 数据模型(Model)
1. 实现 Model 基类，存储数据 user, todo, session
2. 实现 数据 CRUD 方法
3. 用 JSON 格式存储数据

### 路由处理(Controller)
1. 抽象 Request 类对请求进行解析
2. 实现 路由字典映射，绑定路径到路由处理函数
3. 实现 调用 CRUD 接口处理数据


### 模板试图(View)
1. 包含所有 static 文件
2. 实现 html 模板
3. 实现 变量替换 展示数据


