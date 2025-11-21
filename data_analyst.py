"""CSCA08: Fall 2025 -- Assignment 3: Social Media Data Analyst

Starter code.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 Jacqueline Smith, David Liu, Dominik Luszczynski,
and Anya Tafliovich

"""

from typing import TextIO
from copy import deepcopy

from constants import (
    UserData,
    AccountData,
    DOB,
    NUM_POSTS,
    NUM_COMMENTS,
    ACCOUNT_CREATED,
    FOLLOWERS,
    FOLLOWING,
    NUM_MUTUALS,
    BOT_GROUPS,
    SEP,
    USERNAME_COL,
    DOB_COL,
    NUM_POSTS_COL,
    NUM_COMMENTS_COL,
    ACCOUNT_CREATED_COL,
    FOLLOWER_COL,
    FOLLOWING_COL,
    HCLP,
    HCLM,
    HCNA,
    HFLF,
    P_HCLM_COMMENT,
    P_HCLM_MUTUALS,
    P_HCLP_COMMENT,
    P_HCLP_POSTS,
    P_HCNA_COMMENT,
    HFLF_FACTOR,
)

SAMPLE_DATA = {
    "username1": {
        DOB: "1973-01-06",
        NUM_POSTS: 3,
        NUM_COMMENTS: 8,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username2"],
        FOLLOWING: ["username2", "username4"],
        BOT_GROUPS: [],
    },
    "username2": {
        DOB: "1973-01-06",
        NUM_POSTS: 5,
        NUM_COMMENTS: 5,
        ACCOUNT_CREATED: "2025-01-01",
        FOLLOWERS: ["username1", "username3"],
        FOLLOWING: [
            "username1",
            "username3",
        ],
        BOT_GROUPS: [],
    },
    "username3": {
        DOB: "1973-01-06",
        NUM_POSTS: 0,
        NUM_COMMENTS: 11,
        ACCOUNT_CREATED: "2025-01-01",
        FOLLOWERS: ['username2'],
        FOLLOWING: ["username2", "username4", "username5"],
        BOT_GROUPS: [],
    },
    "username4": {
        DOB: "1973-01-06",
        NUM_POSTS: 10,
        NUM_COMMENTS: 1,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username1",
                    "username3",
                    "username5"],
        FOLLOWING: [],
        BOT_GROUPS: [],
    },
    "username5": {
        DOB: "1973-01-06",
        NUM_POSTS: 2,
        NUM_COMMENTS: 10,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username3"],
        FOLLOWING: ["username4"],
        BOT_GROUPS: [],
    },
}

SAMPLE_DATA_WITH_NUM_MUTUALS = {
    "username1": {
        DOB: "1973-01-06",
        NUM_POSTS: 3,
        NUM_COMMENTS: 8,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username2"],
        FOLLOWING: ["username2", "username4"],
        BOT_GROUPS: [],
        NUM_MUTUALS: 1
    },
    "username2": {
        DOB: "1973-01-06",
        NUM_POSTS: 5,
        NUM_COMMENTS: 5,
        ACCOUNT_CREATED: "2025-01-01",
        FOLLOWERS: ["username1", "username3"],
        FOLLOWING: [
            "username1",
            "username3",
        ],
        BOT_GROUPS: [],
        NUM_MUTUALS: 2,
    },
    "username3": {
        DOB: "1973-01-06",
        NUM_POSTS: 0,
        NUM_COMMENTS: 11,
        ACCOUNT_CREATED: "2025-01-01",
        FOLLOWERS: ['username2'],
        FOLLOWING: ["username2", "username4", "username5"],
        BOT_GROUPS: [],
        NUM_MUTUALS: 1
    },
    "username4": {
        DOB: "1973-01-06",
        NUM_POSTS: 10,
        NUM_COMMENTS: 1,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username1", "username3", "username5"],
        FOLLOWING: [],
        BOT_GROUPS: [],
        NUM_MUTUALS: 0
    },
    "username5": {
        DOB: "1973-01-06",
        NUM_POSTS: 2,
        NUM_COMMENTS: 10,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username3"],
        FOLLOWING: ["username4"],
        BOT_GROUPS: [],
        NUM_MUTUALS: 0
    },
}

SAMPLE_DATA_FULL = {
    "username1": {
        DOB: "1973-01-06",
        NUM_POSTS: 3,
        NUM_COMMENTS: 8,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username2"],
        FOLLOWING: ["username2", "username4"],
        BOT_GROUPS: [],
        NUM_MUTUALS: 1
    },
    "username2": {
        DOB: "1973-01-06",
        NUM_POSTS: 5,
        NUM_COMMENTS: 5,
        ACCOUNT_CREATED: "2025-01-01",
        FOLLOWERS: ["username1", "username3"],
        FOLLOWING: [
            "username1",
            "username3",
        ],
        BOT_GROUPS: [],
        NUM_MUTUALS: 2,
    },
    "username3": {
        DOB: "1973-01-06",
        NUM_POSTS: 0,
        NUM_COMMENTS: 11,
        ACCOUNT_CREATED: "2025-01-01",
        FOLLOWERS: ['username2'],
        FOLLOWING: ["username2", "username4", "username5"],
        BOT_GROUPS: ['highCommentsNewAccount',
                     'highFollowingLowFollowers',
                     'highCommentsLowPosts'],
        NUM_MUTUALS: 1
    },
    "username4": {
        DOB: "1973-01-06",
        NUM_POSTS: 10,
        NUM_COMMENTS: 1,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username1", "username3", "username5"],
        FOLLOWING: [],
        BOT_GROUPS: [],
        NUM_MUTUALS: 0
    },
    "username5": {
        DOB: "1973-01-06",
        NUM_POSTS: 2,
        NUM_COMMENTS: 10,
        ACCOUNT_CREATED: "2023-01-01",
        FOLLOWERS: ["username3"],
        FOLLOWING: ["username4"],
        BOT_GROUPS: ['highCommentsLowMutuals'],
        NUM_MUTUALS: 0
    },
}


# We provide the header and docstring for this function to get you
# started and to demonstrate that there are no docstring examples in
# functions that read from files.
def create_users_dictionary(users_file: TextIO) -> UserData:
    """Return a dictionary (no duplicates) created from
    the file users_file in the form of the UserData:

    {
        username: {
            DOB : dob,
            NUM_POSTS: num_posts,
            NUM_COMMENTS: num_comments,
            ACCOUNT_CREATED: account_created,
            FOLLOWERS: [],
            FOLLOWING: [],
            BOT_GROUPS: []
        }
        ...
    }

    Precondition: users_file is open for reading
                  users_file is in the format described in the handout

    """
    user_data = {}
    users_file.readline()
    for line in users_file:
        linelist = line.split(SEP)
        name = linelist[USERNAME_COL].strip()
        dob = linelist[DOB_COL].strip()
        num_post = int(linelist[NUM_POSTS_COL].strip())
        num_comments = int(linelist[NUM_COMMENTS_COL].strip())
        account_created = linelist[ACCOUNT_CREATED_COL].strip()
        if name not in user_data:
            user_data[name] = {}
            user_data[name][DOB] = dob
            user_data[name][NUM_POSTS] = num_post
            user_data[name][NUM_COMMENTS] = num_comments
            user_data[name][ACCOUNT_CREATED] = account_created
            user_data[name][FOLLOWERS] = []
            user_data[name][FOLLOWING] = []
            user_data[name][BOT_GROUPS] = []
    return user_data

def add_follower(user_data: UserData, file: TextIO) -> None:
    """
    Precondition: file is open for reading
                file is in the format described in the handout

Note that there should not be any duplicate usernames for each FOLLOWERS and FOLLOWING list in the UserData dictionary.
 
You do NOT need to write any examples/doctests in this function's docstring.
Mutate? YES
    """
    file.readline()
    for line in file:
        linelist = line.split(SEP)
        follower = linelist[FOLLOWER_COL].strip()
        following = linelist[FOLLOWING_COL].strip()
        if follower in user_data:
            if following not in user_data[follower][FOLLOWING]:
                user_data[follower][FOLLOWING].append(following)
        if following in user_data:
            if follower not in user_data[following][FOLLOWERS]:
                user_data[following][FOLLOWERS].append(follower)




# We provide the header and part of a docstring for this function to
# get you started and to demonstrate the use of function deepcopy in
# examples that modify input data.
def add_num_mutual_connections(users_dict: UserData) -> None:
    """Modify the dictionary users_dict by adding the number of
    mutual relationships each user has using the NUM_MUTUALS key.

    Note a mutual relationship occurs when two users follow each
    other.

    >>> sample_data_copy = deepcopy(SAMPLE_DATA)
    >>> add_num_mutual_connections(sample_data_copy)
    >>> sample_data_copy['username1'][NUM_MUTUALS] == 1
    True
    >>> sample_data_copy['username2'][NUM_MUTUALS] == 2
    True
    """
    for key in users_dict:
        if NUM_MUTUALS not in users_dict[key]:
            users_dict[key][NUM_MUTUALS] = 0
        for name in users_dict[key][FOLLOWERS]:
            if name in users_dict[key][FOLLOWING]:
                users_dict[key][NUM_MUTUALS] += 1

    """
    delete work after
    neeed to sort the lsit 
    [11, 12, 13, 14, 15, 16, 17]
    [11 | 12 | 13 | 14 | 15 | 16 | 17]
        1    2    3    4    5    6          dividers
      0    1    2    3    4    5    6       indexes
     if p = 0.3, return 12
        0.3 x 6 = 1.8 ---> round down to integer --> 1 --> 12
     if p = 0.6 return 14
        0.6 x 6 = 3.6 ---> round down to integer ----> 3 ---> 14
    i = floor(p * dividers) cant use floor so int()? read documentation or test
    """
def get_quantile(num_list: list[int], percentage: float) -> int:
    """ 
    >>> get_quantile([11, 12, 13, 14, 15, 16, 17], 0.3)
    12
    >>> get_quantile([11, 12, 13, 14, 15, 16, 17], 0.6)
    14
    >>> get_quantile([], 0.6)
    -1
    >>> get_quantile([], -0.6)
    -1
    >>> get_quantile([1, 2, 3, 4, 5], -0.6)
    -1
    """
    if not 0 <= percentage <= 1 or not num_list:
        return -1
    num_list.sort()
    divider = len(num_list) - 1
    i = int(percentage * divider)
    return num_list[i]

def add_bot_candidate_groups(user_data: UserData) -> None:
    """precondition add_followers abd add_num_mutual_connections have been called
    
    use num post and num comments collect all values and put them into a list """
    # for gathering 
    num_com_list =[]
    num_post_list = []
    for user in user_data:
        num_com_list.append(user_data[user][NUM_COMMENTS]).sort()
        num_post_list.append(user_data[user][NUM_POSTS]).sort()


    # for HCLP
    HCLP_com_cond = get_quantile(num_com_list, P_HCLP_COMMENT)
    HCLP_post_cond = get_quantile(num_post_list, P_HCLP_POSTS)
    for user in user_data:
        if user_data[user][NUM_COMMENTS] >= HCLP_com_cond and user_data[user][NUM_POSTS] <= HCLP_post_cond:
            user_data[user][BOT_GROUPS].append(HCLP)

    #for HCLM
    HCNA_com_cond = get_quantile(num_com_list, P_HCNA_COMMENT)
    for user in user_data:
        if user_data[user][NUM_COMMENTS] >= HCNA_com_cond and :


    

def compare_account_creation(user_data: UserData, date: str, user: str) -> bool: 
    """precondition date must be in format of yyyy-mm-dd user_data, account creation must be in format of yyyy-mm-dd, create user dictionary must be called"""
    date_list = date.split("-")
    userdate_list = user_data[user][ACCOUNT_CREATED].split("-")
    if date_list[0] > userdate_list[0]:
        return False 
    if (date_list[0] == userdate_list[0] and date_list[1] == userdate_list[1]
        and date_list[2] == userdate_list[2]):
        return False
    return True
# this cover all cases if year is smaller than date then return false, if equal check if day and month equal if it is then return false
# so that means only year factor matters
    





if __name__ == "__main__":
    import doctest

    doctest.testmod()

    '''
    Uncomment the code below when you are ready to test.

    The code below uses the small dataset. If you wish to use the
    larger dataset, please replace _small with _medium.
    '''

    # with open("users_small.csv", "r") as f:
    #     all_users = create_users_dictionary(f)

    # with open("followers_small.csv", "r") as f:
    #     add_followers(all_users, f)

    # add_num_mutual_connections(all_users)

    # add_bot_candidate_groups(all_users)

    # all_bot_candidates = find_all_bot_candidates(all_users)
    # users_using_bots = find_users_abusing_system(all_users)
    # bot_candidate_order = order_bot_candidates(all_users)
    # users_using_bots_order = order_users_abusing_system(all_users)

    # print("=" * 50)
    # print('Bot Candidates: ')
    # print("=" * 50)
    # print(bot_candidate_order)
    # print("=" * 50)
    # print('Users Using Bots: ')
    # print("=" * 50)
    # print(users_using_bots_order)
