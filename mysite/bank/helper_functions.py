zaryadka_budget = 40
max_p2p_sum = 100
p2p_proc = 0.7


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
        return zaryadka_budget / num_of_attendants
    return 0

def seminar(score):
    return score // 2
