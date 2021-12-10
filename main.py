from item_cf import ItemCollaborativeFiltering
from tag_based_recommend import TagBasedRecommend

if __name__ == '__main__':
    movie_file = 'ml-latest/movies.csv'
    ratings_file = 'ml-latest/ratings.csv'
    tag_file = 'ml-latest/tags.csv'

    train_cf = ItemCollaborativeFiltering({'type': 'file', 'file_name': ratings_file}, k=8)
    recall, precision = train_cf.train_model(rating_threshold=2.5)
    print(f'recall:{recall}; precision:{precision}')

    # use tag based recommendation to validate item collaborative filtering recommendation
    tag_rec = TagBasedRecommend(tag_file)
    p, r = tag_rec.train_model(ratings_file, rating_threshold=2.5)
    print(f'tag_recommend: precision {p}, recall {r}')
