from file_reader import csv_read
from item_cf import ItemCollaborativeFiltering


def recommend_movies(user_id, k=10):
    pbs, res = item_cf.predict_interest("{}".format(user_id)), []
    for item_id, w in sorted(pbs.items(), key=lambda x: x[1], reverse=True)[0:k]:
        res.append([item_id, w])

    movie_list = csv_read(movie_file, encoding='utf8')
    id_to_movie = {}
    for movie_id, title, genres in movie_list:
        id_to_movie[movie_id] = {'title': title, 'genres': genres}

    movies = []
    for rec_item in res:
        movies.append([id_to_movie[rec_item[0]]['title'], *rec_item])

    return movies


if __name__ == '__main__':
    # TODO 从imdb爬电影数据
    movie_file = 'ml-latest/movies.csv'
    ratings_file = 'ml-latest/ratings.csv'
    content = csv_read(ratings_file, max_line=6666)
    item_cf = ItemCollaborativeFiltering(user_item_list=content, k=8)
    weights = item_cf.item_similarity()
    max_rec_user_id = 1
    while True:
        if len(item_cf.predict_interest(f'{max_rec_user_id}')) == 0:
            max_rec_user_id -= 1
            break
        max_rec_user_id += 1
    print(f'max recommend user id is {max_rec_user_id}')
