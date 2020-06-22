class Gramatica():

    def __init__(self, gramatica):
        """Constructor de la clase."""
        self.ListaCadena = gramatica.split("\n")
        self.ListaSelect = []

        """
            Ejemplo:
            "A:b A\nA:a\nA:A B c\nA:lambda\nB:b"
        """
        pass

    def isLL1(self):
        """Verifica si una gramática permite realizar derivaciones utilizando
           la técnica LL1.
        
        Returns
        -------
        resultado : bool
            Indica si la gramática es o no LL1.
        """
        cadena = self.ListaCadena
        esLL1 = True
        listaux = []
        for c in cadena:
            listaux.append(c.split(":"))


        for i in listaux:
            if i[0] == i[1][0]:
                esLL1 = False #recursion izq
                return esLL1
        
        for i in listaux: #factor comun
            for x in listaux:
                if i[1][0] == x[1][0] and listaux.index(i) != listaux.index(x) and i[0] == x[0]: 
                    esLL1 = False 
                    return esLL1   

        ntconlambda = []
        for item in cadena:
            AnteConc = item.split(":")
            if AnteConc[1] == "lambda":
                ntconlambda.append(AnteConc[0])
        

        ListaFirst = []
        
        firstaux = []
        no_terminal_first = []
        selects = []
        for item in cadena:
            if esLL1:
                AnteConc = item.split(":")
                concecuente = str(AnteConc[1])
                antecedente = str(AnteConc[0])
                firstaux = []
                firstaux.extend(AnteConc[0])
                selectaux = []
                hastaAhi = False
                selectaux.append(item)
                for caracter in concecuente:
                    if caracter != ' ':
                        if hastaAhi: #Para saber si no tengo que seguir leyendo caracteres
                            break
                        else:    
                            hastaAhi = True                             
                            if caracter.islower() and concecuente != "lambda": 
                                esta = False
                                selectaux.append(caracter)
                                selects.append(selectaux)
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
                                selectaux.append(concecuente)
                                selects.append(selectaux)
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
                                                selectaux.append(ireglas[1])
                                                selects.append(selectaux)
                                                esta = False
                                                for i in ListaFirst: #Si ya tiene algun First
                                                    if antecedente in i:
                                                        pos = ListaFirst.index(i) 
                                                        esta = True
                                                if esta:
                                                    if ireglas[1] not in ListaFirst[pos]: #Si ya hay 1
                                                        ListaFirst[pos].append(ireglas[1][0]) #Habria F Comun
                                                        #break
                                                else:
                                                    firstaux.append(ireglas[1])
                                                    ListaFirst.append(firstaux)
                                                    break
        for aux in selects: #saco selects repetidos
            if (len(selects)-1) >= selects.index(aux)+1:
                if aux == selects[selects.index(aux)+1]:
                    selects.remove(selects[selects.index(aux)+1])
        
        ListaFollow = []
        followaux = []
        c = 1
        for item in cadena:             
            AnteConc = item.split(":")
            concecuente = str(AnteConc[1])
            antecedente = str(AnteConc[0]) 
            followaux = []
            followaux.extend(AnteConc[0]) 
            if c == 1:
                c=2
                followaux.append("$")
                ListaFollow.append(followaux)
            for item2 in listaux: #Lista para encontrar NT en los concecuentes 
                for i in item2[1]: #recorro el antecedente
                    if antecedente == i:
                        cantconc = 0 
                        cantconc = len(item2[1]) #lo uso para saber si tengo que seguir buscando para adelante
                        mov = item2[1].index(i) #Si puedo moverme hacia adelante
                        mov = mov + 2            #muevo
                        if cantconc < mov:
                            followaux.append(item2[0]) #No le sigue nada, agrego el antecedente
                        else:
                            siguiente = item2[1][mov]                                
                            esta = False
                            for x in ListaFollow: #Si ya tiene algun Follow
                                if antecedente in x[0]:
                                    pos = ListaFollow.index(x) 
                                    esta = True
                            if esta:
                                if item2[1][mov] not in ListaFollow[pos]: #Si ya hay 1
                                    ListaFollow[pos].append(item2[1][mov]) 
                            else:
                                followaux.append(item2[1][mov])
                                ListaFollow.append(followaux)
                            
                            if siguiente in ntconlambda: #si tiene lambda 
                                if (mov+2) <= cantconc: #miro si hay algo adelante 
                                    esta = False
                                    for x in ListaFollow: #Si ya tiene algun Follow
                                        if antecedente in x[0]:
                                            pos = ListaFollow.index(x) 
                                            esta = True
                                    if esta:
                                        if item2[1][mov+2] not in ListaFollow[pos]: #Si ya hay 1
                                            ListaFollow[pos].append(item2[1][mov+2]) #Habria F Comun
                                    else:
                                        followaux.append(item2[1][mov])
                                        ListaFollow.append(followaux)                                        
                                else: #sino agrego los follow del concecuente
                                    followaux.append(item2[0]+":Follows") #F para saber que tengo q sacarle los follows y no los first
                                    break

        c = 0 #da 10 vueltas para limpiar los NT
        while c != 10:  
            c = c + 1                 
            for lf in ListaFollow:
                for item in lf:
                    if item.isupper() and lf.index(item) != 0: #si es un NT y no esta primero
                        for lf2 in ListaFirst:
                            #Encuentro el nt y agrego sus follows
                            if lf2[0] == item:
                                encontro = False
                                for x in lf2: 
                                    if x.islower() and x != "lambda":
                                        if x not in lf: #si no esta, lo agrega.
                                            ListaFollow[ListaFollow.index(lf)].append(x)
                                            encontro = True
                                ListaFollow[ListaFollow.index(lf)].remove(item)
                    if "Follows" in item:
                        itemaux, nosirve = item.split(":")
                        for lf2 in ListaFollow:
                            #Encuentro el nt y agrego sus follows
                            if lf2[0] == itemaux:
                                encontro = False
                                for x in lf2: 
                                    if x.islower():
                                        if x not in lf: #si no esta, lo agrega.
                                            ListaFollow[ListaFollow.index(lf)].append(x)
                                            encontro = True
                                ListaFollow[ListaFollow.index(lf)].remove(item)
                    for y in range(1,len(lf)):
                        if lf[y].isupper() and lf[0] == lf[y]:
                           lf.pop(y)#Si quedo un NT igual al antecedente.
        #Donde hay lambda, meto sus follows
        for s in selects:
            if s[1] == "lambda":
                selects[selects.index(s)].remove(s[1]) 
                for lf in ListaFollow: #Busco los follows
                    ante = s[0].split(":")
                    if lf[0] == ante[0]:
                        for i in range (1,len(lf)): #sin contar el primero que es un NT
                            selects[selects.index(s)].append(lf[i]) #Agrego los follows de el

        #Verifico si hay disyuntos
        for sel1 in selects:
            antsel = sel1[0].split(":")
            for sel2 in selects:
                antsel2 = sel2[0].split(":")
                if sel1 != sel2 and antsel[0] == antsel2[0]:
                    for aux1 in antsel[1]:
                        for aux2 in antsel2[1]:
                            if aux1 == aux2 and aux1 != " ":
                                esLL1 = False #disyuntos  
        
        
        for i, x in enumerate(selects): 
            caracteres = x[1]    
            self.ListaSelect.append(caracteres)
            
        return esLL1             
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
        pila = []
        concecuentes = []
        antecedentes = []

        #Saca al distuinguido, antecedentes y concecuentes
        for i, x in enumerate(self.ListaCadena): 
            caracteres = x.split(":")
            ant = caracteres[0]
            con = caracteres[1].split(" ")
            antecedentes.append(ant)
            concecuentes.append(con)
            if i == 0:
                self.distinguido = ant

        lista_entrada = cadena.split(" ")

        derivaciones = self.distinguido + '=> '

        pila.append(concecuentes[0])

        for c in concecuentes[0]:
           derivaciones += c + ' '
        derivaciones += '=>'
        print(derivaciones)

        c = 0
        pertenece = True

        while pertenece == True:    
            for pil in pila:
                #Para los casos donde tenes terminales ya ingresados
                n = 0
                terminales_anteriores = []
                while (pil[n] == lista_entrada[n]) and (pil[n].islower() == True):
                    terminales_anteriores.append(pil[n])
                    c += 1
                    n += 1

                if lista_entrada[n] == '$':
                    pertenece = False

                #Casos donde viene un NT que no se busco
                elemento_agregar = []
                if pil[n].isupper() == True:
                    lista_select_nt = []
                    con = 0
                    while (con < len(antecedentes)):
                        if antecedentes[con] == pil[n]:
                            lista_select_nt.append(self.ListaSelect[con])
                            con += 1
                        else:
                            lista_select_nt.append(None)
                            con += 1
                    
                    for lsnt in lista_select_nt:
                        if lsnt != None:
                            for lsntd in lsnt:
                                if lsntd == lista_entrada[n]:
                                    for e in concecuentes[lista_select_nt.index(lsnt)]:
                                        elemento_agregar.append(e)
                    
                    if elemento_agregar == []:
                        derivaciones = 'No pertenece'
                        pertenece = False


                    #Agrego las derivaciones
                    quedan_todavia = []    
                    print(pil.index(pil[n]))
                    pil.pop(pil.index(pil[n]))
                    pila_aux = []
                    for ta in terminales_anteriores:
                        if ta in pil:
                            pil.pop(pil.index(ta))
                        pila_aux.append(ta)
                        derivaciones += ta + ' '
                    if pil != []:
                        for pi in pil:
                            quedan_todavia.append(pi)
                        pil.pop()
                    for ea in elemento_agregar:
                        pila_aux.append(ea)
                        derivaciones += ea + ' '
                    for qt in quedan_todavia:
                        pila_aux.append(qt)
                        derivaciones += qt + ' '
                    for pa in pila_aux:
                        pil.append(pa) 
                    derivaciones += '=>'
                    print(derivaciones)  
                    break                                   
                else:
                    pertenece = False
                    derivaciones = 'No pertenece'   

        return derivacioness

