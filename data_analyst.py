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

    pass


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

    pass


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
