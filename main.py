import socket               

s = socket.socket()         # Create a socket object
host = '192.168.0.74'    #private ip address of machine running fedora
port = 80                
s.bind((host, port))       

s.listen(5)                
c, addr = s.accept()       
print 'Got connection from', addr    #this line never gets printed
while True:
   c.send(raw_input("Server please type: "))
   print "From Client: ", c.recv(1024)

c.close()     