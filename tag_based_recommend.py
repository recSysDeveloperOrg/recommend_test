import math


class TagBasedRecommend:
    def __init__(self, user_tag_list):
        user_to_tag_cnt, item_to_tag_cnt = {}, {}
        user_to_tags, item_to_tags = {}, {}
        tag_to_users, item_to_users = {}, {}
        item_id_set = set()

        for user_id, item_id, tag_id, _ in user_tag_list:
            tag_id = tag_id.lower()
            if user_id not in user_to_tag_cnt:
                user_to_tag_cnt[user_id] = {}
            if item_id not in item_to_tag_cnt:
                item_to_tag_cnt[item_id] = {}
            user_to_tag_cnt[user_id][tag_id] = 1 if tag_id not in user_to_tag_cnt[user_id] \
                else user_to_tag_cnt[user_id][tag_id] + 1
            item_to_tag_cnt[item_id][tag_id] = 1 if tag_id not in item_to_tag_cnt[item_id] \
                else item_to_tag_cnt[item_id][tag_id] + 1

            if user_id not in user_to_tags:
                user_to_tags[user_id] = set()
            if item_id not in item_to_tags:
                item_to_tags[item_id] = set()
            user_to_tags[user_id].add(tag_id)
            item_to_tags[item_id].add(tag_id)

            if tag_id not in tag_to_users:
                tag_to_users[tag_id] = set()
            if item_id not in item_to_users:
                item_to_users[item_id] = set()
            tag_to_users[tag_id].add(user_id)
            item_to_users[item_id].add(user_id)

            item_id_set.add(item_id)

        self.user_to_tag_cnt = user_to_tag_cnt
        self.item_to_tag_cnt = item_to_tag_cnt
        self.user_to_tags = user_to_tags
        self.item_to_tags = item_to_tags
        self.tag_to_users = tag_to_users
        self.item_to_users = item_to_users
        self.item_id_set = item_id_set

    def predict_interest(self, user_id, item_id):
        share_tags, p = self.user_to_tags[user_id] & self.item_to_tags[item_id], 0.0
        for tag_id in share_tags:
            tag_id = tag_id.lower()
            tmp = self.user_to_tag_cnt[user_id][tag_id] * self.item_to_tag_cnt[item_id][tag_id]
            tmp /= math.log(1 + len(self.tag_to_users[tag_id])) * math.log(1 + len(self.item_to_users[item_id]))
            p += tmp

        return p

    def predict_top_k(self, user_id, k=10):
        item_to_interest = {}
        # you can optimize here with multi-thread
        for item_id in self.item_id_set:
            item_to_interest[item_id] = self.predict_interest(user_id, item_id)

        res = {}
        for item_id, interest in sorted(item_to_interest.items(), key=lambda x: x[1], reverse=True)[0:k]:
            res[item_id] = interest

        return res

    def train_model(self, user_item_list, rating_threshold=3):
        user_to_item_set = {}
        user_set = set()
        for user_item in user_item_list:
            user, item, rating = user_item[0], user_item[1], float(user_item[2])
            user_set.add(user)
            if user not in user_to_item_set:
                user_to_item_set[user] = set()
            if rating < rating_threshold:
                continue
            user_to_item_set[user].add(item)

        share, precision, recall = 0, 0, 0
        for user_id in user_set:
            if user_id not in self.user_to_tags:
                continue

            item_to_interest = self.predict_top_k(user_id)
            item_set = set()
            for item_id, _ in item_to_interest.items():
                item_set.add(item_id)

            share += len(item_set & user_to_item_set[user_id])
            precision += len(item_set)
            recall += len(user_to_item_set[user_id])

        print(f'total share:{share}; recall:{recall}; pre:{precision}')
        return share * 1.0 / precision, share * 1.0 / recall
