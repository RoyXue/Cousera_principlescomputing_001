"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    sum_score = []
    if hand is None:
        return 0
    else:
        for num in hand:
            count = 0
            for order in range(len(hand)):
                if hand[order] == num:
                    count += num
            sum_score.append(count)
        return max(sum_score)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    possible = gen_all_sequences(range(1, num_die_sides+1), num_free_dice)
    rank = 0

    for pos_set in possible:
        all_set = list(held_dice) + list(pos_set)
        rank += score(all_set)
    return float(rank)/len(possible)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    stack = set([()])

    if len(hand) == 0:
        return stack
    else:
        temp = hand[:-1]
        for pos in gen_all_holds(temp):
            stack.add(pos)
            stack.add((pos + (hand[-1],)))

    return stack



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    holds = {}
    possible = gen_all_holds(hand)

    for each_hold in possible:
        each_hold_val = expected_value(each_hold, num_die_sides, len(hand) - len(each_hold))
        holds[each_hold] = holds.get(each_hold, each_hold_val)

    temp = []
    for key, value in holds.items():
        temp.append((value, key))

    return sorted(temp, reverse = True)[0]


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

#import user35_U2vQEq960r_0 as tests

#tests.test_score(score)  
#tests.test_expected_value(expected_value)
#tests.test_strategy(strategy) 

#import user35_uLOFnLQSJV29rFh_5 as expected_value_testsuite
#expected_value_testsuite.run_suite(expected_value)

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)


    
    
    



