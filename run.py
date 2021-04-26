from flask import Flask, render_template, request, url_for, jsonify
from agent_env import *
import os

app = Flask(__name__)

# checa resultado
def Q_table_update():

    ##################### Criação da Tabela Q (antes) - PLAYER 1 ###################
    # Se não existe este Estado dentro da Tabela Q, adicione
    if str(env.board) not in agent_1.Q_table['states']:

        # 1-) Adicionar Estado Atual
        agent_1.Q_table['states'].append( str(env.board ) )

        # 2-) Add valor de Q
        agent_1.Q_table['Q'].append( [0,0,0,0,0,0,0,0,0] )
    ###############################################################
    

    # Registrar o State Inicial no PATH - Player 1
    agent_1.path['states'].append( str(env.board) )

# funct to start the game
def start():

    if env.check_result() != 2: # continua = 2, empate = 0, vitoria = 1, derrota = -1
        
        Q_table_update()
        
        # ( Desenha  Board )
        env.draw_board()
        
        
        print('UPDATED Q TABLE')

        # resultado do jogo
        agent_1.save_result( env.check_result() )

        # Valor da Recompensa
        reward_1 = env.reward( result = env.check_result(), reward_player = agent_1.reward_player  )
        
        # Update Q Table
        agent_1.update_Q( reward_1 )

        # Reset Game
        #env.reset_game()
        #agent_1.reset_game()

        # add partida jogada
        agent_1.number_match += 1

    else:

        Q_table_update()

        ############################ Agente Executa Ação no Ambiente #################### 
        # PLAYER 1
        env.select_pos_by_Q( agent_1.player,name = 'player '+str(agent_1.player),Q_table = agent_1.Q_table)
        #env.select_pos_by_random( agent_1.player, name = 'player '+str(agent_1.player) )  
        #env.select_pos_by_input( agent_1.player, name = 'player '+str(agent_1.player) )

        # ( Desenha  Board )
        env.draw_board()

            
        # Registrar o Action realizada no PATH
        agent_1.path['actions'].append( str(env.pos) )
            
        # Mudar jogador    
        #agent_1.player *= -1 # switch players

    
# LOAD
def load_Q_table():
    # Player 1
    with open('./trained_QxQ/Q_table_1.pkl', 'rb') as handle:
        Q_table_1 = pickle.load(handle)
    with open('./trained_QxQ/partidas_1.pkl', 'rb') as handle:
        number_match_1 = pickle.load(handle)

    agent_1.number_match = number_match_1
    agent_1.Q_table = Q_table_1
    #print(f"número de partidas {agent_1.number_match}")

## Player 1
agent_1 = Agent( 
    lr = 0.9,
    gamma = 0.1,
    reward_player = {
        'win': 1,
        'lost': -1,
        'draw': 0.05,  
                        # Valores Positivos você força ele a buscar empates... ( Ele buscará o empate quando você treinar muito... ele deixa que vencer)
                        # Valore Zero... você acomoda o sistema. (Vc ferra o Player 2)
    }
)

# Load Q Table
load_Q_table()

# Object Enviroment
env = Enviroment(
    epsilon =  0.0,
)

@app.route( '/reset', methods = ['POST'] )
def reset():
    env.reset_game()
    agent_1.reset_game()

    start()
    #board_python = { 'board' : board_python_to_js( list( env.board.flatten() ) ) }
    board_python = board_python_to_js( env.board.flatten() )
    return jsonify( board_python )

@app.route( '/', methods=["GET", "POST"] )
def index(  ):
    if request.method == 'POST':
        board_python = board_js_to_python( request.get_json()['board'] )
        env.board = np.reshape( board_python , (-1, 3)) # Volta para 2D, para atualizar tabela
        #if env.check_result() == 2: # Se não tem vitorioso, chama o ML para jogar.
        start()
        
        board_python = board_python_to_js( env.board.flatten() ) 
        #print(board_python)
        return jsonify( board_python )

    start()
    board_python = { 'board' : board_python_to_js( list( env.board.flatten() ) ) }
    #print(board_python)
    return render_template('index.html', board_python = board_python )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug = False)
    #app.run(debug=True)

