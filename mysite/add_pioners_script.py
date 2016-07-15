__author__ = 'Insolia'

from bank.models import *
import csv
from transliterate import translit
from django.contrib.auth.models import Group


def get_pd(str):
    return '111'


p_f = open('meta_files/pioners.csv')
p_out = open('meta_files/logins.txt', 'w')

g = Group.objects.get(name='pioner')

for p in csv.reader(p_f):
    ln = p[0].decode('utf-8')
    fn = p[1].decode('utf-8')
    tn = p[2].decode('utf-8')
    otr = p[3].decode('utf-8')
    grad = p[4].decode('utf-8')

    login = translit(fn[0], 'ru', reversed=True) + translit(tn[0], 'ru', reversed=True) + translit(ln, 'ru',
                                                                                                   reversed=True)
    login = login.lower()
    pd = get_pd(login)

    new_u = User(first_name=fn, last_name=ln, username=login, password=pd)
    new_u.save()
    g.user_set.add(new_u)
    new_a = Account(user=new_u, third_name=tn, grade=grad)
    new_a.save()

    print ln + ' ' + fn + '\n' + 'login: ' + login + ' password: ' + pd
    info = ln + ' ' + fn + '\n' + 'login: ' + login + ' password: ' + pd

    p_out.write(info.encode('utf-8'))
    p_out.write('\n\n')

