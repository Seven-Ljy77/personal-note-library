下面是一份适合你当前阶段的“学习笔记库”项目需求。先完成必做部分，再做选做；不要一开始加入 Cookie、Refresh Token、Docker。

# 项目：个人学习笔记库

技术栈：

```text
后端：FastAPI + PostgreSQL + SQLAlchemy ORM + Alembic + JWT
前端：原生 HTML + CSS + JavaScript
```

目标：用户注册登录后，只能管理自己的学习笔记。

## 一、数据表

### users

```text
id
username             唯一
email                唯一
hashed_password
is_active            默认 true
created_at
```

### notes

```text
id
title                1～100 字
content              1～10000 字
tags                 可为空，例如 “Python,FastAPI”
is_pinned            默认 false
owner_id             外键，指向 users.id
created_at
updated_at
```

`owner_id` 不能由前端传入，必须由后端通过 JWT 得到当前用户 ID 后填写。

## 二、必做后端接口

| 方法 | 路径 | 是否登录 | 作用 |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | 否 | 注册 |
| `POST` | `/auth/login` | 否 | 登录并返回 Access Token |
| `GET` | `/users/me` | 是 | 获取当前用户信息 |
| `POST` | `/notes` | 是 | 创建自己的笔记 |
| `GET` | `/notes` | 是 | 获取自己的笔记列表 |
| `GET` | `/notes/{note_id}` | 是 | 获取自己的一条笔记 |
| `PATCH` | `/notes/{note_id}` | 是 | 修改自己的一条笔记 |
| `DELETE` | `/notes/{note_id}` | 是 | 删除自己的一条笔记 |

## 三、JWT 要求

登录成功响应：

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

Access Token payload 至少包含：

```json
{
  "sub": "用户 ID",
  "exp": "过期时间"
}
```

所有笔记接口必须要求：

```http
Authorization: Bearer <access_token>
```

实现一个依赖：

```python
get_current_user()
```

它负责：

```text
读取 Authorization 请求头
→ 验证 JWT 签名和 exp
→ 取得 sub
→ 查询数据库用户
→ 返回当前 User 对象
```

## 四、最重要的授权要求

以下写法是错误的：

```python
note = db.get(Note, note_id)
note.title = data.title
```

因为任何登录用户只要猜到 ID，就可能修改别人笔记。

正确逻辑必须同时检查：

```python
Note.id == note_id
Note.owner_id == current_user.id
```

如果查不到，返回：

```text
404：笔记不存在，或不属于当前用户
```

不要向普通用户暴露“这条笔记存在，但属于别人”的信息。

## 五、PATCH 要求

更新请求模型：

```json
{
  "title": "新的标题",
  "content": "新的内容",
  "tags": "Python,JWT",
  "is_pinned": true
}
```

这些字段都应可选。只更新前端实际传入的字段：

```python
updates = payload.model_dump(exclude_unset=True)
```

不能用下面这种方式判断布尔值：

```python
if payload.is_pinned:
    ...
```

因为 `false` 也是合法的新值。

## 六、列表接口要求

`GET /notes` 默认规则：

```text
先显示置顶笔记
→ 再按更新时间倒序
```

可选支持查询参数：

```text
GET /notes?keyword=jwt
GET /notes?tag=Python
GET /notes?completed=false
```

本项目没有 `completed` 字段，因此最后一个不必做；这是提醒你不要照搬需求，要以表结构为准。

## 七、前端最低要求

至少做两个页面：

```text
login.html
notes.html
```

### login.html

```text
注册入口
用户名/邮箱/密码登录表单
登录成功后保存 Access Token
跳转到 notes.html
```

### notes.html

```text
未登录时跳回登录页
创建笔记表单
笔记列表
编辑按钮
删除按钮
置顶开关
退出登录按钮
```

所有受保护请求都统一通过一个函数发送：

```js
async function apiFetch(path, options = {}) {
  // 自动加入 Authorization: Bearer <token>
}
```

退出时：

```js
localStorage.removeItem("access_token");
window.location.href = "./login.html";
```

学习项目可以先使用 `localStorage`；之后学习 Cookie/Session 时，再将方案改造为更安全的形式。

## 八、必须亲自测试的场景

```text
[ ] 注册成功，数据库不是明文密码
[ ] 重复用户名或邮箱返回 409
[ ] 正确密码登录成功
[ ] 错误密码返回 401
[ ] 没带 Token 请求 /notes 被拒绝
[ ] 伪造 Token 被拒绝
[ ] Token 过期被拒绝
[ ] 用户 A 看不到用户 B 的笔记
[ ] 用户 A 不能修改或删除用户 B 的笔记
[ ] title 为空时返回 422
[ ] PATCH 可将 is_pinned 从 true 改为 false
[ ] 退出后前端无法继续访问笔记页
```

## 九、选做功能

完成必做后，再按顺序增加：

```text
1. Refresh Token + /auth/refresh + /auth/logout
2. 标签表，改为多对多关系
3. 笔记搜索与分页
4. 管理员查看全部用户和笔记
5. pytest + TestClient 自动化测试
6. Docker Compose 部署
7. 用 Vue 3 重写前端
```

完成这个项目时，最重要的不是页面好看，而是你能自己解释：

```text
当前用户是谁？
这个用户是否拥有该笔记？
前端 Token 放在哪里？
后端为什么不能相信前端传来的 owner_id？
为什么 PATCH 要使用 exclude_unset=True？
```