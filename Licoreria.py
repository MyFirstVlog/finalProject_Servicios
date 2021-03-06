from SocketServer import ThreadingTCPServer, BaseRequestHandler, UDPServer
import socket
from numpy import *
import numpy as np
import string
from sys import argv,exit

class Licoreria:
    def __init__(self, codigo, procedencia, unidades, costo):   #constructor con atributos
        self.code = codigo
        self.house = procedencia
        self.quantity= unidades
        self.cost = costo
    def consultar(self): #listado de los productos
        listado = "nombre: " + self.code + "//procedencia: " + self.house + "//costo por botella: " + str(self.cost) + "//cantidad: " + str(self.quantity)
        return listado 
    def comprar(self, cantidad): #compra de productos 
        valorPagar = cantidad * self.cost         
        return valorPagar
    def restaUnidades(self, cantidad):# resta de la cantidad de producto actual con la cantidad que compra el usuario
        if cantidad <= self.quantity:
            self.quantity = self.quantity - cantidad
        
    def chequeo(self,cantidad1):# disponibilidad de producto
        if self.quantity >= cantidad1:
            #self.quantity = self.quantity - cantidad
            return "si"
        elif self.quantity < cantidad1:            
            return "no"
    


        
class MyHandler(BaseRequestHandler):#clase de conexion

    def handle(self):#metodo
        print"Connection from ",str(self.client_address)
        SOCKETS_LIST.append(self.request) #agrega los clientes conectados a una lista               
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
                        
            while flag1 == 2:#ciclo inicial de compra y consulta
                flag3 = 2 
                anuncio = self.request.send("Comprar o Consultar \n")        
                data = self.request.recv(1024)   
                aux = data[:-2]
                x = aux.split() 
                print x
                if x[0] == "consultar":
                    #longLista = len(listaAlcohol)
                    for i in listaAlcohol:
                        anuncio = self.request.send(i.consultar() + "\n")#devuelve un contenido de la lista d elos objetos
                        print "entre a consultar"
                        #anuncio = self.request.send("\n") 
                    longitudSockets= len(SOCKETS_LIST)     
                    anuncio = self.request.send("Actualmente hay conectados: " + str(longitudSockets - 1) + " Clientes" + "\n")    
                if x[0] == "comprar":                      
                    nombre = x[1]                                    
                    for j in listaAlcohol: #coincidencia de producto del usuario y valor a pagar
                        if(nombre == j.code):
                                dineroPagar = j.comprar(int(x[2]))
                                con += dineroPagar 
                                valoIndividual =  j.cost
                    listProducto=[nombre,dineroPagar,int(x[2])]                      
                    if bandera2 == 2:                                         
                        matrizPago1= append(matrizPago,[listProducto],0) #se crea la matriz utilizando el listProducto
                        bandera2 = 1
                    else:
                        matrizPago1= append(matrizPago1,[listProducto],0) #agrega listas sobre la matriz ya creada
                    #print matrizPago1
                    if bandera == 2: #elimina primera fila de inicializacion
                        matrizPago1= delete(matrizPago1,[0],0)
                        bandera = 1
                    lenMatrizRow = len(matrizPago1)
                    print matrizPago1
                    anuncio = self.request.send("El total a pagar es: "+str(con)+"\n") #con -> acumulacion de valor a pagar
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
                                aux3 = data.split()
                                aux4 = aux3[1] #contrasena
                                print aux4

                                intab = string.ascii_lowercase #codificacion de la contrasena
                                outtab = intab[3 % 26:] + intab[:3 % 26]
                                trantab = string.maketrans(intab, outtab)
                                contrasena = aux4.translate(trantab)  #contrasena codificada
                                
                                code = contrasena
                                print "esta es la contra codificada: ", code
                                data = aux3[0] + " " + code
                                print "esta es la data que se envia a licoreria: ", data
                                ip = ip_socketUDP #genero el socket udp para generar la conexion con el banco
                                port = port_UDP       
                                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                while flag4==2:
                                    print "entre al while"
                                    for i in range (0,lenMatrizRow):     
                                                                         
                                        message = str(matrizPago1[i][1]) + " "+ data    
                                        print "esto es lo que estoy enviando: ",  message                            
                                        for j in listaAlcohol: #aqui se verifica si hay stock en la licorera
                                            if(matrizPago1[i][0] == j.code):
                                                
                                                rtaCantidad = j.chequeo(int(matrizPago1[i][2]))
                                                #print "Esta es la respuesta del chequeo: ", rtaCantidad, int(matrizPago1[i][2]
                                                              
                                        if rtaCantidad == "si":
                                            sock.sendto(message,(ip,port)) #le manda mensaje a banco cantidad a pagar + nombre + contrasena
                                            response,remote_host = sock.recvfrom(1024)
                                            print response 
                                            if response == "si": 
                                            
                                                for j in listaAlcohol:
                                                    if(matrizPago1[i][0] == j.code): #resta unidades
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
                                            con = 0
                                            listProducto = []
                                            break  
                                                                                   
                                    sock.close() 

                            else: #se devuelva al ciclo para seguir comprando
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

ip_socketUDP = str(argv[3])
port_UDP = int(argv[4])
port_TCP= int(argv[2])
ip_TCP = str(argv[1])

listaAlcohol = [vodka, ron, whiskey, aguardiente, vino]
myServer = ThreadingTCPServer((ip_TCP,port_TCP), MyHandler)
SOCKETS_LIST = []
SOCKETS_LIST.append(myServer)
myServer.serve_forever()

        



    