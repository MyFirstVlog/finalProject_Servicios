from SocketServer import ThreadingTCPServer, BaseRequestHandler, UDPServer
import socket
from numpy import *
import numpy as np

class Licoreria:
    def __init__(self, codigo, procedencia, unidades, costo):
        self.code = codigo
        self.house = procedencia
        self.quantity= unidades
        self.cost = costo
    def consultar(self):
        listado = "nombre: " + self.code + "//procedencia: " + self.house + "//costo por botella: " + str(self.cost) + "//cantidad: " + str(self.quantity)
        return listado
    def comprar(self, cantidad):
        valorPagar = cantidad * self.cost         
        return valorPagar
    def restaUnidades(self, cantidad):
        if cantidad <= self.quantity:
            self.quantity = self.quantity - cantidad
        
    def chequeo(self,cantidad1):
        if self.quantity >= cantidad1:
            #self.quantity = self.quantity - cantidad
            return "si"
        elif self.quantity < cantidad1:            
            return "no"


        
class MyHandler(BaseRequestHandler):
    def handle(self):
        print"Connection from ",str(self.client_address)
        SOCKETS_LIST.append(self.request)                
        host, port = self.client_address
        columna = 0
        fila = 0
        matrizPago = array([["","",0]])
        listProducto = []
        rtaCantidad=""
        dineroPagar = 0
        while True:
            con = 0        
            flag1=2
            flag2=2
            flag3=2  
            bandera = 2
            bandera2 = 2
            #flag4=2
            anuncio = self.request.send("La Licoreria de Alejo, lo saluda !!! \n")
                        
            while flag1 == 2:
                flag3 = 2
                anuncio = self.request.send("Comprar o Consultar \n")        
                data = self.request.recv(1024)   
                aux = data[:-2]
                x = aux.split() 
                print x
                if x[0] == "consultar":
                    #longLista = len(listaAlcohol)
                    for i in listaAlcohol:
                        anuncio = self.request.send(i.consultar() + "\n")
                        print "entre a consultar"
                        #anuncio = self.request.send("\n") 
                    longitudSockets= len(SOCKETS_LIST)     
                    anuncio = self.request.send("Actualmente hay conectados: " + str(longitudSockets - 1) + " Clientes" + "\n")    
                if x[0] == "comprar":                      
                    nombre = x[1]                                    
                    for j in listaAlcohol:
                        if(nombre == j.code):
                                dineroPagar = j.comprar(int(x[2]))
                                con += dineroPagar 
                                valoIndividual =  j.cost
                    listProducto=[nombre,dineroPagar,int(x[2])]     
                    #matrizPago= np.append(listProducto)
                    if bandera2 == 2:                                         
                        matrizPago1= append(matrizPago,[listProducto],0)
                        bandera2 = 1
                    else:
                        matrizPago1= append(matrizPago1,[listProducto],0)
                    #print matrizPago1
                    if bandera == 2:
                        matrizPago1= delete(matrizPago1,[0],0)
                        bandera = 1
                    lenMatrizRow = len(matrizPago1)
                    print matrizPago1
                    anuncio = self.request.send("El total a pagar es: "+str(con)+"\n")
                    anuncio = self.request.send("Desea seguir comprando (Y/N) "+"\n")
                    data = self.request.recv(1024)
                    aux2 = data[:-2]
                    if (aux2 == "N"):
                        while flag3 == 2:                          
                            anuncio = self.request.send("Desea pagar? (Y/N)" + "\n")
                            data = self.request.recv(1024)
                            if data == "Y\r\n":     
                                flag4 = 2                            
                                dataConexion = self.request.send("Estableciendo Conexiones con su Banco"+"\n")
                                dataConexion = self.request.send("Digite su Usuario y Contrasena ( separada de espacios ) "+"\n")
                                data = self.request.recv(1024) 
                                ip = "10.0.2.12"
                                port = 6789        
                                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                while flag4==2:
                                    print "entre al while"
                                    for i in range (0,lenMatrizRow):     
                                        print "entre al for" , " ",  matrizPago1[i][1]                                 
                                        message = str(matrizPago1[i][1]) + " "+ data                                   
                                        for j in listaAlcohol:
                                            if(matrizPago1[i][0] == j.code):
                                                rtaCantidad = j.chequeo(int(matrizPago1[i][2]))
                                                #print "Esta es la respuesta del chequeo: ", rtaCantidad, int(matrizPago1[i][2]
                                                              
                                        if rtaCantidad == "si":
                                            sock.sendto(message,("10.0.2.12",6789)) #le manda mensaje a banco cantidad a pagar + nombre + contrasena
                                            response,remote_host = sock.recvfrom(1024)
                                            print response 
                                            if response == "si": 
                                            
                                                for j in listaAlcohol:
                                                    if(matrizPago1[i][0] == j.code):
                                                        j.restaUnidades(int(matrizPago1[i][2]))
                                                        anuncio = self.request.send("Operacion realizada con exito !!!, tu pedido llegara lo mas pronto posible" + "\n")
                                                        con = 0
                                                        flag3 = 1
                                                        flag4 = 1
                                                        matrizPago = array([["","",0]])
                                                        bandera = 2
                                                        bandera2 = 2
                                                        listProducto = []
                                                        break
                                            elif response == "no":
                                                anuncio = self.request.send("No tienes fondos" + "\n")
                                                flag3 = 1
                                                flag4 = 1
                                                matrizPago = array([["","",0]])
                                                bandera = 2
                                                bandera = 2
                                                listProducto = []
                                                break   
                                        elif rtaCantidad == "no":
                                            anuncio = self.request.send("No tienes Stock" + "\n")
                                            flag3 = 1
                                            flag4 = 1
                                            matrizPago = array([["","",0]])
                                            bandera = 2
                                            bandera = 2
                                            listProducto = []
                                            break  
                                                                                   
                                    sock.close() 

                            else:
                                flag3 = 1                     
                                
                    #else:
                     #   flag1 = 1    

                if (data == "chao\r\n"):
                    flag1 = 1
    
            anuncio = self.request.send("Desea salir (Y/N) \n")
            cliente = self.request.recv(1024)
            if cliente == "Y\r\n": 
                SOCKETS_LIST.remove(self.request)
                break
        


vodka = Licoreria("AbsolutVodka", "Suecia", 8, 80000)
ron = Licoreria("RonViejoDeCaldas", "Colombia", 5, 43000)
whiskey = Licoreria("WhiskeyMacallan", "Escocia", 3, 267000)
aguardiente = Licoreria("AguardienteAntioqueno", "Colombia", 9, 43000)
vino = Licoreria("VinoRose","Francia", 7, 49000)

listaAlcohol = [vodka, ron, whiskey, aguardiente, vino]
myServer = ThreadingTCPServer(("10.0.2.12",3463), MyHandler)
SOCKETS_LIST = []
SOCKETS_LIST.append(myServer)
myServer.serve_forever()

        



    