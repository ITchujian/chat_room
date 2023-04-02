# 即时聊天室-面向对象

## 项目简介
一款基于UDP协议使用Python开发的即时聊天室，包含客户端与服务端
A development based on UDP protocol USES Python instant chat rooms, including client and server

## 项目环境
基于Linux Mint下的Pycharm开发

## 主要技术
- UDP套接字
- 多进程技术
- 面向对象思想

## 网络协议
- “join#username”: 客户端向服务端发送此协议以加入聊天室，其中"username"为客户端指定的用户名。
- “duplicated”: 服务端向客户端发送此协议，表示该客户端指定的用户名已经被其他客户端占用，加入聊天室失败。
- “to_join”:服务端向客户端发送此协议，表示客户端成功加入聊天室。
- “to_join_admin”:服务端向管理员客户端发送此协议，表示管理员身份验证成功，成功加入聊天室。
- “quit#username”:客户端向服务端发送此协议以退出聊天室，其中"username"为客户端的用户名。
- “quit#admin”:管理员客户端向服务端发送此协议以退出聊天室。
- “{datetime.now().strftime(‘%Y-%m-%d %H:%M:%S’)} > {data.decode(‘utf-8’).split(‘#’)[0]} {data.decode(‘utf-8’).split(': ')[1]}”:服务端向所有客户端广播消息时，如果是管理员发送的指令，会采用此格式输出。
- “remove#name”: 管理员客户端向服务端发送此协议以移除指定的成员，其中"name"为要移除的成员的用户名。
- “remove@you”: 服务端向被移除的客户端发送此协议，表示该客户端已经被管理员移除聊天室。
- “name#name”:管理员客户端向服务端发送此协议以查询指定成员的IP地址和端口号，其中"name"为要查询的成员的用户名。服务端将查询结果返回给管理员客户端。

## 代码相关博客
· CSDN深度递增-[基于UDP协议与多进程开发的即时聊天室](https://blog.csdn.net/weixin_46231858/article/details/129889492)
