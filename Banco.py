

from SocketServer import ThreadingTCPServer, BaseRequestHandler

class Banco:
    def __init__(self, usuario, cuenta, password, saldo):
        self.id_cuenta= cuenta
        self.usuario = usuario
        self.password = password
        self.saldo = saldo
    def retirar(self,cantidad):
        if(self.saldo >= 0):
            self.saldo = self.saldo - cantidad
        else:
            return "No tiene fondos suficientes"
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
            anuncio = self.request.send("Bienvenido al Banco Carola")
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
                        anuncio = self.request.send("ingreso correctamente, Que desea hacer?\n") 
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
    

  
user1 = Banco("Alejandro", "1234", "alejo97", 310000)
user2 = Banco("Carolina", "123456", "alejo97", 310000)
user3 = Banco("Cristiano", "1234567", "alejo97", 310000)
listaOfUsers=[user1,user2,user3]


myServer = ThreadingTCPServer(("10.0.2.12",8885), MyHandler)
myServer.serve_forever()






