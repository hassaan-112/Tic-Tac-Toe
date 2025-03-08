# before adding optimization to AI
import streamlit as st
import numpy as np
import random as r
import time


def random_move(board):
    if check_state(board)==0:
        return [5,5]
    i=r.randint(0,2)
    j=r.randint(0,2)
    if board[i,j]!=0:
        return random_move(board)
    else:
        return [i,j]

def optimized_ai(board):     # ai moves
    win_move=guess_location(board,2)
    prevention_move=guess_location(board,1)
    if win_move:
        return win_move
    elif prevention_move:
        return prevention_move
    else:
        return random_move(board)

    
def check_state(board):  # check for winning player
    for i in range(3): 
        if all(board[i,j]==1 for j in range (3)):#check rows for P1
            return 1
        if all(board[i,j]==2 for j in range (3)):#check rows for P2
            return 2
        if all(board[j,i]==1 for j in range (3)):#check cols for P1
            return 1
        if all(board[j,i]==2 for j in range (3)):#check cols for P2
            return 2
    if all(board[i,i]==1 for i in range (3)):#check main diag for 1
        return 1
    if all(board[i,i]==2 for i in range (3)):#check main diag for 2
        return 2
    if all(board[i,j]==1 for i,j in zip(range(3),range(2,-1,-1))):#check other diag for 1
        return 1
    if all(board[i,j]==2 for i,j in zip(range(3),range(2,-1,-1))):#check other diag for 2
        return 2    
    if not any(board[i, j] == 0 for i in range(3) for j in range(3)):
        return 0

def guess_location(board,typ):  # optimal move selector
    for i in range(3):
        if board[i,0]==typ and board[i,1]==typ and board[i,2]==0:    # check rows for optimal moves
            return [i,2]
        elif board[i,0]==typ and board[i,1]==0 and board[i,2]==typ:
            return [i,1]
        elif board[i,0]==0 and board[i,1]==typ and board[i,2]==typ:
            return [i,0]
            
        elif board[0,i]==typ and board[1,i]==typ and board[2,i]==0:  # check cols for optimal moves
            return [2,i]
        elif board[0,i]==typ and board[1,i]==0 and board[2,i]==typ:
            return [1,i]
        elif board[0,i]==0 and board[1,i]==typ and board[2,i]==typ:
            return [0,i]
            
    if board[0,0]==typ and board[1,1]==typ and board[2,2]==0:       # check main diag for optimal moves
        return [2,2]
    elif board[0,0]==typ and board[1,1]==0 and board[2,2]==typ:
        return [1,1]
    elif board[0,0]==0 and board[1,1]==typ and board[2,2]==typ:
        return [0,0]
        
    elif board[0,2]==typ and board[1,1]==typ and board[2,0]==0:  # check second diag for optimal moves
        return [2,0]
    elif board[0,2]==typ and board[1,1]==0 and board[2,0]==typ:
        return [1,1]
    elif board[0,2]==0 and board[1,1]==typ and board[2,0]==typ:
        return [0,2]
    return None
    

if 'board' not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)  
if 'current_player' not in st.session_state:
    st.session_state.current_player = 1  # Player 1 starts
if 'status' not in st.session_state:
    st.session_state.status = True  
if 'AI' not in st.session_state:
    st.session_state.AI=True
if 'selectbox_disabler' not in st.session_state:
    st.session_state.selectbox_disabler=False

#choice box for opponent selection
choice=st.selectbox(f"chose opponent {"AI" if st.session_state.AI else "Human"}",["AI","Human"],disabled=st.session_state.selectbox_disabler)
if choice=="Human":
    st.session_state.AI=False    
    
st.title("Tic-Tac-Toe")  # title

if check_state(st.session_state.board)==1:      # game status
    st.write("Player 1 won")
    st.session_state.status=False
elif(check_state(st.session_state.board)==2):
    st.write("Player 2 won")
    st.session_state.status=False
elif(check_state(st.session_state.board)==0):
    st.write("Draw")
    st.session_state.status=False

    
if st.session_state.current_player == 1 and st.session_state.status:   # turn indicator
    st.write("Player 1's turn") 
elif st.session_state.current_player == 2 and st.session_state.status and not st.session_state.AI:
    st.write("Player 2's turn") 
elif st.session_state.current_player == 2 and st.session_state.status and st.session_state.AI:
    st.write("AI's turn") 
    
for row in range(3):         # turn and save
    cols = st.columns(3)
    for col in range(3):
        cell_value = st.session_state.board[row, col]
        if cell_value == 0:
            label = " " 
        elif cell_value == 1:
            label = "X"  
        else:
            label = "O"
        if cols[col].button(label, key=f"{row}-{col}"):
            if st.session_state.board[row, col] == 0 and st.session_state.status:
                st.session_state.board[row, col] = st.session_state.current_player
                st.session_state.selectbox_disabler=True
                if st.session_state.current_player == 1 :
                    st.session_state.current_player = 2  
                else:
                    st.session_state.current_player=1
                st.rerun()
                
if st.session_state.AI and st.session_state.current_player==2 and  st.session_state.status:  # ai turn
    ret=optimized_ai(st.session_state.board)
    time.sleep(0.5)
    st.session_state.board[ret[0],ret[1]] =2
    st.session_state.current_player=1
    st.rerun()

if st.button("Reset"):   # reset button
    st.session_state.clear()
    st.rerun()
    
