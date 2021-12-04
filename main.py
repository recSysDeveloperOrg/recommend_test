from file_reader import csv_read
from item_cf import ItemCollaborativeFiltering


if __name__ == '__main__':
    ratings_file = 'ml-latest/ratings.csv'
    content = csv_read(ratings_file, max_line=10000)
    item_cf = ItemCollaborativeFiltering(user_item_list=content, k=8)
    weights = item_cf.item_similarity()
    pbs = item_cf.predict_interest('4')
    print(pbs)
