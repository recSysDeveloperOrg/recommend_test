# 电影模块架构
## 接口设计

```
message BaseResp {
    int64 err_no = 1;
    string err_msg = 2;
}
// 这里后面可以考虑加上推荐的原因
message Movie {
    string id = 1;
    string title = 2;
    string pic_url = 3;
    optional string introduction = 4;
    optional string participants = 5;
    optional string release_date = 6;
    optional string language = 7;
}

message RecommendReq {
    int64 page = 1;
    int64 offset = 2;
}
message RecommendResp {
    BaseResp base_resp = 1;
    repeated Movie movies = 2;
    int64 n_recommend = 3; // 系统总的推荐数量, 用于判定是否有下一页
}

message MovieDetailReq {
    string id = 1;
}
message MovieDetailResp {
    BaseResp base_resp = 1;
    Movie movie = 2;
}

message SearchReq {
    string keyword = 1;
    int64 page = 2;
    int64 offset = 3;
}
message SearchResp {
    BaseResp base_resp = 1;
    repeated Movie movies = 2;
    int64 n_search = 3; // 搜索结果总数, 用于判定是否有下一页
}

message CreateReq {
    Movie movie = 1;
}
message CreateResp {
    BaseResp base_resp = 1;
}

service MovieService {
    rpc RecommendMovies(RecommendReq) returns (RecommendResp) {}
    rpc GetMovieDetail(MovieDetailReq) returns (MovieDetailResp) {}
    rpc SearchMovies(SearchReq) returns (SearchResp) {}
    rpc CreateMovie(CreateReq) returns (CreateResp) {}
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

##DB模型
项目准备使用MongoDB，这是一个文档类型的数据库，跟JSON格式非常类似
```
{
    _id: "xxx",
    title:"xxx",
    pic_url:"https://xxx.com",
    introduction: "xxx",
    participants: "xxx",
    release_date: xxx,
    language: "xxx",
    ave_rating:x.x  // 电影平均评分，仅在新用户评分时计算
}
```