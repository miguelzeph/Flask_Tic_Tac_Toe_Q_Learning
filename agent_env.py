import numpy as np
import random
import pandas as pd
import pickle
import os

###################### CLASSES ##########################
# Agent
class Agent(object):

    def __init__(self, lr, gamma, reward_player, ):
        
        self.reward_player = reward_player
        
        self.lr = lr
        
        self.gamma = gamma
        
        self.player = 1 # player 1 = 1 and player 2 = -1
        
        self.number_match = 0
        
        self.results ={
            'win':0,
            'draw':0,
            'lost':0}
        
        self.Q_table = {
            'states' : [],
            'actions': ['(0, 0)','(0, 1)','(0, 2)','(1, 0)','(1, 1)','(1, 2)','(2, 0)','(2, 1)','(2, 2)'],
            'Q': []
        }
        
        self.path = {
            'states':  [], # boards
            'actions': [], # posição no tabuleiro
        }
        
    def reset_game(self):
        self.player = 1
        self.path = {
            'states': [],
            'actions':[],
        }
    
    def reset_historic_game(self):
        self.results ={
            'win':0,
            'draw':0,
            'lost':0}
        
    def save_result(self, resultado):
        
        if resultado == 1:
            #print('venceu')
            self.results['win'] += 1
            
        elif resultado == -1:
            #print('perdeu')
            self.results['lost'] += 1

        else:
            #print('empate')
            self.results['draw'] += 1
            
    def Q_table_df(self):
        
        df = pd.DataFrame(
            index= self.Q_table['states'],
            columns= self.Q_table['actions'],
            data = self.Q_table['Q']
            )
            #data = 0 )
        return df
    
    def update_Q(self, reward):

        # Menor caminho para derrota, pontua mais. ( reward > 0 )
        # Maior caminho para derrota, perde menos. ( reward < 0)
        reward = reward / len(self.path['actions'])
        
        # Q(s,a) = Q(s,a) + alpha* ( R(s) + * Gamma * max_Q(s+1,:) - Q(s,a) ) )
        # R(s) = Reward...
        
        lr =    self.lr    # 0.9 # Alpha - Taxa de Aprendizagem
        gamma = self.gamma # 0.9 # Gamma - Fator de Desconto
        
        
        # Lista de Estados e Ações - Executados
        states_actions = list( self.path.values() )

        # Lista de Estados Reverso (pois iremos do FUTURO pro PASSADO)
        states =  list( reversed( states_actions[0] ) )

        # Lista de Ações Reverso   (pois iremos do FUTURO pro PASSADO)
        actions = list( reversed( states_actions[1] ) )

        # Marcador para eu saber onde estou
        index = 0
        for s2, a2 in zip( states, actions ):
            
            
            if reward >= 0: 

                try:
                    # index  = 0 é a ultima ação que levou a vitóriam, ou derrota
                    if index == 0:

                        s2 = self.Q_table['states'].index(str(s2))
                        a2 = self.Q_table['actions'].index(str(a2))

                        self.Q_table['Q'][s2][a2] = lr* ( reward ) #self.Q_table['Q'][s2][a2] = reward 


                        # Fazer o mesmo, mas agora para o States adiantado

                        ##### Next Value #####

                        # ESTADO avançado
                        index += 1

                        s1 = states[index]
                        s1 = self.Q_table['states'].index(str(s1))

                        a1 = actions[index]
                        a1 = self.Q_table['actions'].index(str(a1))

                        # a2 -> deixa em aberto, por que estamos interessado na ação com valor MÁXIMO do respectivo ESTADO avançado Max_Q(s+1,:)
                        self.Q_table['Q'][s1][a1] += lr*( 0 + gamma*np.max( self.Q_table['Q'][s2] ) - self.Q_table['Q'][s1][a1] )

                    else:

                        ##### pegar o index numérico dos States e Actions
                        s2 = self.Q_table['states'].index(str(s2))
                        a2 = self.Q_table['actions'].index(str(a2))


                        # Fazer o mesmo, mas agora para o States adiantado

                        ##### Next Value #####

                        # ESTADO avançado
                        index += 1

                        s1 = states[index]
                        s1 = self.Q_table['states'].index(str(s1))

                        a1 = actions[index]
                        a1 = self.Q_table['actions'].index(str(a1))

                        # a2 -> deixa em aberto, por que estamos interessado na ação com valor MÁXIMO do respectivo ESTADO avançado Max_Q(s+1,:)
                        self.Q_table['Q'][s1][a1] += lr*( 0 + gamma*np.max( self.Q_table['Q'][s2] ) - self.Q_table['Q'][s1][a1] ) 

                # Não há mais Estados Adiantados para buscar.   
                except IndexError:
                    continue
            
            
            if reward < 0:
            # Se for negativo tem que DESCONTAR, pra isso, usa-se o MIN_Q
                
                try:
                    # index  = 0 é a ultima ação que levou a vitóriam, ou derrota
                    if index == 0:

                        s2 = self.Q_table['states'].index(str(s2))
                        a2 = self.Q_table['actions'].index(str(a2))

                        self.Q_table['Q'][s2][a2] = lr* ( reward ) #self.Q_table['Q'][s2][a2] = reward 


                        # Fazer o mesmo, mas agora para o States adiantado

                        ##### Next Value #####

                        # ESTADO avançado
                        index += 1

                        s1 = states[index]
                        s1 = self.Q_table['states'].index(str(s1))

                        a1 = actions[index]
                        a1 = self.Q_table['actions'].index(str(a1))

                        # a2 -> deixa em aberto, por que estamos interessado na ação com valor MIN do respectivo ESTADO avançado Max_Q(s+1,:)
                        self.Q_table['Q'][s1][a1] += lr*( 0 + gamma*np.min( self.Q_table['Q'][s2] ) - self.Q_table['Q'][s1][a1] )

                    else:

                        ##### pegar o index numérico dos States e Actions
                        s2 = self.Q_table['states'].index(str(s2))
                        a2 = self.Q_table['actions'].index(str(a2))


                        # Fazer o mesmo, mas agora para o States adiantado

                        ##### Next Value #####

                        # ESTADO avançado
                        index += 1

                        s1 = states[index]
                        s1 = self.Q_table['states'].index(str(s1))

                        a1 = actions[index]
                        a1 = self.Q_table['actions'].index(str(a1))

                        # a2 -> deixa em aberto, por que estamos interessado na ação com valor MIN do respectivo ESTADO avançado Max_Q(s+1,:)
                        self.Q_table['Q'][s1][a1] += lr*( 0 + gamma*np.min( self.Q_table['Q'][s2] ) - self.Q_table['Q'][s1][a1] ) 
                        
                # Não há mais Estados Adiantados para buscar.   
                except IndexError:
                    continue

# Enviroment
class Enviroment(object):

    def __init__(self, epsilon):
        
        self.epsilon = epsilon
        

        # Board (é nosso ESTADO ATUAL)
        self.board = np.zeros((3,3))
        
        # pos jogada
        self.pos = 0

    def reset_game(self):
        self.board = np.zeros((3,3))

    # Plotar o Board
    def draw_board(self):

        draw = ''

        for i in range(3):
            for j in range(3):
                simbolo = ''
                # simbolo X (p1 = 1) ou O (p2 = -1)
                if self.board[i][j] == 1:
                    symbol = 'X'
                elif self.board[i][j] == -1:
                    symbol = 'O'
                else:
                    symbol = ' '

                draw += '|'+symbol+''

                if j == 2:

                    draw +='|\n-------\n'

        print(draw)

    # Posições disponíveis
    def available_moves(self):
        return np.argwhere(self.board == 0)
    # Jogar uma posição disponível
    def available_move_choice(self):
        return random.choice(self.available_moves())

    # Checar Resultado    
    def check_result(self):

        # Row
        if sum(self.board[0]) == 3 or sum(self.board[1]) == 3 or sum(self.board[2]) == 3:
            #print('venceu')
            return 1
        if sum(self.board[0]) == -3 or sum(self.board[1]) == -3 or sum(self.board[2]) == -3:
            #print('perdeu')
            return -1
        # Col
        if sum(self.board[:,0]) == 3 or sum(self.board[:,1]) == 3 or sum(self.board[:,2]) == 3:
            #print('venceu')
            return 1
        if sum(self.board[:,0]) == - 3 or sum(self.board[:,1]) == - 3 or sum(self.board[:,2]) == - 3:
            #print('perdeu')
            return -1
        # Diagonal
        if sum(self.board.diagonal()) == 3 or sum(np.fliplr(self.board).diagonal()) == 3:
            #print('venceu')
            return 1
        if sum(self.board.diagonal()) == -3 or sum(np.fliplr(self.board).diagonal()) == -3:
            #print('perdeu')
            return -1
        # Empate
        if not 0 in self.board:
            #print('empate')
            return 0
        
        return 2

        #########################################################
        ## continua = 2, empate = 0, vitoria = 1, derrota = -1 ##
        #########################################################

    # Dar recompensa        
    def reward(self, result, reward_player):

        if result == 1:  # Vitória
            return reward_player['win']

        if result == -1: # Derrota
            return reward_player['lost']
        
        if result == 0:  # Empate
            return reward_player['draw']
    
    # jogada - Random 
    def select_pos_by_random(self, player, name):
        
        row_col = self.available_move_choice()
        
        row = row_col[0] # Linha
        col = row_col[1] # Coluna

        self.board[row][col] = player
        
        self.pos = row,col
        
        #print(name + f' jogou na posição { str(self.pos) }')
           
    # jogada - humano   
    def select_pos_by_input(self, player, name):
        
        #os.system('clear')
        # desenhar jogada do player 
        #self.draw_board()
        while True:
            row = int( input('Row: ') )
            col = int( input('Col: ') )
            
            if [row,col] in self.available_moves().tolist(): # Refransforme Em lista... Array ele aceita 
                
                self.board[row][col] = player
                self.pos = row,col
                break
            else:
                input('try other position...')
    

    def select_pos_by_Q(self,player, name, Q_table):

        # Veja o estado atual seu (Seu board)... pegue a ação com maior Q
        
        
        # jogada Aleatória ( Exploring )
        if np.random.uniform(0, 1) < self.epsilon:
            
            #print('********jogada aleatória - Caiu no EPSILON ***********')
            
            self.select_pos_by_random( player, name = 'player '+str( player ) )


            #print('usando aleatório')

        # Vai na tabela e joga ( Exploiting )
        else:

            # Se existir esse estado gravado...

            if str(self.board) in Q_table['states']:


                #print('usando o Q')


                index_state = Q_table['states'].index( str(self.board) )
                #index_action= self.Q_table['Q'][index_state].index( str(np.max(self.Q_table['Q'][index_state])) )
                #index_qmax = np.argmax(self.Q_table['Q'][index_state])


                # pega todos valores de Q com respectivo index state na ordem DESCRESCENTE
                # assim, se a posição máx já estiver ocupada, ele vai pro segundo maior e assim por diante.

                #print(sorted( self.Q_table['Q'][index_state], reverse = True ) )
                #input()
                
                valores_qmax = sorted( Q_table['Q'][index_state], reverse = True )
                # pega o maior na ordem decrescente... 
                for qmax in valores_qmax:
                    
                    # logo se for Zero não temos estado treinado
                    #if qmax == 0:
                        
                        #print(f'********Jogada Aleatório - qmax = {qmax} ... não tem treino***********')
                        
                        #self.select_pos_by_random( player, name = 'player '+str( player ) )
                        #break
                        #return 'break'


                    index_qmax = Q_table['Q'][index_state].index( qmax )

                    action = Q_table['actions'][index_qmax]

                    row = int(action[1:2])
                    col = int(action[4:5])


                    if [row,col] in self.available_moves().tolist(): # Refransforme Em lista... Array ele aceita  

                        self.board[row][col] = player

                        self.pos = row,col
                        
                        #print(f'******** Jogada Inteligente - melhor Q:{qmax}***********')


                        #break
                        return 'break'



            # se não existir, joga aleatório mesmo
            else:
                
                #print('********Jogada Aleatória - Não existe este Estado***********')
                
                #print(str(self.board))
                
                self.select_pos_by_random( player, name = 'player '+str(player) )
#########################################################

###################### FUNÇÕES ##########################
# JS board     => ["X", "", "0", "", "X", "", "", "", "0"]
# Python board => [ [0,0,0], [0,-1,0], [0,0,0] ]

#Teste = ["X", "", "0", "", "X", "", "", "", "0"]

# Board List Js to Python
def board_js_to_python(board_list):

    new_board = []
    for element in board_list:
        if element == "":
            new_board.append(0.0)
        if element == "X":
            new_board.append(1.0)
        if element == "0":
            new_board.append(-1.0)

    return new_board

# Board List Python to JS
def board_python_to_js(board_list):

    new_board = []
    for element in board_list:
        if element == 0:
            new_board.append("")
        if element == 1:
            new_board.append("X")
        if element == -1:
            new_board.append("0")

    return new_board