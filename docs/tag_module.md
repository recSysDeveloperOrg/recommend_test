# 标签模块架构
## 接口定义

```
message BaseResp {
    i64 errNo
    string errMsg
}
message Tag {
    i64 id
    string content
    datetime createdAt
}

message CreateTagReq {
    string movieId
    string tagContent
}
message CreateTagResp {
    BaseResp baseResp
}

message QueryMovieTagReq {
    string movieId
}
message QueryMovieTagResp {
    BaseResp baseResp
    repeated Tag tags
}

message QueryUserTagCloudReq {
    i64 nTags   // 查询k大频率的tag
}
message QueryUserTagCloudResp {
    BaseResp baseResp
    repeated Tag tags
}

message QueryTagRecordsReq {
    i64 page
    i64 offset
}
message QueryTagRecordsResp {
    BaseResp baseResp
    repeated Tag tags
    i64 nRecords
}

message QueryRecentTagsReq {
    i64 nTags
}
message QueryRecentTagsResp {
    BaseResp baseResp
    repeated Tag tags   // 这里会确保返回的时候按照时间倒序
}

message QueryMovieTopNTagsReq {
    string movieId
    i64 nTags
}
message QueryMovieTopNTagsResp {
    BaseResp baseResp
    repeated Tag tags
}

service TagService {
    rpc createTag(CreateTagReq) returns (CreateTagResp) {} (接口幂等)
    rpc queryMovieTag(QueryMovieTagReq) returns (QueryMovieTagResp) {}
    rpc queryUserTagCloud(QueryUserTagCloudReq) returns (QueryUserTagCloudResp) {}
    rpc queryTagRecords(QueryTagRecordsReq) returns (QueryTagRecordsResp) {}
    rpc queryRecentTags(QueryRecentTagsReq) returns (QueryRecentTagsResp) {}
    rpc queryMovieTopNTags(QueryMovieTopNTagsReq) returns (QueryMovieTopNTagsResp) {}
}
```

## 功能简介
1. 用户可以在电影详情页面创建新的(createTag)&修改(createTag)&查看自己的Tag(queryMovieTag)
2. 用户可以在个人页面查看自己的标签云（也就是根据标签次数排序）(queryUserTagCloud)
3. 用户可以在个人页面查看历史标签记录（可以考虑和历史评分记录放在一起作为历史记录）(queryTagRecords)
4. 用户在新建tag时会获取最近创建的K个tag，方便通过点击填入(queryRecentTags)
5. 电影详情页面会展示这个电影被打的最多的N个tag(queryMovieTopNTags)

## 错误码约定（xxxResp.baseResp.errNo）
这六个rpc口的resp统一错误码如下：
```
0,"成功"
1,"参数非法"
2,"用户未登录"
999,"系统未知错误"
```