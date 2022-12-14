"""CSC108/A08: Fall 2021 -- Assignment 2: voting

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Sophia Huynh, Sadia Sharmin,
Elizabeth Patitsas, Anya Tafliovich.

"""

from typing import List

from constants import (COL_RIDING, COL_VOTER, COL_RANK, COL_RANGE,
                       COL_APPROVAL, APPROVAL_TRUE, APPROVAL_FALSE,
                       SEPARATOR)

# In the following docstrings, 'VoteData' refers to a list of 5
# elements of the following types:
#
# at index COL_RIDING: int         (this is the riding number)
# at index COL_VOTER: int         (this is the voter number)
# at index COL_RANK: List[str]   (this is the rank ballot)
# at index COL_RANGE: List[int]   (this is the range ballot)
# at index COL_APPROVAL: List[bool]  (this is the approval ballot)

###############################################################################
# Task 0: Creating example data
###############################################################################

SAMPLE_DATA_1 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
                  [False, True, False, False]],
                 [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
                  [False, False, True, True]],
                 [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
                  [False, True, False, True]],
                 [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
                  [True, False, True, True]]]
SAMPLE_ORDER_1 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']


SAMPLE_DATA_2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [4, 0, 5, 0],
                  [True, False, True, False]],
                 [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4, 5, 5, 5],
                  [True, True, True, True]],
                 [72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [0, 1, 1, 5],
                  [False, True, True, True]]]
SAMPLE_ORDER_2 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']

SAMPLE_DATA_3 = [[0, 0, ['NDP'], [5], [True]]]

SAMPLE_DATA_4 = [[0, 0, ['NDP'], [5], [True]],
                 [0, 2, ['NDP', 'BLUE'], [5, 4], [True, False]],
                 [1, 0, ['NDP'], [5], [True]], [7, 90, ['NDP'], [5], [False]],
                 [5, 2, ['GREEN', 'BLUE'], [5, 4], [True, False]]]


###############################################################################
# Task 1: Data cleaning
###############################################################################

def clean_data(data: List[List[str]]) -> None:
    """Modify data so that the applicable string values are converted to
    their appropriate type, making data of type List['VoteType'].

    Pre: Each item in data is in the format
     at index COL_RIDING: a str that can be converted to an integer (riding)
     at index COL_VOTER: a str that can be converted to an integer (voter ID)
     at index COL_RANK: a SEPARATOR-separated non-empty string (rank ballot)
     at index COL_RANGE: a SEPARATOR-separated non-empty string of ints
                         (range ballot)
     at index COL_APPROVAL: a SEPARATOR-separated non-empty string of
                         APPROVAL_TRUE's and APPROVAL_FALSE's (approval ballot)

    >>> data = [['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]
    >>> expected = [[0, 1, ['NDP', 'Liberal', 'Green', 'CPC'], [1, 4, 2, 3],
    ...             [False, True, False, False]]]
    >>> clean_data(data)
    >>> data == expected
    True
    >>> data2 = [['0', '20', 'NDP', '1', 'YES']]
    >>> clean_data(data2)
    >>> data2 == [[0, 20, ['NDP'], [1], [True]]]
    True
    >>> data3 = [['-90', '-70', 'b;90', '2;1', 'NO;YES']]
    >>> clean_data(data3)
    >>> data3 == [[-90, -70, ['b', '90'], [2, 1], [False, True]]]
    True
    """
    for votes in data:
        votes[COL_RIDING] = int(votes[COL_RIDING])
        votes[COL_VOTER] = int(votes[COL_VOTER])
        votes[COL_RANK] = votes[COL_RANK].split(SEPARATOR)
        votes[COL_RANGE] = list(int(r) for r in votes[COL_RANGE].split(SEPARATOR
                                                                       ))
        new_approval = []
        for approval in votes[COL_APPROVAL].split(SEPARATOR):
            if approval == APPROVAL_TRUE:
                new_approval.append(True)
            else:
                new_approval.append(False)
        votes[COL_APPROVAL] = new_approval


###############################################################################
# Task 2: Data extraction
###############################################################################

def extract_column(data: List[list], column: int) -> list:
    """Return a list containing only the elements at index column for each
    sublist in data.

    Pre: each sublist of data has an item at index column.

    >>> extract_column([[1, 2, 3], [4, 5, 6]], 2)
    [3, 6]
    >>> extract_column([['NDP', 'ABLE', 'APPLE'], [0]], 0)
    ['NDP', 0]
    >>> extract_column([[70, 49, 8, 0], ['b', 'e', 'd', '4', 2], [4, [9, 8], 2], [True, False, True]], 1)
    [49, 'e', [9, 8], False]
    """
    extracted = []
    for values in data:
        extracted.append(values[column])
    return extracted


def extract_single_ballots(data: List['VoteData']) -> List[str]:
    """Return a list containing only the highest ranked candidate from
    each rank ballot in voting data data.

    Pre: data is a list of valid 'VoteData's
         The rank ballot is at index COL_RANK for each voter.

    >>> extract_single_ballots(SAMPLE_DATA_1)
    ['NDP', 'LIBERAL', 'GREEN', 'LIBERAL']
    >>> extract_single_ballots(SAMPLE_DATA_2)
    ['LIBERAL', 'GREEN', 'NDP']
    >>> extract_single_ballots(SAMPLE_DATA_3)
    ['NDP']
    >>> extract_single_ballots(SAMPLE_DATA_4)
    ['NDP', 'NDP', 'NDP', 'NDP', 'GREEN']
    """
    highest_ranked = []
    for values in data:
        highest_ranked.append(values[COL_RANK][0])
    return highest_ranked


def get_votes_in_riding(data: List['VoteData'],
                        riding: int) -> List['VoteData']:
    """Return a list containing only voting data for riding riding from
    voting data data.

    Pre: data is a list of valid 'VoteData's

    >>> expected = [[1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
    ...              [False, False, True, True]],
    ...             [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
    ...              [False, True, False, True]],
    ...             [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
    ...              [True, False, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_1, 1) == expected
    True
    >>> expected2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [4, 0, 5, 0],
    ...              [True, False, True, False]],
    ...             [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4, 5, 5, 5],
    ...              [True, True, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_2, 117) == expected2
    True
    >>> expected3 = []
    >>> get_votes_in_riding(SAMPLE_DATA_3, 1) == expected3
    True
    """
    riding_votes = []
    for values in data:
        if values[COL_RIDING] == riding:
            riding_votes.append(values)
    return riding_votes


###############################################################################
# Task 3.1: Plurality Voting System
###############################################################################

def voting_plurality(single_ballots: List[str],
                     party_order: List[str]) -> List[int]:
    """Return the total number of ballots cast for each party in
    single-candidate ballots single_ballots, in the order specified in
    party_order.

    Pre: each item in single_ballots appears in party_order

    >>> voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_1)
    [1, 3, 0, 1]
    >>> voting_plurality(['GREEN'], SAMPLE_ORDER_2)
    [0, 1, 0, 0]
    >>> voting_plurality([], [])
    []
    """
    total = len(party_order) * [0]
    for vote in single_ballots:
        i = party_order.index(vote)
        total[i] = total[i] + 1
    return total


###############################################################################
# Task 3.2: Approval Voting System
###############################################################################

# Note: even though the only thing we need from party_order in this
# function is its length, we still design all voting functions to
# receive party_order, for consistency and readability.
def voting_approval(approval_ballots: List[List[bool]],
                    party_order: List[str]) -> List[int]:
    """Return the total number of approvals for each party in approval
    ballots approval_ballots, in the order specified in party_order.

    Pre: len of each sublist of approval_ballots is len(party_order)
         the approvals in each ballot are specified in the order of party_order

    >>> voting_approval([[True, True, False, False],
    ...                  [False, False, False, True],
    ...                  [False, True, False, False]], SAMPLE_ORDER_1)
    [1, 2, 0, 1]
    >>> voting_approval([[True, True], [True, True], [False, False],
    ...                  [False, True], [True, True], [True, True],
    ...                  [False, True], [False, False]], ['YELLOW', 'GREEN'])
    [4, 6]
    >>> voting_approval([[]], [])
    []
    >>> voting_approval([[False]], ['GG'])
    [0]
    """
    total = len(party_order) * [0]
    i = 0
    while i < len(party_order):
        for values in approval_ballots:
            if values[i]:
                total[i] = total[i] + 1
            else:
                total[i] = total[i]
        i = i + 1

    return total


###############################################################################
# Task 3.3: Range Voting System
###############################################################################

def voting_range(range_ballots: List[List[int]],
                 party_order: List[str]) -> List[int]:
    """Return the total score for each party in range ballots
    range_ballots, in the order specified in party_order.

    Pre: len of each sublist of range_ballots is len(party_order)
         the scores in each ballot are specified in the order of party_order

    >>> voting_range([[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]],
    ...              SAMPLE_ORDER_1)
    [7, 12, 6, 8]
    >>> voting_range([[4, 0, 5, 0], [4, 5, 5, 5]], SAMPLE_ORDER_2)
    [8, 5, 10, 5]
    >>> voting_range([[0]], ['green'])
    [0]
    >>> voting_range([[]], [])
    []
    """
    total = len(party_order) * [0]
    i = 0
    while i < len(party_order):
        for votes in range_ballots:
            total[i] = total[i] + votes[i]
        i = i + 1
    return total

###############################################################################
# Task 3.4: Borda Count Voting System
###############################################################################

def voting_borda(rank_ballots: List[List[str]],
                 party_order: List[str]) -> List[int]:
    """Return the Borda count for each party in rank ballots rank_ballots,
    in the order specified in party_order.

    Pre: each ballot contains all and only elements of party_order

    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_1)
    [4, 4, 8, 2]
    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP']], SAMPLE_ORDER_2)
    [1, 2, 3, 0]
    >>> voting_borda([['YEL', 'BLU', 'ORA']], ['YEL', 'BLU', 'ORA'])
    [2, 1, 0]
    >>> voting_borda([[]], [])
    []
    >>> voting_borda([['a'], ['a']], ['a'])
    [0]
    """
    total = len(party_order) * [0]
    i = 0
    while i < len(party_order):
        for votes in rank_ballots:
            idx = party_order.index(votes[i])
            total[idx] = total[idx] + len(party_order) - 1 - i
        i = i + 1
    return total


###############################################################################
# Task 3.5: Instant Run-off Voting System
###############################################################################

def remove_party(rank_ballots: List[List[str]], party_to_remove: str) -> None:
    """Change rank ballots rank_ballots by removing the party
    party_to_remove from each ballot.

    Pre: party_to_remove is in all of the ballots in rank_ballots.

    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'GREEN', 'CPC'],
    ...             ['CPC', 'LIBERAL', 'GREEN'],
    ...             ['CPC', 'GREEN', 'LIBERAL']]
    True
    >>> v = [['YL', 'BLU', 'ORA'], ['BLU', 'YL', 'ORA'], ['YL', 'BLU', 'ORA']]
    >>> remove_party(v, 'ORA')
    >>> v == [['YL', 'BLU'], ['BLU', 'YL'], ['YL', 'BLU']]
    True
    >>> n = [['A'], ['A']]
    >>> remove_party(n, 'A')
    >>> n == [[], []]
    True
    """
    for votes in rank_ballots:
        votes.remove(party_to_remove)

def get_lowest(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the lowest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_lowest([16, 100, 4, 200], SAMPLE_ORDER_1)
    'LIBERAL'
    >>> get_lowest([16, 4, 4, 200], SAMPLE_ORDER_1)
    'GREEN'
    >>> get_lowest([0, 0, 0], ['a', 'b', 'c'])
    'a'
    >>> get_lowest([-1], ['b'])
    'b'
    """
    return party_order[party_tallies.index(min(party_tallies))]


def get_winner(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the highest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_winner([16, 100, 4, 200], SAMPLE_ORDER_1)
    'NDP'
    >>> get_winner([100, 100, 100, 100], SAMPLE_ORDER_2)
    'CPC'
    >>> get_winner([0], ['a'])
    'a'
    """

    return party_order[party_tallies.index(max(party_tallies))]


def voting_irv(rank_ballots: List[List[str]], party_order: List[str]) -> str:
    """Return the party which wins when IRV is performed on the list of
    rank ballots rank_ballots. Change rank_ballots and party_order as
    needed in IRV, removing parties that are eliminated in the
    process. Each ballot in rank_ballots is ordered by party_order.

    Pre: each ballot contains all and only elements of party_order
         len(rank_ballots) > 0

    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> voting_irv(ballots, order)
    'NDP'
    >>> ballots == [['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL']]
    True
    >>> order
    ['LIBERAL', 'NDP']
    >>> ord = ['a', 'b', 'c']
    >>> bal = [['a', 'b', 'c'], ['c', 'b', 'a']]
    >>> voting_irv(bal, ord)
    'c'
    >>> bal == [['c'], ['c']]
    True
    >>> ord == ['c']
    True
    >>> voting_irv([['v']], ['v'])
    'v'
    >>> voting_irv([['a', 'b'], ['a', 'b']], ['a', 'b'])
    'a'
    """
    while len(party_order) >= 1:
        min_votes = len(rank_ballots)//2 + 1
        firsts_list = []
        for vote in rank_ballots:
            firsts_list.append(vote[0])
        total_firsts = voting_plurality(firsts_list, party_order)
        for num in total_firsts:
            if num >= min_votes:
                return get_winner(total_firsts, party_order)
        party_to_remove = get_lowest(total_firsts, party_order)
        party_order.remove(party_to_remove)
        remove_party(rank_ballots, party_to_remove)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
