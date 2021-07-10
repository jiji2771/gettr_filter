import requests
import json
import time
import os

SENSITIVE_WORDS_FILE_PATH = "./sensitive_words.txt"
TARGET_USER_PATH = "./target_user.txt"
test_POST_ID = "p2nhx1"
test_OFFSET = "0"
test_MAX = "-1"
test_SIZE = "100"
# URL_POST_COMMENTS = f"https://api.gettr.com/u/post/{test_POST_ID}/comments/?offset={test_OFFSET}&max={test_MAX}"
# SAVE_PATH = f"./violated_comments_{test_POST_ID}.txt"
test_TARGET_USER = "warroom"
# URL_USER_POSTS = f"https://api.gettr.com/u/user/{test_TARGET_USER}/posts/?offset={test_OFFSET}&size={test_SIZE}&fp=f_uo"

# https://api.gettr.com/u/post/p2nhx1/comments

# https://api.gettr.com/u/post/p2nhx1/comments/?offset=0&max=200


def import_target_user(file_path):
    # duplicate code, may refactor later
    # import user
    # return a set of users
    with open(file_path) as f:
        raw_user_list = f.readlines()
    tmp_word_list = [s.strip() for s in raw_user_list]
    tmp_word_list2 = [s.lower() for s in tmp_word_list]
    user_set = set(tmp_word_list2)
    return user_set


def import_sensitive_words(file_path):
    with open(file_path) as f:
        raw_word_list = f.readlines()

    # remove "\n"
    tmp_word_list = [s.strip() for s in raw_word_list]
    # remove "#"
    word_list = [s.strip("#") for s in tmp_word_list]
    # we may need to remove other symbols

    # convert all words to lower case
    lower_word_list = [s.lower() for s in word_list]

    # convert list to set for shorter length
    word_set = set(lower_word_list)
    return word_set


def crawl_one_post(post_id, offset=0, max=-1):
    # default: crawl all comments from one post
    # offset: which index to start
    # max: the maximum number of comments to get; -1 means all comments
    # return the all comments including this post content

    # POST format in API
    # "_t": "xresp",
    # "rc": "OK",
    # "result": {...}

    #   "result": {
    #   "data": {},
    #   "aux": {},
    #   "serial": "cmfd"}
    URL_POST_COMMENTS = f"https://api.gettr.com/u/post/{post_id}/comments/?offset={offset}&max={max}"
    try:
        response = requests.get(URL_POST_COMMENTS.format(post_id, offset, max))
        data = json.loads(response.text)
        if 'result' not in data:
            print(f'error, no result in {URL_POST_COMMENTS.format(post_id)}')
            return []
        if len(data['result']) == 0:
            print("No content from this post.")
            return []

        # "aux" contains the post content and all comments
        # key is the post/comment id
        # value is the post/comment content, including the txt, tag, userid, date, pid (parent id) and puid (parent uid)
        raw_cmt_list = data["result"]["aux"]["cmt"]
        return raw_cmt_list

    except Exception as e:
        print('Error: ')
        print(e)


# test_result = crawl_one_post("p2nhx1")
# print(test_result)
# for cmt in test_result:
#     print(test_result[cmt])

# print(len(test_result))

# word_list = import_sensitive_words(SENSITIVE_WORDS_FILE_PATH)
# print(word_list)


def filter_one_comment(raw_one_comment, sensitive_word_set):
    # filter one comment or post
    # raw_one_comment: comment or post in JSON
    # sensitive_word_set: cleaned sensitive word set
    # return True/False, sensitive word
    # return True: this comment/post contains words from the list
    # return False: this comment/post is OK and clean.


    # check txt
    if raw_one_comment["txt"] is None:
        return False, ""
    content = raw_one_comment["txt"].lower()
    for sw in sensitive_word_set:
        if sw in content:
            return True, sw

    # check tag if it has
    if "htgs" in raw_one_comment:
        raw_tag_list = raw_one_comment["htgs"]
        if raw_tag_list is None:
            return False, ""
        tag_list = [s.lower() for s in raw_tag_list]
        for sw in sensitive_word_set:
            if sw in tag_list:
                return True, sw

    return False, ""

# print(filter_one_comment(test_result["p2nhx1"], word_list))


def filter_one_post(raw_one_post, sensitive_words_set):
    # raw_one_post: post including comments in JSON
    # sensitive_words_set: provided sensitive words in set
    # return a list of post and comments referring sensitive words
    # return [(comment, sensitive_word)]

    target_cmt_list = []

    # loop post and comments
    if raw_one_post == None:
        return []

    if len(raw_one_post) == 0:
        return []

    for cmt_id in raw_one_post:
        cmt_type, sw = filter_one_comment(raw_one_post[cmt_id], sensitive_words_set)
        if cmt_type == True:
            target_cmt_list.append((raw_one_post[cmt_id], sw))

    return target_cmt_list


# test_cmt_list = filter_one_post(test_result, word_list)

# for cmt in test_cmt_list:
#     print(cmt[0])
#     print(cmt[1])


def collect_one_user_posts(user_id, offset=0, size=100):
    # collect posts from one user
    # return user's post id list
    URL_USER_POSTS = f"https://api.gettr.com/u/user/{user_id}/posts/?offset={offset}&size={size}&fp=f_uo"
    post_id_list = []
    try:
        response = requests.get(URL_USER_POSTS.format(user_id, offset, size))
        data = json.loads(response.text)
        if 'result' not in data:
            print(f'error, no result in {URL_USER_POSTS.format(user_id)}')
            return []
        if len(data['result']) == 0:
            print("No content from this user.")
            return []

        # get a list of post ids from "list"
        raw_post_list = data["result"]["data"]["list"]
        for p in raw_post_list:
            post_id_list.append(p["activity"]["pstid"])

        return post_id_list

    except Exception as e:
        print('Error: ')
        print(e)


def save_to_file(cmt_list, post_id, post_user):
    # save the violated comments to txt file
    # first line: comment in JSON
    # second line: violated sensitive word in this comment
    print(f"Violated comments are saved at ./{post_user}/{post_user}_{post_id}.txt\n")
    save_path = f"./{post_user}/{post_user}_{post_id}.txt"
    violated_comment_URL = "https://gettr.com/comment/"
    with open(save_path.format(post_user, post_user, post_id), 'a+') as f:
        for cmt in cmt_list:
            f.write(violated_comment_URL+cmt[0]["_id"]+"\n")
            f.write("%s\n" % cmt[0])
            f.write("%s\n\n" % cmt[1])


# save_to_file(test_cmt_list)


if __name__ == '__main__':
    user_list = import_target_user(TARGET_USER_PATH)
    word_list = import_sensitive_words(SENSITIVE_WORDS_FILE_PATH)
    for u in user_list:
        print(f"Collecting {u}'s post IDs")
        if not os.path.exists(f"{u}"):
            os.makedirs(f"{u}")
        post_id_list = collect_one_user_posts(user_id=u)
        for p in post_id_list:
            print(f"Filtering {u}'s post: {p}")
            all_cmt_list = crawl_one_post(p)
            violated_cmt_list = filter_one_post(all_cmt_list, word_list)
            save_to_file(violated_cmt_list, post_user=u, post_id=p)