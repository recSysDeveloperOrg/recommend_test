# 用户系统架构文档
本次系统对于用户的功能处理比较简单，只需要处理传统的登录、注册、获取个人信息等功能即可

## 接口文档
```
message BaseResp {
    i64 errNo
    string errMsg
}

message User {
    string id
    string name
    string password
    string gender
}

message LoginReq {
    string username
    string password
}
message LoginResp {
    BaseResp baseResp
    string accessToken
    string refreshToken
}

message RegisterReq {
    User user
}
message RegisterResp {
    BaseResp baseResp
}

message QueryReq {
    string accessToken
    string refreshToken
}
message QueryResp {
    BaseResp baseResp
    User user
    string accessToken // only if refreshToken in QueryReq is set
}

service UserService {
    rpc login(LoginReq) returns (LoginResp) {}
    rpc register(RegisterReq) returns (RegisterResp) {}
    rpc query(QueryReq) returns (QueryResp) {}
}
```

## JWT简单介绍
用户登录/信息获取基于主要基于JWT模型构建，JWT Model如下：
```
{
    "accessToken": xxx,
    "refreshToken": xxx
}
```
其中accessToken是访问令牌，用户每一次访问系统功能模块都需要在请求头上带上accessToken信息，accessToken由三部分组成：
```
<accessToken start>
头部信息（包含令牌过期时间等与令牌相关的数据）
载荷信息（包括用户相关信息，例如用户uid，但是一定不能将重要的信息包含在载荷中）
签名信息（一般是先将头部和载荷进行base64编码，然后使用服务器私钥进行加密即可）
<accessToken end>
```
可以将accessToken的有效期相对设置比较短一些，在过期后利用refreshToken获取新的accessToken，如果refreshToken也过期了，那么就需要用户重新登录了。通常来说，accessToken不需要在服务端缓存任何信息，每次传入的时候进行校验与计算即可，根据载荷中的信息处理业务需求即可，refreshToken需要进行持久化存储。（其实不做refreshToken也没有什么问题）

## 系统功能介绍
1. 系统的任何页面都会上报日志，日志需要用户登录，这里靠前端传userId
2. 用户登录（UserService.login)，输入用户名&密码登录，登录后能够进入个人页面查看自己的历史电影点评记录和自己的标签云，电影模块和标签模块都需要向用户模块请求用户信息（UserService.query)
3. 允许新用户注册（UserService.register)，注册主要分为两个步骤，第一步填写必要的注册信息（用户名、密码、性别），第二步需要强制用户选取一些热门标签，作为推荐系统冷启动的参数，给新用户初步推荐电影

## 错误码约定
在登录响应中（LoginResp），可能会返回以下错误，格式为 errNo,errMsg
```
0,"成功"
1,"参数非法"
2,"用户不存在或者密码错误"
999,"系统发生未知错误"
```
在注册响应中（RegisterResp），可能会返回以下错误，格式为 errNo,errMsg
```
0,"成功"
1,"参数非法"
2,"用户名重复，请修改用户名"
3,"性别不正确，请修改性别"
999,"系统发生未知错误"
```
在查询响应中（QueryResp），可能会返回以下错误，格式为 errNo,errMsg
```
0,"成功"（如果是refreshToken成功了，需要从QueryResp中取得新的accessToken）
1,"参数非法"
2,"传入的token已经过期"
999,"系统发生未知错误"
```

##DB模型
项目准备使用MongoDB，这是一个文档类型的数据库，跟JSON格式非常类似
```
用户模型：
{
    _id:"xxx",
    name: "xxx",
    password: "xxx",
    gender: "xxx"
}
refresh_token:
{
    refreshToken: "xxx",
    userId:"xxx"
}
```