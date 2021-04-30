import pymongo
from pymongo import MongoClient
### Não esqueça ### pip install pymongo dnspython

# Guardar o link em um arquivo de segurança
arq = open('./.key','r')
key = arq.readline()
arq.close()


cluster = MongoClient( str( key ) )
db = cluster["TicTacToeReinforcementLearning" ] # Cluster
collection = db[ "TicTacToeReinforcementLearning"] # Dentro do Cluster temos a Coleção

# VALORES
Q_table_db = {
    #'_id': 1, # Se não criar, o próprio DB cria um automáticamente
    'states': 'teste...' ,
    'actions': 'teste...' ,
    'Q': 'teste...' ,  
}
print('okay')
# CREATE OBJECT IN MONGO DB (Exemplo)
collection.insert_one( Q_table_db ) 

"""
# UPDATE MONGO DB
from bson.objectid import ObjectId
id_object = {"_id" : ObjectId("608b189fe511655ac0d27dc4")} # Pega o id no site do MONGODB
new_information = {"$set":Q_table_db}
collection.find_one_and_update( id_object , new_information, upsert=True )
"""

# Load arquivo do MONGODB
#from bson.objectid import ObjectId
#Q_table_db = collection.find_one( {'_id': ObjectId("608b189fe511655ac0d27dc4") } )


""" ############ Não deu CErto....
# Mandar um Pickle, pois é mais leve que um Array
import pickle
doc = {
    '_id' : 11112, # SE Já existir esse _id... ele dá BUG
    'pickled' : pickle.dumps( Q_table_db )
    }
collection.insert_one( doc )


# Load um Pickle
from bson.binary import Binary
x = collection.find_one( {'_id':11112} ) # find_one ( ) tem também find( )
"""