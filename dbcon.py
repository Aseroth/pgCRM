import sqlite3
from sqlite3 import Error
import os

rel_dir = os.path.dirname(os.path.abspath(__file__))
dbfile = '{}\\baza.db'.format(rel_dir)


clientTable = '''CREATE TABLE IF NOT EXISTS client(
                id integer PRIMARY KEY,
                name text NOT NULL,
                adres text NOT NULL,
                phone text NOT NULL,
                mail text NOT NULL,
                ident text NOT NULL,
                type text NOT NULL,
                UNIQUE (ident)
                );'''

policyTable ='''CREATE TABLE IF NOT EXISTS policy(
                id integer PRIMARY KEY,
                number text NOT NULL,
                type text NOT NULL,
                company text NOT NULL,
                begin_date text NOT NULL,
                end_date text NOT NULL,
                cost integer NOT NULL,
                payment integer NOT NULL,
                client_id integer NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(id)
                
                );'''

carTable = '''CREATE TABLE IF NOT EXISTS cars(
                id integer PRIMARY KEY,
                carType, text
                carMake text,
                carModel text,
                carYear integer,
                carReg text,
                carVin text,
                policy_id integer,
                FOREIGN KEY (policy_id) REFERENCES policy(id),
                UNIQUE(carReg, carVin)
                );'''

instalmentsTable = '''CREATE TABLE IF NOT EXISTS instalments(
                id integer PRIMARY KEY,
                instalmentsNumber integer,
                paid bool,
                policy_id integer,
                client_id integer,
                FOREIGN KEY(policy_id) REFERENCES policy(id),
                FOREIGN KEY(client_id) REFERENCES clients(id)
                );'''

 #<---  TODO do uzupełenienia albo tabela z polisami o pojazd albo stworzyć tabele ubezpieczanych przedmiotów 9Pojazdy/nieruchomość )

class Connection:
    def __init__(self):
        global dbfile
        
        self.conn = None
        try:
            self.conn = sqlite3.connect(dbfile, check_same_thread=False)
            #print(sqlite3.version)
            #return self.conn
        except Error as err:
            print(err)

        #return self.conn

    def createTable_clients(self):
        global clientTable
        try:
            self.c = self.conn.cursor()
            self.c.execute(clientTable)
            self.state = True
        except Error as err:
            print(err)
            self.state = False
        return self.state
            

    def createTable_insure(self):
        global policyTable
        try:
            self.c = self.conn.cursor()
            self.c.execute(policyTable)
            state = True
        except Error as err:
            print(err)
            state = False
        
        return state
    
    def createTable_car(self):
        global carTable
        try:
            self.c = self.conn.cursor()
            self.c.execute(carTable)
            state = True
        except Error as err:
            print(err)
            state = False
        return state
    
    def createTable_instalments(self):
        global instalmentsTable
        try:
            self.c = self.conn.cursor()
            self.c.execute(instalmentsTable)
            state = True
        except Error as err:
            print(err)
            state = False
        return state


    def createClient(self, client):
        sql = '''INSERT INTO client(name, adres, phone, mail, ident, type) VALUES (?,?,?,?,?,?)'''
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, client)
            self.conn.commit()
            state = True
        except Error as err:
            print(err)
            state=False
        #return self.cur.lastrowid
        return state

    def createPolicy(self, policy):
        sql = '''INSERT INTO policy (number, type, company, begin_date, end_date, cost, payment, client_id) VALUES (?,?,?,?,?,?,?,?)'''
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, policy)
            self.conn.commit()
            print (self.cur.lastrowid)
        except Error as err:
            print(err)
            
        
        return self.cur.lastrowid
    
    def createCar(self, carData):
        sql = '''INSERT INTO cars (carType, carMake, carModel, carYear, carReg, carVin, policy_id) VALUES (?,?,?,?,?,?,?)'''
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, carData)
            self.conn.commit()
            state = True
        except Error as err:
            print(err)
            state = False
        return state

        #return self.cur.lastrowid

    def createInstalment(self, instalmentData):
        sql = '''INSERT INTO instalments (instalmentsNumber, paid, policy_id, client_id ) VALUES (?,?,?,?)'''
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, instalmentData)
            self.conn.commit()
            state = True
        except Error as err:
            print(err)
            state = False
        return state

    def updateClient(self, client):
        sql = '''UPDATE client
                SET name = ?,
                    adres = ?,
                    phone = ?, 
                    mail = ?,
                    ident = ?,
                    type = ?
                WHERE id = ?'''
        self.cur = self.conn.cursor()
        self.cur.execute(sql, client)
        self.conn.commit()
        
        return self.cur

    def updatePolicy(self, policy):
        sql = ''' UPDATE policy
                  SET number = ?,
                  company = ?,
                  begin_date=?,
                  end_date = ?,
                  cost = ?,
                  payment = ?,
                  client_id = ?
                WHERE id = ?'''
        
        self.cur = self.conn.cursor()
        self.cur.execute(sql, policy)
        self.conn.commit()

    def updateCar(self, carData):
        sql = ''' UPDATE cars
                  SET carType=?,
                  carMake = ?,
                  carModel = ?,
                  carYear = ?,
                  carReg = ?,
                  carVin= ?,
                  policy_id = ?
                  WHERE id = ?'''
        self.cur = self.conn.cursor()
        self.cur.execute(sql, carData)
        self.conn.commit()


    def deleteClient(self, clientID):
        sql = 'DELETE FROM client WHERE id=?'
        self.cur = self.conn.cursor()
        self.cur.execute(sql,(clientID,))
        self.conn.commit()

    def deletePolicy(self, policyID):
        sql = 'DELETE FROM policy WHERE id=?'
        self.cur = self.conn.cursor()
        self.cur.execute(sql, (policyID,))
        self.conn.commit()

    def printClients(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM client")
        data = self.cur.fetchall()
        self.client = []
        for row in data:
            self.client.append(row)


        return self.client
    
    def printPolicy(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM policy")
        data = self.cur.fetchall()
        self.policy = []
        for row in data:
            self.policy.append(row)

        return self.policy

    def printInstalments(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM instalments")
        data = self.cur.fetchall()
        self.instalmentsList = []
        for row in data:
            self.instalmentsList.append(row)

        return self.instalmentsList
    
    def printCars(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM cars")
        data = self.cur.fetchall()
        self.carsList = []
        for row in data:
            self.carsList.append(row)

        return self.carsList

    def searchClient(self, name):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT  * FROM client WHERE name = ?", (name, ))
        self.rows = self.cur.fetchall()

        for row in self.rows:
            print(row)
    
    def searchClientById(self, clientId):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM client WHERE id = ?", (clientId,))
        self.rows = self.cur.fetchall()
        self.editClient = []
        for row in self.rows:
            self.editClient.append(row)
        print(self.editClient)
        return self.editClient
    
    def serachPolicy(self, number):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT  * FROM policy WHERE number = ?", (number, ))
        self.rows = self.cur.fetchall()

        for row in self.rows:
            print(row)

    def searchClientPolicy(self, id):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM policy WHERE client_id = ?",(id,))
        self.rows = self.cur.fetchall()
        self.clientPolicy = []
        for row in self.rows:
            self.clientPolicy.append(row)

        return self.clientPolicy

    def searchPolicybyId(self, id):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM policy WHERE id = ?",(id,))
        self.rows = self.cur.fetchall()
        self.clientPolicybyId = []
        for row in self.rows:
            self.clientPolicybyId.append(row)
        
        return self.clientPolicybyId

