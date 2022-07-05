import pglet
from pglet import Button, Checkbox, Column, Grid, Stack, Textbox, Text, Toolbar, toolbar, Dropdown, dropdown, Tabs, Tab, Panel, DatePicker, Html, Message, Dialog
import dbcon
from dbcon import *
from identcheck import mainCheck






class Person:
    def __init__(self,SQLID:int, name: str, adres: str, mail: str, phone: str, type: str, ident: str):
        self.SQLID = SQLID
        self.name = name
        self.adres = adres
        self.mail = mail
        self.phone = phone
        self.type = type
        self.ident = ident

tabele = Connection()
tabele.createTable_clients()

klienci = []
if len(list(tabele.printClients()))>0:
    for x in range(len(list(tabele.printClients()))):
        klienci.append(list(tabele.printClients()[x]))


grid  = None
