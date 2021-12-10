import csv
import math
import multiprocessing
import random
import threading


def init_from_mem(content):
    like_cnt = {}
    for _, like_items in content.items():
        for like_item in like_items:
            like_cnt[like_item[0]] = 1 if like_item[0] not in like_cnt \
                else like_cnt[like_item[0]] + 1

    return content, like_cnt


def init_from_file(file_name):
    user_items, like_cnt = {}, {}
    with open(file_name, encoding='utf8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader, None)
        for line in csv_reader:
            user, item, rating = line[0], line[1], float(line[2])
            if user not in user_items:
                user_items[user] = []

            like_cnt[item] = 1 if item not in like_cnt else like_cnt[item] + 1
            user_items[user].append([item, rating])

    return user_items, like_cnt


class TrainModel(threading.Thread):
    def __init__(self, model_id, user_items, like_cnt):
        threading.Thread.__init__(self)
        self.model_id = model_id
        self.user_items = user_items
        self.weights = {}
        self.like_cnt = like_cnt
        print(f'{model_id} got {len(user_items.items())}')

    def run(self) -> None:
        user_items, like_cnt, weights = self.user_items, self.like_cnt, {}
        loop_cnt = 0
        for _, like_list in user_items.items():
            if loop_cnt % 100 == 0:
                print(f'loop:{loop_cnt}')
            loop_cnt += 1

            for i in like_list:
                for j in like_list:
                    if i[0] == j[0]:
                        continue

                    if i[0] not in weights:
                        weights[i[0]] = {}
                    # reduce influence from frequent users
                    weights[i[0]][j[0]] = 1.0 / math.log(1.0 + len(like_list)) \
                        if j[0] not in weights[i[0]] \
                        else weights[i[0]][j[0]] + 1.0 / math.log(1.0 + len(like_list))

        for i, j_list in weights.items():
            for j, wij in weights[i].items():
                weights[i][j] = wij / math.sqrt(like_cnt[i] * like_cnt[j])

        self.weights = weights

    def get_weights(self):
        return self.weights


class ItemCollaborativeFiltering:
    # user_item_list: a two-dimensional array, each array is like [user, item, etc...]
    # it's used mostly in item_similarity
    # k: parameter for finding k nearest items
    def __init__(self, arg, k):
        if arg['type'] is None:
            raise ValueError('arg["type"] is None')

        arg_type = arg['type']
        if arg_type.lower() == 'file':
            user_items, like_cnt = init_from_file(arg['file_name'])
        elif arg_type.lower() == 'mem':
            user_items, like_cnt = init_from_mem(arg['mem_content'])
        else:
            raise ValueError(f'arg_type[{arg_type}] is not defined')

        self.user_items = user_items
        self.like_cnt = like_cnt
        self.weights = {}
        self.k = k

    def item_similarity(self):
        user_items, like_cnt = self.user_items, self.like_cnt
        thread_cnt = multiprocessing.cpu_count() * 2
        print(f'thread cnt set {thread_cnt}')
        sep_user_item = [{} for _ in range(thread_cnt)]
        train_model_threads = []
        i = 0

        for user, like_list in user_items.items():
            sep_user_item[i % len(sep_user_item)][user] = like_list
            i += 1

        for i in range(thread_cnt):
            tm = TrainModel(f'model[{i}]', sep_user_item[i], like_cnt)
            train_model_threads.append(tm)
            tm.start()

        for i in range(thread_cnt):
            train_model_threads[i].join()

        weights = {}
        for model_thread in train_model_threads:
            w = model_thread.get_weights()
            for i, j_list in w.items():
                if i not in weights:
                    weights[i] = {}
                for j, wij in j_list.items():
                    weights[i][j] = wij

        # normalize weights to promote recommendation accuracy
        for i, j_list in weights.items():
            max_val = 0.0
            for j, wij in weights[i].items():
                max_val = max(max_val, wij)
            for j, wij in weights[i].items():
                weights[i][j] /= max_val

        self.weights = weights
        self.like_cnt = None

    # predict_interest: predict interest possibilities for user_id
    def predict_interest(self, user_id):
        user_items, weights, k = self.user_items[user_id], self.weights, self.k
        item_to_possibility = {}

        for i, rating in user_items:
            if i not in weights:
                continue

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
        item_cf_model = ItemCollaborativeFiltering({'type': 'mem', 'mem_content': train_data}, k=10)
        item_cf_model.item_similarity()
        item_cf_model.user_items = self.user_items
        # {user_id: [items with ratings >= rating_threshold]}
        users, user_to_items = set(), {}
        for user, like_list in test_data.items():
            users.add(user)
            for item, rating in like_list:
                if rating < rating_threshold:
                    continue

                if user not in user_to_items:
                    user_to_items[user] = set()
                user_to_items[user].add(item)

        predict_user_to_items = {}
        for user_id in users:
            if user_id not in item_cf_model.user_items:
                continue
            predict_items = item_cf_model.predict_interest(user_id)
            print(f'predict {user_id} complete')
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
        train_data, test_data = {}, {}
        for user, like_list in self.user_items.items():
            # 只选取1%的用户数据来训练
            if random.randint(0, 100) != 0:
                continue
            if random.randint(0, 5) == 0:
                test_data[user] = like_list
            else:
                train_data[user] = like_list

        return train_data, test_data
