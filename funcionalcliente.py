import socket
import threading
from tkinter import *
from tkinter import simpledialog

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message == "start_game":
                    top.deiconify()  # Mostra a interface quando o jogo começa
                elif message.startswith("MOVE"):
                    row, col = map(int, message.split()[1:])
                    handle_opponent_move(row, col)
                else:
                    message_list.insert(END, message)
        except:
            break

def send(event=None):
    message = my_message.get()
    my_message.set("")
    message_list.insert(END, f"{username}: {message}")
    client_socket.send(f"{username}: {message}".encode('utf-8'))
    if message == "bye":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_message.set("bye")
    send()

def handle_click(row, col):
    if board[row][col] == "" and not game_over and player_turn:
        board[row][col] = player_symbol
        draw_board()
        client_socket.send(f"MOVE {row} {col}".encode('utf-8'))
        check_winner()
        switch_player()

def handle_opponent_move(row, col):
    if board[row][col] == "" and not game_over and not player_turn:
        board[row][col] = opponent_symbol
        draw_board()
        check_winner()
        switch_player()

def draw_board():
    canvas.delete("all")
    for row in range(3):
        for col in range(3):
            x0 = col * 100
            y0 = row * 100
            x1 = x0 + 100
            y1 = y0 + 100
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", tags="rect")
            if board[row][col] == "X":
                canvas.create_line(x0+10, y0+10, x1-10, y1-10, width=2, tags="cross")
                canvas.create_line(x1-10, y0+10, x0+10, y1-10, width=2, tags="cross")
            elif board[row][col] == "O":
                canvas.create_oval(x0+10, y0+10, x1-10, y1-10, width=2, tags="circle")

def check_winner():
    global game_over
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            game_over = True
            canvas.create_line(50, i*100+50, 250, i*100+50, width=3, fill="red")
            break
        elif board[0][i] == board[1][i] == board[2][i] != "":
            game_over = True
            canvas.create_line(i*100+50, 50, i*100+50, 250, width=3, fill="red")
            break
    if board[0][0] == board[1][1] == board[2][2] != "":
        game_over = True
        canvas.create_line(50, 50, 250, 250, width=3, fill="red")
    elif board[0][2] == board[1][1] == board[2][0] != "":
        game_over = True
        canvas.create_line(250, 50, 50, 250, width=3, fill="red")

def switch_player():
    global player_turn
    player_turn = not player_turn

def reset_game():
    global board, game_over
    board = [["" for _ in range(3)] for _ in range(3)]
    game_over = False
    draw_board()

top = Tk()
top.title("Chat & Tic Tac Toe")
top.withdraw()  # Oculta a interface no início

# Pedindo o nome do usuário
username = simpledialog.askstring("Username", "Please enter your name:")

# Configurando a interface do chat
message_frame = Frame(top)
my_message = StringVar()
scrollbar = Scrollbar(message_frame)
message_list = Listbox(message_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
message_list.pack(side=LEFT, fill=BOTH)
message_list.pack()
message_frame.pack()

entry_field = Entry(top, textvariable=my_message)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(top, text="Send", command=send)
send_button.pack()

# Configurando o jogo da velha
canvas = Canvas(top, width=300, height=300, bg="white")
canvas.pack()

canvas.bind("<Button-1>", lambda event: handle_click(event.y // 100, event.x // 100))

reset_button = Button(top, text="Reset Game", command=reset_game)
reset_button.pack()

player_symbol = "X"
opponent_symbol = "O" if player_symbol == "X" else "X"
board = [["" for _ in range(3)] for _ in range(3)]
game_over = False
player_turn = True

draw_board()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = '127.0.0.1'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

top.mainloop()
