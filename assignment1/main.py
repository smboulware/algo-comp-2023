#!usr/bin/env python3
import json
import sys
import os
from urllib import response
import numpy as np

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

def scoring_function(user1, user2, response_dist):
    """
    Score function: Set baseline as 20 to prevent negatives.
    Then increase score for matching answers and decrease scores
    for different answers according to the functions from the notes.
    Divide by 40 as max addition/subtraction is 20.
    """
    score = 20
    for i in range(19):
        if user1.responses[i] == user2.responses[i]:
            score += 1 / (1 + response_dist[i][user1.responses[i]])
        else: 
            score -= 1 / (1 + np.sqrt(response_dist[i][user1.responses[i]] * response_dist[i][user2.responses[i]]))
    return score / 40

def year_compatibility(user1, user2):
    """
    Year compatibility: More compatibility the closer the year
    difference is. The multipler only ranges from 0.8 to 1 as
    the responses should have a higher weight than the year.
    """
    match = 1 - np.abs(user1.grad_year - user2.grad_year) * 0.05
    return match


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2, response_dist):
    # Gender compatability: users must fit each others preferences in order to match
    if user1.gender not in user2.preferences:
        return 0
    if user2.gender not in user1.preferences:
        return 0


    score = scoring_function(user1, user2, response_dist)
    score *= year_compatibility(user1, user2)
    
    return score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    response_dist = np.zeros((20,6))

    for i in range(20):
        for j in range(len(users)-1):
            response_dist[i][(users[j].responses[i])] += 1
        for j in range(6):
            response_dist[i][j] = response_dist[i][j]/len(users)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2, response_dist)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
