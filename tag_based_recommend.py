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
        for item_id in self.item_id_set:
            item_to_interest[item_id] = self.predict_interest(user_id, item_id)

        res = {}
        for item_id, interest in sorted(item_to_interest.items(), key=lambda x: x[1], reverse=True)[0:k]:
            res[item_id] = interest

        return res
