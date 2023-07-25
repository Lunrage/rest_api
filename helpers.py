from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String
from sqlalchemy import text, bindparam
from sqlalchemy_utils import database_exists, create_database
import os.path
import json

class DBClass:
    def __init__(self):
        self.engine = create_engine("sqlite:///cakes_db", echo=True)
        self.meta = MetaData()
        self.conn = self.engine.connect()
        
    def createDatabase(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        print(database_exists(self.engine.url))

    def createCakesTable(self):
        self.cakes_table = Table(
           'cakes', self.meta, 
           Column('id', Integer, primary_key = True), 
           Column('name', String), 
           Column("price", Float),
           Column('description', String), 
        )

    def createAllTables(self):
        '''
        Creates the database and all the defined tables
        '''
        # Create the database:
        self.createDatabase()

        # Define the Cakes table:
        self.createCakesTable()

        # Create all the defined talbes:
        self.meta.create_all(self.engine)
        
        # check if file exists:
        file_path = './data/cakes.json'
        file_exist = os.path.isfile(file_path)
        if file_exist:
            # load initial cakes:
            self.loadInitialCakes(file_path)
        else:
            print("Cakes init file not found.")


    #*********************************************************************************************************************
    #    INSERT
    #*********************************************************************************************************************
    def saveCake(self, cake):
        name = cake.getName()
        price = cake.getPrice()
        description = cake.getDescription()
        result = self.insertCake(name, description, price)
        
        return result
    
    def insertCake(self, name, description, price):
        ins = self.cakes_table.insert().values(name=name, description=description, price=price)
        result = self.conn.execute(ins)
        
        return result.inserted_primary_key[0]

    #*********************************************************************************************************************
    #    SELECT
    #*********************************************************************************************************************
    def getAllCakes(self):
        sel = self.cakes_table.select()
        result = self.conn.execute(sel)
        my_res = result.all()
        
        if len(my_res) >= 1:
            return my_res
        else:
            return None

    def getCakeById(self, id1):
        sel = self.cakes_table.select().where(self.cakes_table.c.id==id1)
        result = self.conn.execute(sel)
        my_res = result.all()
        if len(my_res) >= 1:
            row = my_res[0]
            return row
        else:
            return None

    #*********************************************************************************************************************
    #    DELETE
    #*********************************************************************************************************************
    def deleteCake(self, id1):
        de = text("DELETE FROM "+ self.cakes_table.name +" WHERE "+ self.cakes_table.name +".id == :id")
        de = de.bindparams(bindparam("id", type_=Integer))
        result = self.conn.execute(de, {"id": id1})
        if result.rowcount >= 1:
            return True
        else:
            return False
        return result
    
    #*********************************************************************************************************************
    #    UPDATE
    #*********************************************************************************************************************
    def updateCake(self, id1, cake):
        nm = cake.getName()
        pr = cake.getPrice()
        des = cake.getDescription()
        up = text("UPDATE "+ self.cakes_table.name +" SET name = :name, price = :price, description = :description "
                  + "WHERE " + self.cakes_table.name +".id == :id")
        up = up.bindparams(bindparam("id", type_=Integer),
                           bindparam("name", type_=String),
                           bindparam("price", type_=Float),
                           bindparam("description", type_=String))
        result = self.conn.execute(up, {"id": id1, "name": nm, "price":pr, "description":des})
        if result.rowcount >= 1:
            return True
        else:
            return False
        return result
    
    #*********************************************************************************************************************
    #    MORE FUNCTIONS
    #*********************************************************************************************************************
    def loadInitialCakes(self, fp):
        file = open('data/cakes.json', "r")
        data = json.loads(file.read())
        cakes = data["cakes"]
        for cake in cakes:
            name = cake["name"]
            description = cake["description"]
            price = cake["price"]
            self.insertCake(name, description, price)
            
            
