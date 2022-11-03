from queue import PriorityQueue
import numpy as np
from typing import List, Tuple
from random import shuffle

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    for i in range (len(scores)):
        for j in range (len(scores)):
            if gender_id[i] == "Male" and gender_pref[j] == "Women":
                scores[i][j] = 0
                scores[j][i] = 0
            if gender_id[i] == "Female" and gender_pref[j] == "Men":
                scores[i][j] = 0  
                scores[j][i] = 0         

            if gender_id[j] == "Male" and gender_pref[i] == "Women":
                scores[i][j] = 0
                scores[j][i] = 0
            if gender_id[j] == "Female" and gender_pref[i] == "Men":
                scores[i][j] = 0   
                scores[j][i] = 0  

    print(scores)
    shuffle(scores)

    n = len(scores) // 2

    proposer_rankings = []
    for i in range (n):
        i_rank = []
        for j in range (n):
            i_rank.append(j)
        i_rank = sorted(i_rank, key=lambda x: scores[i][x + n])
        proposer_rankings.append(i_rank)
    
    receiver_rankings = []
    for i in range (n):
        i_rank = []
        for j in range (n):
            i_rank.append((j))
        i_rank = sorted(i_rank, key=lambda x: scores[x])
        receiver_rankings.append(i_rank)

    matches = []

    proposer_status = []
    for i in range (n):
        proposer_status.append(i)

    receiver_status = []
    for i in range (n):
        receiver_status.append(-1)

    while proposer_status != []:
        print(matches)
        proposer = proposer_status.pop(0)
        for i in range (n):
            choice = proposer_rankings[proposer][i]
            if receiver_status[choice] == -1:
                matches.append((proposer, choice + n))
                receiver_status[choice] = proposer
                break
            elif receiver_rankings[choice].index(proposer) < receiver_rankings[choice].index(receiver_status[choice]):
                matches.append((proposer, choice + n))
                matches.remove((receiver_status[choice], choice + n))
                proposer_status.append(receiver_status[choice])
                receiver_status[choice] = proposer
                break
    
    print(matches)
    for match in matches:
        print(scores[match[0]][match[1]])
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
