# 电影模块架构
## 接口设计

```
message BaseResp {
    i64 errNo
    string errMsg
}
// 这里后面可以考虑加上推荐的原因
message Movie {
    string id
    string title
    string picUrl
    optional string introduction
    optional string participants
    optional string releaseDate
    optional string language
}

message RecommendReq {
    i64 page
    i64 offset    
}
message RecommendResp {
    BaseResp baseResp
    repeated Movie movies
    i64 nRecommend // 系统总的推荐数量, 用于判定是否有下一页
}

message MovieDetailReq {
    string id
}
message MovieDetailResp {
    BaseResp baseResp
    Movie movie
}

message SearchReq {
    string keyword
    i64 page
    i64 offset
}
message SearchResp {
    BaseResp baseResp
    repeated Movie movies
    i64 nSearch // 搜索结果总数, 用于判定是否有下一页
}

message CreateReq {
    Movie movie
}
message CreateResp {
    BaseResp baseResp
}

service MovieService {
    rpc recommendMovies(RecommendReq) returns (RecommendResp) {}
    rpc getMovieDetail(MovieDetailReq) returns (MovieDetailResp) {}
    rpc searchMovies(SearchReq) returns (SearchResp) {}
    rpc createMovie(CreateReq) returns (CreateResp) {}
}
```

## 功能说明
1. 首页需要个性化推荐用户可能感兴趣的电影（MovieService.recommendMovies），直接调用推荐服务接口获取Id列表，组合少部分信息即可
2. 搜索框需要根据关键词搜索可能相关的电影（MovieService.searchMovies）
3. 从首页/搜索页面找到相关电影简介后，可以进入电影详情页面查看电影详情（MovieService.getMovieDetail）
4. 可以添加新的电影信息（MovieService.createMovie），这个rpc接口中需要幂等处理

## 错误码约定(xxxResp.baseResp.errNo)
RecommendResp中：
```
0,"成功"
1,"参数非法"
2,"用户未登录"
3,"目前无法为用户生成推荐列表，请稍后再试"
999,"系统未知错误"
```
MovieDetailResp中：
```
0,"成功"
1,"参数非法"
2,"用户未登录"
3,"找不到movie id对应的电影详情"
999,"系统未知错误"
```
SearchResp中：
```
0,"成功"
1,"参数非法"
2,"用户未登录"
999,"系统未知错误"
```
CreateResp中：
```
0,"成功"
1,"参数非法"
2,"用户未登录"
3,"用户没有权限创建新电影条目"
999,"系统未知错误"
```