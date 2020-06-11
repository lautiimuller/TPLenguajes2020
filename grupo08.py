class Gramatica():

    def __init__(self, gramatica):
        """Constructor de la clase."""
        ListaCadena = gramatica.split("\n")
        print (ListaCadena)

        """
            Ejemplo:
            "A:b A\nA:a\nA:A B c\nA:lambda\nB:b"
        """
        pass

    def isLL1(self, gramatica):
        """Verifica si una gramática permite realizar derivaciones utilizando
           la técnica LL1.
        
        Returns
        -------
        resultado : bool
            Indica si la gramática es o no LL1.
        """
        cadena = gramatica.split("\n")
        esLL1 = True
        listaux = []
        for c in cadena:
            listaux.append(c.split(":"))
        print ("Lista ordenada", listaux)

        ntconlambda = []
        for item in cadena:
            AnteConc = item.split(":")
            if AnteConc[1] == "lambda":
                ntconlambda.append(AnteConc[0])
        print("Antecedentes con Lambda:",ntconlambda)

        first = []
        ListaFirst = []
        firstaux = []
        no_terminal_first = []

        for item in cadena:
            if esLL1:
                AnteConc = item.split(":")
                concecuente = str(AnteConc[1])
                antecedente = str(AnteConc[0])
                firstaux = []
                firstaux.extend(AnteConc[0])
                first.extend(AnteConc[0])
                c = 0
                hastaAhi = False

                for caracter in concecuente:
                    if caracter != ' ':
                        if hastaAhi: #Para saber si no tengo que seguir leyendo caracteres
                            break
                        else:    
                            hastaAhi = True                             
                            if caracter.islower() and concecuente != "lambda": 
                                esta = False
                                for i in ListaFirst: #Si ya tiene algun First
                                    if antecedente in i:
                                        esta = True
                                        pos = ListaFirst.index(i)
                                if esta:
                                    ListaFirst[pos].append(caracter)
                                else:
                                    firstaux.append(caracter)
                                    ListaFirst.append(firstaux)
                                    break
                            if concecuente == "lambda":
                                esta = False
                                for i in ListaFirst: #Si ya tiene algun First
                                    if antecedente in i:
                                        esta = True
                                        pos = ListaFirst.index(i)
                                if esta:
                                    ListaFirst[pos].append(concecuente)
                                else:
                                    firstaux.append(concecuente)
                                    ListaFirst.append(firstaux)
                                    break
                            if caracter.isupper() and concecuente != "lambda":
                                if antecedente != caracter: 
                                    for ireglas in listaux:
                                        if ireglas[1] == "lambda":
                                            hastaAhi = False #Debo seguir leyendo otro Caracter
                                        if caracter not in ntconlambda:
                                            hastaAhi = True
                                        if caracter in ireglas[0]: #Encuentro el NT y saco su first
                                            if ireglas[1].islower():
                                                esta = False
                                                for i in ListaFirst: #Si ya tiene algun First
                                                    if antecedente in i:
                                                        pos = ListaFirst.index(i) 
                                                        esta = True
                                                if esta:
                                                    if ireglas[1] not in ListaFirst[pos]: #Si ya hay 1
                                                        ListaFirst[pos].append(ireglas[1]) #Habria F Comun
                                                        break
                                                else:
                                                    firstaux.append(ireglas[1])
                                                    ListaFirst.append(firstaux)
                                                    break
                                else:
                                    # esLL1 = False #recursividad por izq 
                                    break  #(Lo comento para poder seguir porq la gramatica era recursiva)
                    
        print ("")
        print("Los first son: ", ListaFirst)


    def parse(self, cadena):
        """Retorna la derivación para una cadena dada utilizando las
           producciones de la gramática y los conjuntos de Fi, Fo y Se
           obtenidos previamente.

        Parameters
        ----------
        cadena : string
            Cadena de entrada.

            Ejemplo:
            babc

        Returns
        -------
        devivacion : string
            Representación de las reglas a aplicar para derivar la cadena
            utilizando la gramática.
        """
        pass

# Original lista = Gramatica("A:b A\nA:a\nA:A B c\nA:lambda\nB:b").isLL1("A:b A\nA:a\nA:A B c\nA:lambda\nB:b")

#Esta es de prueba
lista = Gramatica("A:b A\nA:B\nA:B C c\nB:lambda\nB:b\nC:h\nB:c").isLL1("A:b A\nA:B\nA:B C c\nB:lambda\nB:b\nC:h\nB:c")
