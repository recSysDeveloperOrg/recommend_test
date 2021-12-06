# 电影模块架构
## 接口设计

```
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