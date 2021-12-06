# 评分模块
## 接口设计
```
message BaseResp {
    i64 errNo
    string errMsg
}
message Movie {
    string id
    string title
    string picUrl
    optional string introduction
    optional string participants
    optional string releaseDate
    optional string language
}
message RateRecord {
    Movie movie
    i64 rating
}

message RateReq {
    string movieId
    i64 rating
}
message RateResp {
    BaseResp baseResp
}
message QueryRateRecordsReq {
    i64 page
    i64 offset
}
message QueryRateRecordsResp {
    BaseResp baseResp
    repeated RateRecord records
    i64 nRecords
}

message QueryMovieRatingReq {
    repeated string movieIdList
}
message QueryMovieRatingResp {
    map<string,i64> movieId2PersonalRating
    map<string,i64> movieId2AverageRating
}

service RatingService {
    rpc rateMovie(RateReq) returns (RateResp) {}
    rpc queryRateRecords(QueryRateRecordsReq) returns (QueryRateRecordsResp) {}
    rpc batchQueryMovieRating(QueryMovieRatingReq) returns (QueryMovieRatingResp) {}
}
```

## 功能说明
1. 电影详情页面需要展示该电影的平均得分&用户给该电影的打分（RatingService.batchQueryMovieRating）
2. 用户可以在电影详情页面给这个电影打分（RatingService.rateMovie）
3. 用户可以在个人详情页面查看历史评分记录（可以考虑和历史tag记录放在一起）（RatingService.queryRateRecords）

## 错误码约定（xxxResp.baseResp.errNo）
RateResp:
```
0,"成功"
1,"参数非法"
2,"用户未登录"
999,"系统未知错误"
```
QueryRateRecordsResp:
```
0,"成功"
1,"参数非法"
2,"用户未登录"
999,"系统未知错误"
```
QueryMovieRatingResp:
```
0,"成功"
1,"参数非法"
2,"用户未登录"
999,"系统未知错误"
```