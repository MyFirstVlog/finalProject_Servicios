from SocketServer import ThreadingTCPServer, BaseRequestHandler

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
        self.quantity = self.quantity - cantidad
        return valorPagar
        
class MyHandler(BaseRequestHandler):
    def handle(self):
        print"Connection from ",str(self.client_address)
        SOCKETS_LIST.append(self.request)                
        host, port = self.client_address
        while True:
            con = 0        
            flag1=2
            flag2=2
            flag3=2  
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
                    while flag3 == 2:
                        anuncio = self.request.send("El total a pagar es: " + str(con) + "\n")
                        anuncio = self.request.send("Desea seguir comprando? (Y/N)" + "\n")
                        data = self.request.recv(1024)
                        aux2 = data[:-2]
                        x2 = aux.split()
                        if (aux2 == "Y"):
                            flag3 = 1                            
                        elif (aux2 == "N"): 
                            flag3 = 1
                            flag1 = 1
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
myServer = ThreadingTCPServer(("10.0.2.12",8885), MyHandler)
SOCKETS_LIST = []
SOCKETS_LIST.append(myServer)
myServer.serve_forever()

        



    