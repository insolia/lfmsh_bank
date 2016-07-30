# coding=utf-8


zaryadka_budget = 40.
p2p_buf = 40.
p2p_proc = 0.7
daily_tax = -20
sem_needed = 18
activity_money = {1 : 20, 2: 15, 3: 10, 4: 5}

from models import *
from dal import autocomplete



class PionerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return 0

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(last_name__istartswith=self.q)

        return qs




def zaryadka(num_of_attendants):
    if num_of_attendants != 0:
        return max(1, zaryadka_budget / num_of_attendants)
    return 0

def seminar(score):
    if score >0:
        return score*5
    else:
        return score * 10

def lec_pen(missed):
    return (missed+1) * 10

def get_tax_desc():
    return unicode('Неизбежны только смерть и налоги.','utf-8')
