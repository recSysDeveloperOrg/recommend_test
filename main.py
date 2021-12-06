from file_reader import csv_read
from item_cf import ItemCollaborativeFiltering
from tag_based_recommend import TagBasedRecommend

if __name__ == '__main__':
    movie_file = 'ml-latest/movies.csv'
    ratings_file = 'ml-latest/ratings.csv'
    tag_file = 'ml-latest/tags.csv'

    rating_content = csv_read(ratings_file, max_line=10000)
    train_cf = ItemCollaborativeFiltering(rating_content, k=8)
    recall, precision = train_cf.train_model(rating_threshold=2.5)
    print(f'recall:{recall}; precision:{precision}')

    # use tag based recommendation to validate item collaborative filtering recommendation
    tag_content = csv_read(tag_file)
    tag_rec = TagBasedRecommend(tag_content)
    p, r = tag_rec.train_model(rating_content, rating_threshold=2.5)
    print(f'tag_recommend: precision {p}, recall {r}')
