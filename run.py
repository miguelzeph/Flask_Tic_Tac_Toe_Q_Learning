from flask import Flask, render_template, request, url_for, jsonify
from agent_env import *
import os

app = Flask(__name__)

def check():
    if env.check_result() != 2: # continua = 2, empate = 0, vitoria = 1, derrota = -1

        # resultado do jogo
        agent_1.save_result( env.check_result() )

        # Valor da Recompensa
        reward_1 = env.reward( result = env.check_result(), reward_player = agent_1.reward_player  )
        
        # Update Q Table
        agent_1.update_Q( reward_1 )

        # Reset Game - Criei uma view func para isso
        #env.reset_game()
        #agent_1.reset_game()

        # add partida jogada
        agent_1.number_match += 1

        return 'break'

# funct to start the game
def start():

    # Jogada inicial e Jogada Player JavaScript
    #env.draw_board()

    # Primeiro Check - Jogada por Click
    if check() == 'break':
        return 'fim da func Start()'
    
    ################ Criação da Tabela Q (antes) - PLAYER 1 ###################
    # Se não existe este Estado dentro da Tabela Q, adicione
    if str(env.board) not in agent_1.Q_table['states']:

        # 1-) Adicionar Estado Atual
        agent_1.Q_table['states'].append( str(env.board ) )

        # 2-) Add valor de Q
        agent_1.Q_table['Q'].append( [99998,11111,99995,11112,99999,11113,99996,11114,99997] )
    ############################################################################
    
    # Registrar o State Inicial no PATH - Player 1
    agent_1.path['states'].append( str(env.board) )

    ################### Agente Executa Ação no Ambiente ######################## 
    # PLAYER 1
    env.select_pos_by_Q( agent_1.player,name = 'player '+str(agent_1.player),Q_table = agent_1.Q_table)
    #env.select_pos_by_random( agent_1.player, name = 'player '+str(agent_1.player) )  
    #env.select_pos_by_input( agent_1.player, name = 'player '+str(agent_1.player) )

    # ( Desenha  Board )
    #env.draw_board()

    # Registrar o Action realizada no PATH
    agent_1.path['actions'].append( str(env.pos) )
        
    # Mudar jogador    
    #agent_1.player *= -1 # switch players

    # Segundo Check é a Jogada por ML 
    if check() == 'break':
        return 'fim da func Start()'
    
# LOAD
def load_Q_table():
    # Player 1
    with open('./trained_QxQ/Q_table_1.pkl', 'rb') as handle:
        Q_table_1 = pickle.load(handle)
    with open('./trained_QxQ/partidas_1.pkl', 'rb') as handle:
        number_match_1 = pickle.load(handle)
    agent_1.Q_table = Q_table_1
    agent_1.number_match = number_match_1

## Player 1
agent_1 = Agent( 
    lr = 0.9,
    gamma = 0.9,
    reward_player = {
        'win': 1000,
        'lost': -100000,
        'draw': -10000,  
    }
)



# Object Enviroment
env = Enviroment(
    epsilon =  0.0,
)

###########################################
################# MONGO DB ################
import pymongo
from pymongo import MongoClient
### Não esqueça ### ---> pip install pymongo dnspython
from bson.objectid import ObjectId # para update o object já criado no MongodB Atlas

try: # Local
    arq = open('./.key','r')
    key = arq.readline()
    cluster = MongoClient( str( key ) )
    arq.close()
except FileNotFoundError: # Heroku
    key = str( os.environ['MONGO_DB_KEY'] )
    cluster = MongoClient( key )

db = cluster["TicTacToeReinforcementLearning"] # Cluster
collection = db["TicTacToeReinforcementLearning"] # Dentro do Cluster temos a Coleção
###########################################
###########################################



try: 
    print('Load Q_table pelo MongoDB')
    # Load mongoDB - Q Table para Agent 1 object 
    from bson.objectid import ObjectId
    Q_table_db = collection.find_one( {'_id': ObjectId("608b189fe511655ac0d27dc4") } )

    agent_1.Q_table['states'] = Q_table_db['states']
    agent_1.Q_table['actions'] = Q_table_db['actions']
    agent_1.Q_table['Q'] = Q_table_db['Q']
except:
    # Load Q Table pelo arquivo mesmo 
    print('Load Q_table pelo ARQUIVO')
    load_Q_table()


@app.route( '/start_game', methods = ['POST'] )
def start_game():
    start()
    board_python = board_python_to_js( env.board.flatten() )
    return jsonify( board_python )

@app.route( '/reset_game', methods = ['POST'] )
def reset_game():

    # Reseta o Game
    env.reset_game()
    agent_1.reset_game()
    # Já realiza outra jogada
    start()
    board_python = board_python_to_js( env.board.flatten() )
    return jsonify( board_python )

@app.route( '/', methods=["GET", "POST"] )
def index( ):
    if request.method == 'POST':
        board_python = board_js_to_python( request.get_json()['board'] ) # 1D
        # Volta para matriz 3x3 e atualiza o Objecto ENV BOARD
        env.board = np.reshape( board_python , (-1, 3))
        # Realiza uma jogada
        start()
        board_python = board_python_to_js( env.board.flatten() ) # flatten() -> transforma qualquer matriz em 1D
        return jsonify( board_python )
    board_python = { 'board' : board_python_to_js( list( env.board.flatten() ) ) }
    return render_template('index.html', board_python = board_python )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug = False)
    #app.run(debug=True)

"""
print( "Salvando a Q table no mongodb...")
####### Quando Fechar o Flask, ele Salva os novos Valores da Q Table. #######
Q_table_db = {
'states': agent_1.Q_table['states'] ,
'actions': agent_1.Q_table['actions'] ,
'Q': agent_1.Q_table['Q'] ,  
}
id_object = {"_id" : ObjectId("608b189fe511655ac0d27dc4")} # Pega o id no site do MONGODB
new_information = {"$set":Q_table_db}
collection.find_one_and_update( 
    id_object ,
    new_information,
    upsert=True 
    )
"""
