import dbcon
from dbcon import *
from tabulate import tabulate

testy = Connection()
klienci = None
polisy = None

def read_clients():
    global klienci
    klienci = testy.printClients()
    return klienci

def read_polisy():
    global polisy
    polisy = testy.printPolicy()
    return polisy

def clients_print():
    print(tabulate(read_clients(), headers=["ID", "Nazwa", 'Adres', 'Telefon', 'Mail','Pesel', 'Rodzaj']))

def polisy_print():
    print(tabulate(read_polisy(), headers=['ID', 'Nr polisy', 'Rodzaj', 'Towarzystwo', 'Okres od', 'Okres do', 'Przypis', 'Liczba rat', 'ID klienta']))


polisy_print()