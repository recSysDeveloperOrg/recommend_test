import math
import random


class ItemCollaborativeFiltering:
    # user_item_list: a two-dimensional array, each array is like [user, item, etc...]
    # it's used mostly in item_similarity
    # k: parameter for finding k nearest items
    def __init__(self, user_item_list, k):

        user_items, like_cnt = {}, {}
        for user_item in user_item_list:
            user, item = user_item[0], user_item[1]
            if user not in user_items:
                user_items[user] = set()

            like_cnt[item] = 1 if item not in like_cnt else like_cnt[item] + 1
            user_items[user].add(item)

        self.user_items = user_items
        self.like_cnt = like_cnt
        self.user_item_list = user_item_list
        self.weights = {}
        self.k = k

    def item_similarity(self):
        user_items, like_cnt = self.user_items, self.like_cnt
        weights = {}
        for _, like_set in user_items.items():
            for i in like_set:
                for j in like_set:
                    if i == j:
                        continue

                    if i not in weights:
                        weights[i] = {}
                    # reduce influence from frequent users
                    weights[i][j] = 1.0 / math.log(1.0 + len(like_set)) \
                        if j not in weights[i] else weights[i][j] + 1.0 / math.log(1.0 + len(like_set))

        for i, j_list in weights.items():
            for j, wij in weights[i].items():
                weights[i][j] = wij / math.sqrt(like_cnt[i] * like_cnt[j])

        # normalize weights to promote recommendation accuracy
        for i, j_list in weights.items():
            max_val = 0.0
            for j, wij in weights[i].items():
                max_val = max(max_val, wij)
            for j, wij in weights[i].items():
                weights[i][j] /= max_val

        self.weights = weights

    # predict_interest: predict interest possibilities for user_id
    def predict_interest(self, user_id):
        user_item_list, weights, k = self.user_item_list, self.weights, self.k
        item_to_rating, item_to_possibility = {}, {}
        for user_item in user_item_list:
            user, item, rating = user_item[0], user_item[1], user_item[2]
            if user != user_id:
                continue

            item_to_rating[item] = float(rating)

        for i, rating in item_to_rating.items():
            for j, wij in sorted(weights[i].items(), key=lambda x: x[1], reverse=True)[0:k]:
                if j in self.user_items[user_id]:
                    continue

                item_to_possibility[j] = wij * rating if j not in item_to_possibility \
                    else item_to_possibility[j] + wij * rating

        return item_to_possibility

    # train_model is used only to measure the recall and precision of the model
    # and should never be called in production env
    def train_model(self, rating_threshold=3):
        train_data, test_data = self.split_data()
        item_cf_model = ItemCollaborativeFiltering(train_data, k=10)
        item_cf_model.item_similarity()
        # {user_id: [items with ratings >= rating_threshold]}
        users, user_to_items = set(), {}
        for data in test_data:
            user, item, rating = data[0], data[1], float(data[2])
            users.add(user)

            if rating < rating_threshold:
                continue
            if user not in user_to_items:
                user_to_items[user] = set()
            user_to_items[user].add(item)

        predict_user_to_items = {}
        for user_id in users:
            predict_items = item_cf_model.predict_interest(user_id)
            predict_set = set()
            for item_id, _ in predict_items.items():
                predict_set.add(item_id)

            predict_user_to_items[user_id] = predict_set

        # compare difference between user_to_items and predict_user_to_items
        share, r, t = 0, 0, 0
        for user_id in users:
            if user_id not in user_to_items or user_id not in predict_user_to_items:
                continue

            share += len(user_to_items[user_id] & predict_user_to_items[user_id])
            r += len(predict_user_to_items[user_id])
            t += len(user_to_items[user_id])

        print(f'share:{share}; predict_r:{r}; recall_t:{t}')
        return (1.0 * share) / (1.0 * t), (1.0 * share) / (1.0 * r)

    def split_data(self):
        train_data, test_data = [], []
        for data in self.user_item_list:
            if random.randint(0, 5) == 0:
                test_data.append(data)
            else:
                train_data.append(data)

        return train_data, test_data
