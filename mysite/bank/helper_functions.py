zaryadka_budget = 40
max_p2p_sum = 100



def zaryadka(num_of_attendants):
    if num_of_attendants != 0:
        return zaryadka_budget / num_of_attendants
    return 0

def seminar(score):
    return score / 2
