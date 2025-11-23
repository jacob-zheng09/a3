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
    """Modifies the user data(no duplicates), user_data, by adding
    followers and following information from the given file.

    Precondition: file is open for reading
                  file is in the format described in the handout
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
    mutual relationships each user has. (If users are following each other)

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

def get_quantile(num_list: list[int], percentage: float) -> int:
    """ Returns the quantile value from num_list at the given percentage.
    The percentage is a float between 0 and 1 inclusive.
    
    precondition: num_list is a list of integers
                  percentage is a float between 0 and 1 inclusive
                  
    >>> get_quantile([11, 12, 13, 14, 15, 16, 17], 0.0)
    11
    >>> get_quantile([11, 12, 13, 14, 15, 16, 17], 0.3)
    12
    >>> get_quantile([11, 12, 13, 14, 15, 16, 17], 1)
    17
    >>> get_quantile([], 0.6)
    -1
    >>> get_quantile([1, 2, 3, 4, 5], -0.6)
    -1
    >>> get_quantile([1, 2, 3, 4, 5], 1.2)
    -1
    """
    if not 0 <= percentage <= 1 or not num_list:
        return -1
    num_list.sort()
    divider = len(num_list) - 1
    i = int(percentage * divider)
    return num_list[i]


def add_bot_candidate_groups(user_data: UserData) -> None:
    """ Modifies user_data by adding bot candidate groups to each user.
    
    precondition: add_follower and add_num_mutual_connections have been called
    >>> sample_data_copy = deepcopy(SAMPLE_DATA_WITH_NUM_MUTUALS)
    >>> add_bot_candidate_groups(sample_data_copy)
    >>> sample_data_copy == SAMPLE_DATA_FULL
    True
    """
    # optimization
    HCLP_com_cond, HCLP_post_cond, HCNA_com_cond, HCLM_com_cond, HCLM_mutual_cond = gather_quantiles(user_data)
    for user in user_data:
        num_of_followers = len(user_data[user][FOLLOWERS])
        num_of_following = len(user_data[user][FOLLOWING])
        if user_data[user][NUM_COMMENTS] >= HCNA_com_cond and compare_account_creation(user_data, "2023-01-01", user):
            user_data[user][BOT_GROUPS].append(HCNA)
        if num_of_following > HFLF_FACTOR * num_of_followers:
            user_data[user][BOT_GROUPS].append(HFLF)
        if user_data[user][NUM_COMMENTS] >= HCLP_com_cond and user_data[user][NUM_POSTS] <= HCLP_post_cond:
            user_data[user][BOT_GROUPS].append(HCLP)
        if user_data[user][NUM_COMMENTS] >= HCLM_com_cond and user_data[user][NUM_MUTUALS] <= HCLM_mutual_cond:
            user_data[user][BOT_GROUPS].append(HCLM)

            
def gather_data(user_data: UserData) -> tuple[list[int], list[int], list[int]]:
    """Returns a tuple of three lists: list of number of comments,
    list of number of posts, list of number of mutual connections. 
    gathered from user_data for bot candidate groups.
    
    precondition: add_follower and add_num_mutual_connections have been called
    >>> sample_data_copy = deepcopy(SAMPLE_DATA_WITH_NUM_MUTUALS)
    >>> gather_data(sample_data_copy)
    ([1, 5, 8, 10, 11], [0, 2, 3, 5, 10], [0, 0, 1, 1, 2])
    """
    tuple_list = ([], [], [])
    for user in user_data:
        tuple_list[0].append(user_data[user][NUM_COMMENTS])
        tuple_list[1].append(user_data[user][NUM_POSTS])
        tuple_list[2].append(user_data[user][NUM_MUTUALS])
    for lst in tuple_list:
        lst.sort()
    return tuple_list

def gather_quantiles(user_data: UserData) -> tuple[int, int, int, int, int]:
    """Returns a tuple of integer five quantile values for bot candidate conditions,
    gathered from user_data.
    
    precondition: add_follower and add_num_mutual_connections have been called
    >>> sample_data_copy = deepcopy(SAMPLE_DATA_WITH_NUM_MUTUALS)
    >>> gather_quantiles(sample_data_copy)
    (10, 0, 10, 10, 0)
    """
    num_com_list, num_post_list, num_mutual_list = gather_data(user_data)
    HCLP_com_cond = get_quantile(num_com_list, P_HCLP_COMMENT) # 0.9
    HCLP_post_cond = get_quantile(num_post_list, P_HCLP_POSTS) # 0.1
    HCNA_com_cond = get_quantile(num_com_list, P_HCNA_COMMENT) # 0.75
    HCLM_com_cond = get_quantile(num_com_list, P_HCLM_COMMENT) # 0.8
    HCLM_mutual_cond = get_quantile(num_mutual_list, P_HCLM_MUTUALS) 
    return (HCLP_com_cond, HCLP_post_cond, HCNA_com_cond, HCLM_com_cond, HCLM_mutual_cond)

def compare_account_creation(user_data: UserData, date: str, user: str) -> bool: 
    """Returns a boolean value whether the account creation date
    of user is after the given date.
    
    precondition: date is in format of yyyy-mm-dd
                    account creation date of user in user_data is in format of yyyy-mm-dd
                    create user dictionary has been called
    >>> sample_data_copy = deepcopy(SAMPLE_DATA_WITH_NUM_MUTUALS)
    >>> compare_account_creation(sample_data_copy, "2023-01-01", "username2")
    True
    """
    date_list = date.split("-")
    userdate_list = user_data[user][ACCOUNT_CREATED].split("-")
    if int(date_list[0]) > int(userdate_list[0]):
        return False 
    if int(date_list[0]) == int(userdate_list[0]):
        if int(date_list[1]) > int(userdate_list[1]):
            return False
        if int(date_list[1]) == int(userdate_list[1]):
            if int(date_list[2]) == int(userdate_list[2]):
                return False
    return True

def find_all_bot_candidates(user_data: UserData) -> UserData:
    """ Returns a dictionary of all bot candidates from user_data.
    
    precondition: add_bot_candidate_groups has been called
    
    >>> sample_data_copy = deepcopy(SAMPLE_DATA_FULL)
    >>> bots = find_all_bot_candidates(sample_data_copy)
    >>> k_bots = bots.keys()
    >>> k_bots == {'username3', 'username5'}
    True
    """
    bots = {}
    for user in user_data:
        if len(user_data[user][BOT_GROUPS]) > 0:
            bots[user] = user_data[user].copy()
    return bots

def find_users_abusing_system(user_data: UserData) -> UserData:
    """  Returns a dictionary of all users abusing the system from user_data.
    (more thatn 50% of bot followers)
    
    precondition: add_bot_candidate_groups has been called
    
    >>> sample_data_copy = deepcopy(SAMPLE_DATA_FULL)
    >>> abuser = find_users_abusing_system(sample_data_copy)
    >>> k_abuser = abuser.keys()
    >>> k_abuser == {'username5', 'username4'}
    True
    """
    abusers = {}
    bots = find_all_bot_candidates(user_data)
    for user in user_data:
        if user_data[user][FOLLOWERS]:
            bots_total = 0
            for follow in user_data[user][FOLLOWERS]:
                if follow in bots:
                    bots_total += 1
            num_follow = len(user_data[user][FOLLOWERS])
            if bots_total/num_follow > 0.5:
                abusers[user] = user_data[user].copy()
    return abusers

def order_bot_candidates(user_data: UserData) -> list[str]:
    """ Returns a list of all bot candidates in decreasing order
    by number of bot groups from user_data.
    
    precondition: add_bot_candidate_groups has been called
                    dictionary passed will have all keys in AccountData
                    NUM_MUTUALS and BOT_GROUPS keys will be present.
    
    >>> sample_data_copy = deepcopy(SAMPLE_DATA_FULL)
    >>> order_bot_candidates(sample_data_copy)
    ['username3', 'username5']
    """
    candidates = find_all_bot_candidates(user_data)
    num_dic = {}
    bot_cand = []
    for user in candidates:
        num_bots = len(candidates[user][BOT_GROUPS])
        if num_bots not in num_dic:
            num_dic[num_bots] = []
        num_dic[num_bots].append(user)
    num_list = list(num_dic.keys())
    num_list.sort(reverse = True)
    if not num_list:
        return []
    for num in num_dic:
        num_dic[num].sort(reverse = True)
    for key in num_list:
        for user in num_dic[key]:
            bot_cand.append(user)
    return bot_cand

def order_users_abusing_system(user_data: UserData) -> list[str]:
    """ Returns a list of all users in decreasing order
    abusing the system from user_data.
    
    precondition: find_users_abusing_system has been called.
                    dictionary passed will have all keys in AccountData
                    NUM_MUTUALS and BOT_GROUPS keys will be present.

    >>> sample_data_copy = deepcopy(SAMPLE_DATA_FULL)
    >>> order_users_abusing_system(sample_data_copy)
    ['username4', 'username5']
    """
    candidates = find_users_abusing_system(user_data)
    bots = find_all_bot_candidates(user_data)
    num_dic = {}
    abuse_cand = []
    for user in candidates:
        num_bots = 0
        for bot in user_data[user][FOLLOWERS]:
            if bot in bots:
                num_bots += 1
        if num_bots not in num_dic:
            num_dic[num_bots] = []
        num_dic[num_bots].append(user)
    num_list = list(num_dic.keys())
    num_list.sort(reverse = True)
    if not num_list:
        return []
    for num in num_dic:
        num_dic[num].sort(reverse = True)
    for key in num_list:
        for user in num_dic[key]:
            abuse_cand.append(user)
    return abuse_cand
    





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
