"""CSCA08 Fall 2025 -- Assignment 3: Social Media Data Analyst

A simple checker for functions in data_analyst.py.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 Dominik Luszczynski,
Jacqueline Smith, David Liu, and Anya Tafliovich

"""
from io import StringIO
from typing import Any, Union
import unittest
import checker
import data_analyst

AccountData = dict[str, str | list[str] | int]
UserData = dict[str, AccountData]
# Dictionary Keys
USERNAME = 'username'
DOB = 'dob'
NUM_POSTS = 'num_posts'
NUM_COMMENTS = 'num_comments'
ACCOUNT_CREATED = 'account_created'
FOLLOWERS = 'followers'
FOLLOWING = 'following'
NUM_MUTUALS = 'num_mutuals'
BOT_GROUPS = 'bot_groups'

# Column indexes for users file
USERNAME_COL = 0 # username
DOB_COL = 1 # date of birth
NUM_POSTS_COL = 2 # number of posts made
NUM_COMMENTS_COL = 3 # number of comments made
ACCOUNT_CREATED_COL = 4 # date of account creation

# Column indexes for follower file
FOLLOWER_COL = 0
FOLLOWING_COL = 1

# seperator for reading files
SEP = ','

# Bot Group Names
HCLP = 'highCommentsLowPosts'
HCLM = 'highCommentsLowMutuals'
HCNA = 'highCommentsNewAccount'
HFLF = 'highFollowingLowFollowers'

# Bot Group quantiles and Factors
P_HCLP_COMMENT = 0.9
P_HCLP_POSTS = 0.1
P_HCLM_COMMENT = 0.8
P_HCLM_MUTUALS = 0.1
P_HCNA_COMMENT = 0.75
HFLF_FACTOR = 2

CONSTANTS = {
    'DOB': 'dob',
    'NUM_POSTS': 'num_posts',
    'NUM_COMMENTS': 'num_comments',
    'ACCOUNT_CREATED': 'account_created',
    'FOLLOWERS': 'followers',
    'FOLLOWING': 'following',
    'NUM_MUTUALS': 'num_mutuals',
    'BOT_GROUPS': 'bot_groups',
    # Column indexes for users file
    'USERNAME_COL': 0, # username
    'DOB_COL': 1, # date of birth
    'NUM_POSTS_COL': 2, # number of posts made
    'NUM_COMMENTS_COL': 3, # number of comments made
    'ACCOUNT_CREATED_COL': 4, # date of account creation
    # Column indexes for follower file
    'FOLLOWER_COL': 0,
    'FOLLOWING_COL': 1,
    'SEP': ',',
    # Bot Group Names
    'HCLP': 'highCommentsLowPosts',
    'HCLM': 'highCommentsLowMutuals',
    'HCNA': 'highCommentsNewAccount',
    'HFLF': 'highFollowingLowFollowers',

    # Bot Group quantiles and Factors
    'P_HCLP_COMMENT': 0.9,
    'P_HCLP_POSTS': 0.1,
    'P_HCLM_COMMENT': 0.8,
    'P_HCLM_MUTUALS': 0.1,
    'P_HCNA_COMMENT': 0.75,
    'HFLF_FACTOR': 2,

}



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

USERS_SMALL = '''username,dob,num_posts,num_comments,account_created
krogers,1977-12-01,193,731,2024-09-08
jennifercooper,1913-01-07,479,796,2020-03-21
heatherrobinson,1930-05-29,165,858,2023-05-31
hacosta,1971-03-24,230,856,2021-03-29
paulbaldwin,1944-08-20,220,371,2024-08-24
allison45,1938-07-02,338,898,2024-08-13
suzannenavarro,1912-11-19,438,464,2022-10-11
bellpeter,1995-05-18,192,143,2022-11-27
emeyer,1924-06-25,88,973,2023-08-15
wcosta,1954-11-04,266,911,2025-01-05'''

FOLLOWERS_SMALL = '''follower,following
heatherrobinson,suzannenavarro
wcosta,emeyer
bellpeter,paulbaldwin
allison45,paulbaldwin
emeyer,jennifercooper
hacosta,jennifercooper
wcosta,bellpeter
suzannenavarro,krogers
bellpeter,allison45
wcosta,krogers
wcosta,heatherrobinson
bellpeter,krogers
suzannenavarro,hacosta
allison45,krogers
wcosta,hacosta
jennifercooper,suzannenavarro
krogers,hacosta
heatherrobinson,jennifercooper
emeyer,paulbaldwin
hacosta,paulbaldwin
bellpeter,hacosta
paulbaldwin,krogers
allison45,hacosta
bellpeter,suzannenavarro
emeyer,allison45
paulbaldwin,hacosta
emeyer,krogers
bellpeter,wcosta
hacosta,heatherrobinson
emeyer,heatherrobinson
emeyer,hacosta
heatherrobinson,allison45
wcosta,jennifercooper
krogers,jennifercooper
hacosta,suzannenavarro
emeyer,suzannenavarro
heatherrobinson,krogers
jennifercooper,paulbaldwin
jennifercooper,allison45
krogers,paulbaldwin
'''



class TestChecker(unittest.TestCase):
    """Sanity checker for assignment 3 functions."""

    def test_create_users_dictionaary(self) -> None:
        """Function create_users_dictionary"""

        self._check(data_analyst.create_users_dictionary, [StringIO(USERS_SMALL)],
                    dict)

    def test_add_followers(self) -> None:
        """Function add_followers"""

        users = data_analyst.create_users_dictionary(StringIO(USERS_SMALL))
        self._check(data_analyst.add_followers, [users, StringIO(FOLLOWERS_SMALL)],
                    type(None))

    def test_add_num_mutual_connections(self) -> None:
        """Function add_num_mutual_connections"""

        self._check(data_analyst.add_num_mutual_connections,
                    [SAMPLE_DATA],
                    type(None))

    def test_get_quantile(self) -> None:
        """Function get_quantile"""

        print(f'\nChecking get_quantile...')
        self._check(data_analyst.get_quantile,
                    [[2, 3, 1, 34, 1, 3], 0.2],
                    int)
        
    def test_add_bot_candidate_groups(self) -> None:
        """Function add_bot_candidate_groups"""

        self._check(data_analyst.add_bot_candidate_groups,
                    [SAMPLE_DATA_WITH_NUM_MUTUALS], type(None))


    def test_find_all_bot_candidates(self) -> None:
        """Function find_all_bot_candidates"""

        self._check(data_analyst.find_all_bot_candidates,
                    [SAMPLE_DATA_FULL], dict)

    def test_find_users_abusing_system(self) -> None:
        """Function find_users_abusing_system"""

        self._check(data_analyst.find_users_abusing_system,
                    [SAMPLE_DATA_FULL], dict)


    def test_order_bot_candidates(self) -> None:
        """Function order_bot_candidates"""

        print(f'\nChecking order_bot_candidates...')
        result = checker.returns_list_of(data_analyst.order_bot_candidates, [SAMPLE_DATA_FULL], str)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def test_order_users_abusing_system(self) -> None:
        """Function order_users_abusing_system"""

        print(f'\nChecking order_users_abusing_system...')
        result = checker.returns_list_of(data_analyst.order_users_abusing_system, [SAMPLE_DATA_FULL], str)
        self.assertTrue(result[0], result[1])
        print('  check complete')


    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, data_analyst)
        print('  check complete')


    def _check(self, func: callable, args: list, ret_type: type) -> None:
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.

        """

        print(f'\nChecking {func.__name__}...')
        result = checker.type_check_simple(func, args, ret_type)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def _check_constants(self, name2value: dict[str, object], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = (f'The value of constant {name} should be '
                   '{expected} but is {actual}.')
            self.assertEqual(expected, actual, msg)



checker.ensure_no_io('data_analyst')
TARGET_LEN = 79
print(''.center(TARGET_LEN, "="))
print(' Start: checking coding style '.center(TARGET_LEN, "="))
checker.run_pyta('data_analyst.py', 'a3_pyta.txt')
print(' End checking coding style '.center(TARGET_LEN, "="))

print(' Start: checking type contracts '.center(TARGET_LEN, "="))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, "="))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')