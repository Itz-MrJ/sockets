import socket               

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'    
port = 5000                
s.bind((host, port))       
print('Listening...')
s.listen(5)

c, addr = s.accept()       
print ('Got connection from', addr)  
while True:
   c.send(raw_input("Server please type: "))
   print("From Client: ", c.recv(1024))
c.close()