

from SocketServer import ThreadingTCPServer, BaseRequestHandler, UDPServer
from threading import Thread
import string
from sys import argv,exit
class Banco:
    def __init__(self, usuario, cuenta, password, saldo):
        self.id_cuenta= cuenta
        self.usuario = usuario
        self.password = password
        self.saldo = saldo
    def retirar(self,cantidad):
        print self.saldo, cantidad
        if (self.saldo >= cantidad):  
            print "entre al sef retireae"      
            self.saldo = self.saldo - cantidad      
            return "si"      
        else:
            return "no"
    def consultar(self):
        return self.saldo
    def consignar(self,valor):
        self.saldo = self.saldo + valor
        return self.saldo

class MyHandler(BaseRequestHandler):

    def handle(self): 
        print"Connection from ",str(self.client_address) 
           
        while True:
            #anuncio = self.request.send("1) Consulte su saldo\n 2)Consignar Dinero\n 3) Retirar dinero")
            flag1=2
            flag2=2
            flag3=2  
            anuncio = self.request.send("Bienvenido al Banco Carola\n")
            anuncio = self.request.send(" Ingrese usuario:\n")
            cliente = self.request.recv(1024)
            if cliente == "chao\r\n": break
            while flag1 == 2:
                print "entre"
                anuncio = self.request.send("Ingrese Contrasena:\n")
                contrasena = self.request.recv(1024)                
                if contrasena == "chao\r\n":
                    break
                for i in listaOfUsers:                    
                    if(i.usuario+"\r\n" == cliente and i.password+"\r\n" == contrasena):
                        anuncio = self.request.send("ingreso correctamente !!!, Que desea hacer?\n") 
                        while flag2 == 2:
                            data= self.request.recv(1024) 
                            aux= data[:-2]
                            x= aux.split()             

                            if x[0] == "retirar":
                                i.retirar(int(x[1]))
                                anuncio = self.request.send("Te quedan: "+str(i.saldo)+"\n")
                            elif x[0] == "consultar":
                                i.consultar()
                                anuncio = self.request.send("Tienes: "+str(i.saldo)+"\n")
                            elif x[0] == "consignar":
                                i.consignar(int(x[1]))
                                anuncio = self.request.send("Nuevo saldo: "+str(i.saldo)+"\n")
                            if(data == "chao\r\n"):
                                flag1 = 1
                                flag2 = 1
                                         

        self.request.close()
    
class MyHandlerUDP(BaseRequestHandler):

    def handle(self):
        print "Connection from ", str(self.client_address)
        data, conn = self.request
        flag1=2
        flag2=2
        flag3=2
        aux= data
        x= aux.split() 
        print "esto es lo que llega al banco", x
        cliente = x[1]
        #descodificacion de la contrasena
        intab = string.ascii_lowercase
        outtab = intab[-3 % 26:] + intab[:-3 % 26]
        trantab = string.maketrans(intab, outtab)
        contrasena = x[2].translate(trantab)          
        print "esta es la contra decodifcada",contrasena

        print cliente, contrasena, int(x[0])
        while flag1 == 2:
            for i in listaOfUsers:                    
                    if(i.usuario == cliente and i.password == contrasena):
                        print i.saldo
                        a = i.retirar(int(x[0]))
                        if a == "si":
                            print "entre al si "
                            data = "si"
                            conn.sendto(data,self.client_address)
                            flag1 = 1
                        else:
                            data = "no"
                            conn.sendto(data,self.client_address)
                            flag1 = 1




    

  
user1 = Banco("Alejandro", "1234", "alejo", 482000)
user2 = Banco("Carolina", "123456", "alejo", 482000)
user3 = Banco("Cristiano", "1234567", "alejo", 482000)
listaOfUsers=[user1,user2,user3]


port_UDP = int(argv[3])
port_TCP= int(argv[2])
ip_TCP = str(argv[1])

myServer = ThreadingTCPServer((ip_TCP,port_TCP), MyHandler)
myServerUDP = UDPServer((ip_TCP, port_UDP),MyHandlerUDP)

t1 = Thread(target=myServer.serve_forever)
t = Thread(target=myServerUDP.serve_forever)

t1.start()
t.start()

t1.join()
t.join()






