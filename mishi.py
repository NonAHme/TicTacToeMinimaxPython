from math import inf as infinity
from random import choice
import platform
import time
from os import system
from tkinter import *
import tkinter.messagebox
tk = Tk()
tk.title("MishiCatIA")

bclick = True

h_choice = 'X'  # X or O
c_choice = 'O'  # X or O
first = 'Y'  # if human is the first

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """Hace match si el jugador hizo 3 en raya con algunos de esos estados"""
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    state-> El estado del tablero
    retorna -> Si existe un Ganador 
     """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    state-> El estado del tablero
    retona una lista de Cell si estas estan vacias 
    """
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if(cell == 0):
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    Recibe las coordenadas en el tablero de una celda y retorna si esta vacia o no
    """
    cell = [x, y]
    if cell in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def human_turn(number_cell):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    # tkinter.messagebox.showinfo("","celda no.:"+str(number_cell))
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return


    # Dictionary of valid moves
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    if number_cell < 1 or number_cell > 9:
        tkinter.messagebox.showinfo("Casilla no valida")
        return False

    coord = moves[number_cell]
    # tkinter.messagebox.showinfo(
    #     "Coordenadas", " x:"+str(coord[0])+" y:"+str(coord[1]))
    if not valid_move(coord[0], coord[1]):
        tkinter.messagebox.showinfo("Casilla no valida")
        return False
    return set_move(coord[0], coord[1], HUMAN)


def ai_turn(c_choice, h_choice):
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)
    # tkinter.messagebox.showinfo("","Las coordenadas de IA son: x:"+str(move[0])+" y:"+str(move[1]))
    return move

def btnClick(buttons):
    if len(empty_cells(board)) <= 1 or  game_over(board):
        if wins(board, HUMAN):
            tkinter.messagebox.showinfo("Partida terminada","Gano Humano")
        elif wins(board,COMP):
            tkinter.messagebox.showinfo("Partida terminada","Gano MISHI")
        else:
            tkinter.messagebox.showinfo("Partida terminada","Empate")
        tk.destroy() #Destruye la ventana
        global bclick
    if buttons["text"] == " " and bclick == True:
        buttons["text"] = "X"
        bclick = False
        human_turn(buttonToNumber(buttons))
        coords = ai_turn(c_choice, h_choice)
        numberToButton(coords)["text"] = "O"
        bclick = True
    # tkinter.messagebox.showinfo("Celdas vacias?",str(len(empty_cells(board))))
    # tkinter.messagebox.showinfo("Game Over?",str(game_over(board)))

def disableButton():
    button1.configure(state=DISABLED)
    button2.configure(state=DISABLED)
    button3.configure(state=DISABLED)
    button4.configure(state=DISABLED)
    button5.configure(state=DISABLED)
    button6.configure(state=DISABLED)
    button7.configure(state=DISABLED)
    button8.configure(state=DISABLED)
    button9.configure(state=DISABLED)


def buttonToNumber(buttons):
    numButton = -1
    if button1 == buttons:
        numButton = 1
    if button2 == buttons:
        numButton = 2
    if button3 == buttons:
        numButton = 3
    if button4 == buttons:
        numButton = 4
    if button5 == buttons:
        numButton = 5
    if button6 == buttons:
        numButton = 6
    if button7 == buttons:
        numButton = 7
    if button8 == buttons:
        numButton = 8
    if button9 == buttons:
        numButton = 9
    return numButton


def numberToButton(Coords):
        # Dictionary of valid moves
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    numButton=-1
    for i in range(1,9):
        # tkinter.messagebox.showinfo("","Las coordenadas for son: x:"+str(Coords[0])+" y:"+str(Coords[1]))
        # tkinter.messagebox.showinfo("","Valor de i:"+str(i))
        LCoord=moves[i]
        
        if LCoord[0]==Coords[0] and LCoord[1]==Coords[1]:
            numButton = i
            # tkinter.messagebox.showinfo("","Valor de numButton en if:"+str(numButton))


    # tkinter.messagebox.showinfo("","El valor de la casilla es: "+str(numButton))
    # tkinter.messagebox.showinfo("","Las coordenadas de IA son: x:"+str(Coords[0])+" y:"+str(Coords[1]))

    if numButton == 1:
        return button1
    if numButton == 2:
        return button2
    if numButton == 3:
        return button3
    if numButton == 4:
        return button4
    if numButton == 5:
        return button5
    if numButton == 6:
        return button6
    if numButton == 7:
        return button7
    if numButton == 8:
        return button8
    if numButton == 9:
        return button9


buttons = StringVar()

label = Label(tk, text="Mishi :3", font='Times 20 bold',
              bg='white', fg='black', height=1, width=8)
label.grid(row=2, column=0)

label = Label(tk, text="Turno: ", font='Times 20 bold',
              bg='white', fg='black', height=1, width=8)
label.grid(row=2, column=1)

button1 = Button(tk, text=" ", font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button1))
button1.grid(row=3, column=0)

button2 = Button(tk, text=' ', font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button2))
button2.grid(row=3, column=1)

button3 = Button(tk, text=' ', font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button3))
button3.grid(row=3, column=2)

button4 = Button(tk, text=' ', font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button4))
button4.grid(row=4, column=0)

button5 = Button(tk, text=' ', font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button5))
button5.grid(row=4, column=1)

button6 = Button(tk, text=' ', font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button6))
button6.grid(row=4, column=2)

button7 = Button(tk, text=' ', font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button7))
button7.grid(row=5, column=0)

button8 = Button(tk, text=' ', font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button8))
button8.grid(row=5, column=1)

button9 = Button(tk, text=' ', font='Times 20 bold', bg='gray',
                 fg='white', height=4, width=8, command=lambda: btnClick(button9))
button9.grid(row=5, column=2)

tk.mainloop()
