import pymongo
from pymongo import MongoClient
### Não esqueça ### pip install pymongo dnspython

try: # Local
    arq = open('./.key','r')
    key = arq.readline()
    cluster = MongoClient( str( key ) )
    arq.close()
except FileNotFoundError: # Heroku
    key = str( os.environ['MONGO_DB_KEY'] )
    cluster = MongoClient( key )

db = cluster( "TicTacToeReinforcementLearning" ) # Cluster
collection = db[ "TicTacToeReinforcementLearning"] # Dentro do Cluster temos a Coleção
################################################
################################################


Q_table_db = {
    'id': 404,
    'states': 'teste...' ,
    'actions': 'teste...' ,
    'Q': 'teste...' ,  
}

collection.insert_one( Q_table_db )
