# import socket 
# import threading
# from selenium import webdriver

# HEADER = 64
# PORT = 5001
# SERVER = ''
# ADDR = (SERVER, PORT)
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)


# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")
#     msg_length = conn.recv(HEADER).decode(FORMAT)
#     print("ini")
#     driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
#     print(msg_length)
#     print('fetching')
#     test = driver.get("https://api.tracker.gg/api/v2/valorant/standard/profile/riot/mrj%2300003/")
#     print('done')
#     print(test.text)
#     conn.send("Msg received {}".encode(FORMAT))
#     conn.close()
#     driver.close()
        

# def start():
#     server.listen()
#     print(f"[LISTENING] Server is listening on {SERVER}")
#     while True:
#         conn, addr = server.accept()
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()
#         print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


# print("[STARTING] server is starting...")
# start()

user = ['Itz_MrJ', 'a', 'b', 'bb']

print(user.index('a'))
user.append({'user': 'mrj','points': 0})
print(user)