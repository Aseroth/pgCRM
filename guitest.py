from datetime import datetime
from matplotlib.pyplot import text
from numpy import double

import pglet
from pglet import Button, Checkbox, Column, Grid, Stack, Textbox, Text, Toolbar, toolbar, Dropdown, dropdown, Tabs, Tab, Panel, DatePicker, Html, Message, Dialog
import dbcon
from dbcon import *

class Person:
    def __init__(self,SQLID:int, name: str, adres: str, mail: str, phone: str, type: str, ident: str):
        self.SQLID = SQLID
        self.name = name
        self.adres = adres
        self.mail = mail
        self.phone = phone
        self.type = type
        self.ident = ident

class Polisa:
    def __init__(self, pSQLID: int, numer: str, rodzaj: str, towarzystwo: str, start:str, koniec:str, przypis:double, platnosc:int):
        self.pSQLID = pSQLID
        self.numer = numer
        self.rodzaj = rodzaj
        self.towarzystwo=towarzystwo
        self.start = start
        self.koniec = koniec
        self.przypis = przypis
        self.player = platnosc

#class Pojazd:
    #def __

def main(page):
#-----------------USTAWIENIE POŁĄCZENIA Z BAZĄ--------------------------------
    tabele = Connection()
    tabele.createTable_clients()
    tabele.createTable_insure()

    klienci = []
    
    if len(list(tabele.printClients()))>0:
        for x in range(len(list(tabele.printClients()))):
            klienci.append(list(tabele.printClients()[x]))
    
    polisyLista = []
    if len(list(tabele.printPolicy()))>0:
        for x in range(len(list(tabele.printPolicy()))):
            polisyLista.append(list(tabele.printPolicy()[x]))

#----------------------------------------------------            
    page.title = 'CRM'
    page.horizontal_align='start'
    page.update()

    grid = None



    #--------DODAWANIE KLIENTÓW DO BAZY
    def add_client(e):
        if len(klienci)==0:
            nextnumber = 1
        else:
            nextnumber = klienci[-1][0]+1
        grid.items.append(
            Person(
                SQLID=nextnumber,
                name = getName.value,
                adres = getAdres.value,
                mail = getMail.value,
                phone = getPhone.value,
                ident = getIdent.value,
                type = getType.value,
            ),
            
        )

        
        wpis = [nextnumber,getName.value, getAdres.value, getPhone.value, getMail.value, getIdent.value, getType.value]
        
        wpisSQL=[getName.value, getAdres.value, getPhone.value, getMail.value, getIdent.value, getType.value]
        #tabele.createClient(wpisSQL)
        if tabele.createClient(wpisSQL) == True:
            klienci.append(wpis)
            page.add(Message(value='Dodano klienta', dismiss=True, type='success'))
            
        elif tabele.createClient(wpisSQL) == False:
            page.add(Message(value='Błąd podczas dodawania klienta', dismiss=True, type='error'))
            
        getName.value=''
        getAdres.value=''
        getMail.value=''
        getPhone.value=''
        getIdent.value=''
        getType.value=''
        
        page.update()
        
#---------------------------------------------------
    def select_entry(e):
        add_policy.disabled = len(e.control.selected_items)==0
        show_policy.disabled = len(e.control.selected_items)==0
        edit_client.disabled = len(e.control.selected_items)==0
        delete_client.disabled = len(e.control.selected_items)==0

        add_policy.update()
        show_policy.update()
        edit_client.update()
        delete_client.update()

    def add_insur(e):
        insurePanel.open=True
        nrPolisy.value=''
        rodzajPolisy.value=''
        towarzystwo.value=''
        startPolisy.value=''
        koniecPolisy.value=''
        przypis.value=''
        platnosc.value=''
        page.update()
        
        
    def edit_entry(e):
        for choice in grid.selected_items:
            nrWpisu=choice.SQLID
            # TODO do uzupełnienia -> zaczytać dane z wybranego wpisu <- odwołać się do danych z SQL, dodać funkcje zapisu, możma zrobić panelem

    def save_insure(e):
        
        for choice in grid.selected_items:
            nrWpisu=choice.SQLID
        
        policyData = (nrPolisy.value, rodzajPolisy.value, towarzystwo.value, startPolisy.value, koniecPolisy.value, int(przypis.value), int(platnosc.value), nrWpisu)
        tabele.createPolicy(policyData)
        polisaLista = (nrPolisy.value, rodzajPolisy.value, towarzystwo.value, startPolisy.value, koniecPolisy.value, int(przypis.value), int(platnosc.value))
        polisyLista.append(polisaLista)
        page.update()

    def delete_client_entry(e):
        for choice in grid.selected_items:
            grid.items.remove(choice)
            tabele.deleteClient(choice.SQLID)
        page.update()
    
    def car_save(e):
        if rodzajPolisy.value=='Komunikacyjna':
            rodzajPojazdu.disabled=False
            markaPojazdu.disabled=False
            modelPojazdu.disabled=False
            rokProdukcji.disabled=False
            nrRejestracyjny.disabled=False
            nrVin.disabled = False
        else:
            rodzajPojazdu.disabled=True
            markaPojazdu.disabled=True
            modelPojazdu.disabled=True
            rokProdukcji.disabled=True
            nrRejestracyjny.disabled=True
            nrVin.disabled = True

        page.update()
        

    def show_insures(e):
        insureViewPanel.open=True
        for choice in grid.selected_items:
            nrWpisu=choice.SQLID

        polisy=tabele.searchClientPolicy(nrWpisu)
        
        panelListInsures.options.clear()
        if len(polisy)>0:
            for x in range(len(polisy)):
                panelListInsures.options.append(dropdown.Option('{} | {} | {}'.format(polisy[x][0],polisy[x][1], polisy[x][3])))
        
        page.update()

    def show_chosen_insure(e):
        for choice in grid.selected_items:
            nrWpisu=choice.SQLID

        polisy=tabele.searchClientPolicy(nrWpisu)
        id=int(panelListInsures.value[0])-1
        
        panelInsure.value=polisy[id][1]
        panelCompany.value=polisy[id][3]
        panelType.value=polisy[id][2]
        panelStart.value=polisy[id][4]
        panelEnd.value=polisy[id][5]
        panelCost.value=polisy[id][6]
        panelInstalments.value=polisy[id][7]

        page.update()

#-------PANEL DODAWANIE POLISY
    nrPolisy = Textbox(placeholder='Nr polisy')
    rodzajPolisy = Dropdown(width=180, on_change = car_save, options=[
        dropdown.Option('Komunikacyjna'),
        dropdown.Option('Mieszkaniowa'),
        dropdown.Option('Firmowa'),
        dropdown.Option('Życiowa'),
        dropdown.Option('Szkolna'),

    ])
    towarzystwo = Dropdown(width=180,  options=[
        dropdown.Option('PZU'),
        dropdown.Option('WARTA'),
        dropdown.Option('Ergo Hestia'),
        dropdown.Option('Allianz'),
        dropdown.Option('Compensa'),
        dropdown.Option('Interrisk'),
        dropdown.Option('TUW'),
        dropdown.Option('TUZ'),
        dropdown.Option('Proama'),
        dropdown.Option('Generali'),
        dropdown.Option('Link4'),
        dropdown.Option('Wefox'),
        dropdown.Option('Generali Agro'),
        dropdown.Option('Wiener'),
        ])
    
    startPolisy = Textbox(placeholder='Start polisy dd/mm/rrr')
    koniecPolisy = Textbox(placeholder='Koniec polisy dd/mm/rrr')
    przypis = Textbox(placeholder='Przypis składki')
    platnosc = Dropdown(width=180, options=[
        dropdown.Option('1'),
        dropdown.Option('2'),
        dropdown.Option('3'),
        dropdown.Option('4'),
        dropdown.Option('6'),
        dropdown.Option('12')
    ])

    rodzajPojazdu=Dropdown(width=180, disabled=True,  options=[
        dropdown.Option('Samochód osobowy'),
        dropdown.Option('Ciężarowy o DMC < 3,5 T'),
        dropdown.Option('Ciężarowy o DMC >3,5 T'),
        dropdown.Option('Ciągnik siodłowy'),
        dropdown.Option('Ciągnik rolniczy'),
        dropdown.Option('Przyczepa/naczepa'),
        dropdown.Option('Motor/skuter'),
        dropdown.Option('Autobus'),
        dropdown.Option('Quad'),
        dropdown.Option('Specjalny'),
        dropdown.Option('Inny'),
        ])
    markaPojazdu = Textbox(placeholder='Marka', disabled=True)
    modelPojazdu = Textbox(placeholder='Model pojazdu', disabled=True)
    rokProdukcji = Textbox(placeholder='Rok produkcji', disabled=True)
    nrRejestracyjny = Textbox(placeholder='Nr rejestracyjny', disabled=True)
    nrVin = Textbox(placeholder='Nr VIN', disabled=True)
    
    insurePanel = Panel(title='Dodaj polisę', controls=[
        nrPolisy,
        Text(value='Rodzaj polisy'),
        rodzajPolisy,
        Text(value='Towarzystwo ubezpieczeniowe'),
        towarzystwo,
        startPolisy,
        koniecPolisy,
        przypis,
        Text(value='Liczba rat'),
        platnosc,
        Text(value='Rodzaj pojazdu'),
        rodzajPojazdu,
        markaPojazdu,
        modelPojazdu,
        rokProdukcji,
        nrRejestracyjny,
        nrVin,
        Button('Dodaj polise', on_click=save_insure)
    ])


#------PANEL POLISY KLIENTA---------
    panelListInsures = Dropdown(width=180, disabled=False, on_change=show_chosen_insure, options = [])
    panelInsure = Textbox(value='', read_only=True)
    panelCompany = Textbox(value='', read_only=True)
    panelType = Textbox(value='', read_only=True)
    panelStart=Textbox(value='', read_only=True)
    panelEnd=Textbox(value='', read_only=True)
    panelCost=Textbox(value='', read_only=True)
    panelInstalments=Textbox(value='', read_only=True)
    
    kontolki = Stack(controls=[
        Text(value='Wybierz polisę'),
        panelListInsures,
        Text(value='Nr polisy: '),
        panelInsure,
        Text(value='\nRodzaj polisy: '),
        panelType,
        Text(value='\nTowarzystwo ubezpieczeniowe: '),
        panelCompany,
        Text(value='\nStart polisy: '),
        panelStart,
        Text(value='\nKoniec polisy: '),
        panelEnd,
        Text(value='\nPrzypis: '),
        panelCost,
        Text(value='\nLiczba rat: '),
        panelInstalments,
    ])
         
    insureViewPanel = Panel(title='Polisy klienta', controls=[
        kontolki
    ])


#--------- PRZYBORNIK KLIENTA---------------

    add_policy = toolbar.Item(
        text='Dodaj polise', icon='PageHeaderEdit', disabled=True, on_click=add_insur
    )
    show_policy = toolbar.Item(
        text='Polisy klienta', icon='ExploreContent', disabled=True, on_click=show_insures
    )
    edit_client = toolbar.Item(
        text='Edytuj klienta', icon='Edit', disabled=True, on_click=edit_entry
    )
    delete_client = toolbar.Item(
        text='Usuń klienta', icon='Delete', disabled=True, on_click=delete_client_entry)

    grid_toolbar = Toolbar(items=[add_policy, show_policy, edit_client, delete_client])
    
#---------------- TABELA KLIENTÓW

    grid = Grid(
        selection_mode='single',
        compact= True,
        header_visible=True,
        columns=[
            Column(resizable=True, min_width=20, max_width=50, name='ID', template_controls=[Text(value='{SQLID}')]),
            Column(resizable=True,min_width=350,max_width=400 ,name='Nazwa', template_controls=[Text(value='{name}')]),
            Column(resizable=True,min_width=250,max_width=400 ,name='Adres', template_controls=[Text(value='{adres}')]),
            Column(resizable=True,min_width=100,max_width=150 ,name='Telefon', template_controls=[Text(value='{phone}')]),
            Column(resizable=True,min_width=250,max_width=350 ,name='Mail', template_controls=[Text(value='{mail}')]),
            Column(resizable=True,max_width=200 ,name='Pesel/Regon', template_controls=[Text(value='{ident}')]),
            Column(resizable=True,min_width=100,max_width=150 ,name='Rodzaj', template_controls=[Text(value='{type}')]),
            ],
        items = [
            
        ],
        margin=0,
        on_select=select_entry,

    )
#-----------------------------------------

#----- UZUPEŁNIANIE TABELI WPISAMI Z BAZY SQLITE
    for x in range(len(klienci)):
        grid.items.append(
            Person(
                SQLID = klienci[x][0],
                name = klienci[x][1], #nazwa
                adres = klienci[x][2], #adres
                mail = klienci[x][4], #mail
                phone = klienci[x][3], #telefon
                ident = klienci[x][5], #id klienta
                type = klienci[x][6], # typ klienta

                
            ),
        )

#----------------TABELA POLIS--------------------

    polisyGrid = Grid(
        selection_mode= 'single',
        compact= True,
        header_visible= True,
        columns=[
            Column(resizable=True, min_width=20, max_width=50, name='ID', template_controls=[Text(value='{pSQLid}')]),
            Column(resizable=True,min_width=150,max_width=220 ,name='Numer polisy', sort_field=True ,template_controls=[Text(value='{numer}')]),
            Column(resizable=True,min_width=150,max_width=250 ,name='Rodzaj', template_controls=[Text(value='{rodzaj}')]),
            Column(resizable=True,min_width=100,max_width=150, field_name='Towarzystwo',sort_field=True , template_controls=[Text(value='{towarzystwo}')]),
            Column(resizable=True,min_width=150,max_width=200 ,name='Start polisy', template_controls=[Text(value='{start}')]),
            Column(resizable=True,min_width=150,max_width=200,name='Koniec polisy', template_controls=[Text(value='{koniec}')]),
            Column(resizable=True,min_width=100,max_width=150 ,name='Przypis', template_controls=[Text(value='{przypis}')]),
            Column(resizable=True,min_width=100,max_width=250 ,name='Schemat płatności', template_controls=[Text(value='{platnosc}')]),
        ],
        items=[

        ],
        margin=0,
    )

    for x in range(len(polisyLista)):
        polisyGrid.items.append(
            Polisa(
                pSQLID=polisyLista[x][0],
                numer = polisyLista[x][1],
                rodzaj = polisyLista[x][2],
                towarzystwo=polisyLista[x][3],
                start=polisyLista[x][4],
                koniec=polisyLista[x][5],
                przypis=polisyLista[x][6],
                platnosc=polisyLista[x][7],
            ),
        )

    #insure_grid = 

    
#--------FORMULARZ DODAWANIA KLIENTA
    
    getName = Textbox(placeholder='Nazwa klienta')
    getAdres = Textbox(placeholder='Adres klienta')
    getMail = Textbox(placeholder='Mail klienta')
    getPhone = Textbox(placeholder='Telefon klienta')
    getIdent = Textbox(placeholder='Pesel/Regon klienta')
    getType = Dropdown(width=180, options=[
            dropdown.Option('Osoba fizyczna'),
            dropdown.Option('Osoba Prawna'),
            dropdown.Option('Jednoosobowa działalnośc gosp.'),
            ])
    



#---------------STRONA GŁÓWNA---------------

    liczba_klientow = len(klienci)
    data = datetime.now()
    day = data.day
    month = data.month
    if month <10:
        month='0'+str(month)
    year = data.year
    frontPanel = Stack(horizontal=False, controls=[
        Text(value='Liczba polis kończących się w ciągu 30 dni: ', size='large', bold=True),
        Text(value='Przypis łączny od początku roku: ', size='large', bold=True),
        Text(value='Przypis łączny w roku ubiegłym: ', size='large',bold=True),
        Text(value='Liczba polis od poczatku roku: ', size='large', bold=True),
        
    ])

    def endingInsure():
        pass

#-------- ZAKŁADKI MENU GŁÓWNEGO

    mainMenu = Tabs(
        solid = True,
        margin = '10px',
        tabs = [
            Tab(
                text='Strona główna',
                icon='Home',
                controls=[ Stack( horizontal=False, controls=[
                    frontPanel,
                    ],
                    ),
                ],
            
            ),
            Tab(
                text='Klienci',
                icon='People',
                #count=nrClients(),
                controls=[
                    grid_toolbar,
                    grid,
                    Text("Dodaj klienta", size='medium'),
                    Stack(horizontal=True, controls=[
                            getName,
                            getAdres,
                            getMail,
                            getPhone,
                            getIdent,
                            getType,
                            Button('Dodaj klienta', on_click=add_client),
                        ]),
                    
                ]),
            Tab(
                text='Polisy',
                icon='DocumentSet',
                #count=len(polisy),
                controls=[
                    polisyGrid,
                ],
                ),
        ]
    )

    page.add(
        mainMenu,
        insurePanel,
        insureViewPanel,
        
    )

print(datetime.now)
pglet.app('test-crm', target=main)