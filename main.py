from file_reader import csv_read
from item_cf import ItemCollaborativeFiltering
from tag_based_recommend import TagBasedRecommend


def get_movies():
    movie_list = csv_read(movie_file, encoding='utf8')
    id_to_movie = {}
    for movie_id, title, genres in movie_list:
        id_to_movie[movie_id] = {'title': title, 'genres': genres}

    return id_to_movie


def recommend_movies_by_item_cf(user_id, k=10):
    content = csv_read(ratings_file, max_line=6666)
    item_cf = ItemCollaborativeFiltering(user_item_list=content, k=8)
    pbs, res = item_cf.predict_interest("{}".format(user_id)), []
    for item_id, w in sorted(pbs.items(), key=lambda x: x[1], reverse=True)[0:k]:
        res.append([item_id, w])

    id_to_movie = get_movies()
    movies = []
    for rec_item in res:
        movies.append([id_to_movie[rec_item[0]]['title'], *rec_item])

    return movies


def item_cf_predict():
    content = csv_read(ratings_file, max_line=20000)
    item_cf = ItemCollaborativeFiltering(user_item_list=content, k=8)
    item_cf.item_similarity()
    max_rec_user_id = 1
    while True:
        if len(item_cf.predict_interest(f'{max_rec_user_id}')) == 0:
            max_rec_user_id -= 1
            break
        max_rec_user_id += 1
    print(f'max recommend user id is {max_rec_user_id}')


def recommend_movie_by_tag(user_id, max_k=10):
    tag_content = csv_read(tag_file)
    tag_rec = TagBasedRecommend(tag_content)
    movie_id_to_preference = tag_rec.predict_top_k(user_id=f'{user_id}', k=max_k)
    movies = get_movies()
    res = {}

    for movie_id, p in movie_id_to_preference.items():
        res[movies[movie_id]['title']] = {
            "preference": p,
            "movie_id": movie_id
        }

    return res


if __name__ == '__main__':
    movie_file = 'ml-latest/movies.csv'
    ratings_file = 'ml-latest/ratings.csv'
    tag_file = 'ml-latest/tags.csv'

    # item_cf_predict()
    rec_res = recommend_movie_by_tag(user_id='56')
    for movie_title, movie_data in rec_res.items():
        print(f'{movie_title}: {movie_data}')
