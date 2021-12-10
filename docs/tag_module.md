# 标签模块架构
## 接口定义

```
syntax = "proto3";
package tag;

option java_package = "com.ljygogogo.movie.tag";
option java_multiple_files = true;

message BaseResp {
  int64 errNo = 1;
  string errMsg = 2;
}
message Tag {
  int64 id = 1;
  string content = 2;
  int64 updatedAt = 3;  // 对于用户来说，这是用户最后一次使用这个tag的时间，对于电影来说，这是电影最后一次被打这个tag的时间
  int64 nTimes = 4; // 对于用户来说，这是用户使用这个tag的次数，对于电影来说，这是电影被打上这个tag的次数
}

message CreateTagReq {
  string userId = 1;
  string movieId = 2;
  string tagContent = 3;
}
message CreateTagResp {
  BaseResp baseResp = 1;
}

message QueryMovieTagReq {
  string userId = 1;
  string movieId = 2;
}
message QueryMovieTagResp {
  BaseResp baseResp = 1;
  repeated Tag tags = 2;
}

message QueryUserTagCloudReq {
  string userId = 1;
  int64 nTags = 2;   // 查询k大频率的tag
}
message QueryUserTagCloudResp {
  BaseResp baseResp = 1;
  repeated Tag tags = 2;
}

message QueryTagRecordsReq {
  string userId = 1;
  int64 page = 2;
  int64 offset = 3;
}
message QueryTagRecordsResp {
  BaseResp baseResp = 1;
  repeated Tag tags = 2;
  int64 nRecords = 3;
}

message QueryMovieTopNTagsReq {
  string movieId = 1;
  int64 nTags = 2;
}
message QueryMovieTopNTagsResp {
  BaseResp baseResp = 1;
  repeated Tag tags = 2;
}

service TagService {
  rpc createTag(CreateTagReq) returns (CreateTagResp) {}
  rpc queryMovieTag(QueryMovieTagReq) returns (QueryMovieTagResp) {}
  rpc queryUserTagCloud(QueryUserTagCloudReq) returns (QueryUserTagCloudResp) {}
  rpc queryTagRecords(QueryTagRecordsReq) returns (QueryTagRecordsResp) {}
  rpc queryMovieTopNTags(QueryMovieTopNTagsReq) returns (QueryMovieTopNTagsResp) {}
}
```

## 功能简介
1. 用户可以在电影详情页面创建新的(createTag)&修改(createTag)&查看自己的Tag(queryMovieTag)
2. 用户可以在个人页面查看自己的标签云（也就是根据标签次数排序）(queryUserTagCloud)
3. 用户可以在个人页面查看历史标签记录（可以考虑和历史评分记录放在一起作为历史记录）(queryTagRecords)
4. 用户在新建tag时会获取最近创建的K个tag，方便通过点击填入(queryTagRecords)
5. 电影详情页面会展示这个电影被打的最多的N个tag(queryMovieTopNTags)

## 错误码约定（xxxResp.baseResp.errNo）
这六个rpc口的resp统一错误码如下：
```
0,"成功"
1,"参数非法"
999,"系统未知错误"
```

##DB模型
项目准备使用MongoDB，这是一个文档类型的数据库，跟JSON格式非常类似
```
tag:
{
    _id:"xxx",
    content:"xxx"
}
用户打的tag：
{
    _id:"xxx",
    userId: "xxx",
    movieId: "xxx",
    tagId: "xxx",
    updatedAt: xxx, // 用户最后一次使用这个Tag的时间
    useTimes: 666,   // 用户打这个tag的次数
}
电影tag：
{
    _id:"xxx",
    movieId: "xxx",
    tagId: "xxx",
    updatedAt: xxx, // 这个电影最近一次被打这个tag的时间
    taggedTimes: 666    // 表示这个电影被打这个tag的次数
}
```