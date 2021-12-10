# 评分模块
## 接口设计
```
syntax = "proto3";
package rating;

option java_package = "com.ljygogogo.movie.rating";
option java_multiple_files = true;

message BaseResp {
  int64 errNo = 1;
  string errMsg = 2;
}
message Movie {
  string id = 1;
  string title = 2;
  string picUrl = 3;
  optional string introduction = 4;
  optional string participants = 5;
  optional string releaseDate = 6;
  optional string language = 7;
  optional int64 uniqueRatingCnt = 8;
  optional float averageRating = 9;
}
message RateRecord {
  Movie movie = 1;
  float rating = 2;
}

message RateReq {
  string movieId = 1;
  string userId = 2;
  float rating = 3;
}
message RateResp {
  BaseResp baseResp = 1;
}
message QueryRateRecordsReq {
  string userId = 1;
  int64 page = 2;
  int64 offset = 3;
}
message QueryRateRecordsResp {
  BaseResp baseResp = 1;
  repeated RateRecord records = 2;
  int64 nRecords = 3;
}

message QueryMovieRatingReq {
  string userId = 1;
  repeated string movieIdList = 2;
}
message QueryMovieRatingResp {
  map<string,float> movieId2PersonalRating = 1;
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

##DB模型
项目准备使用MongoDB，这是一个文档类型的数据库，跟JSON格式非常类似
```
{
    userId: "xxx",
    movieId: "xxx",
    rating: x.x
}
```