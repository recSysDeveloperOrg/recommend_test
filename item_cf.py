import math


class ItemCollaborativeFiltering:
    # user_item_list: a two-dimensional array, each array is like [user, item, etc...]
    # it's used mostly in item_similarity
    # k: parameter for finding k nearest items
    def __init__(self, user_item_list, k):
        self.user_item_list = user_item_list
        self.weights = {}
        self.k = k

    def item_similarity(self):
        user_item_list = self.user_item_list
        # first, convert [user,item] to { user: [liked_list] }
        user_items, like_cnt = {}, {}
        for user_item in user_item_list:
            user, item = user_item[0], user_item[1]
            if user not in user_items:
                user_items[user] = []

            like_cnt[item] = 1 if item not in like_cnt else like_cnt[item] + 1
            user_items[user].append(item)

        weights = {}
        for _, like_list in user_items.items():
            for i in like_list:
                for j in like_list:
                    if i == j:
                        continue

                    if i not in weights:
                        weights[i] = {}
                    # reduce influence from frequent users
                    weights[i][j] = 1.0 / math.log(1.0 + len(like_list)) \
                        if j not in weights[i] else weights[i][j] + 1.0 / math.log(1.0 + len(like_list))

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

    # predict_interest: predict interest possibilities for user_id2
    def predict_interest(self, user_id):
        user_item_list, weights, k = self.user_item_list, self.weights, self.k
        item_to_rating, item_to_possibility = {}, {}
        for user_item in user_item_list:
            user, item, rating = user_item[0], user_item[1], user_item[2]
            if user != user_id:
                continue

            item_to_rating[item] = float(rating)

        for i, rating in item_to_rating.items():
            pb = 0.0
            for j, wij in sorted(weights[i].items(), key=lambda x: x[1], reverse=True)[0:k]:
                pb += wij * rating

            if pb > 0:
                item_to_possibility[i] = pb

        return item_to_possibility
