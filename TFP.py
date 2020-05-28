import json

def crearEdificio():
    # Genera el edificio en forma de una matriz organizada en pisos,filas y columnas 
    # marcandolas todas desocupadas al iniciar el programa. Retorna la matriz "edificio".
    edificio = {}
    for piso in range(1, 7):
        if piso == 6:
            f = 5
        else:
            f = 10
        c = 10
        mpiso = []
        for fila in range(f):
            listaF = []
            for columna in range(c):
                listaF.append('O')
            mpiso.append(listaF)
            listaF = []
        edificio['Piso' + str(piso)] = mpiso
    return edificio
def extraerClasificiacion():
    # Extrae las matrices de la calificacion.json para despues convertir los numeros de 1-4 
    # en los strings relacionados a cada tipo de vehiculos. Retorna la calificacion con los strings en vez de enteros 
    with open('clasificacion.json', 'r') as archivo:
        clasificacion = json.load(archivo)
        archivo.close()
    for piso in range(1,7):
        for fila in range(len(clasificacion['Piso' + str(piso)])):
            for columna in range(len(clasificacion['Piso' + str(piso)][fila])):
                elemento = clasificacion['Piso' + str(piso)][fila][columna]
                if elemento == 1:
                    clasificacion['Piso' + str(piso)][fila][columna] = 'Automóvil'
                elif elemento == 2:
                    clasificacion['Piso' + str(piso)][fila][columna] = 'Automóvil Eléctrico'
                elif elemento == 3:
                    clasificacion['Piso' + str(piso)][fila][columna] = 'Motocicleta'
                elif elemento == 4:
                    clasificacion['Piso' + str(piso)][fila][columna] = 'Discapacitado'
    return(clasificacion)
def ingresodecarro():
    # Toma como variables globales la matriz del edifico, la clasificacion retornada y la lista vacia de actualidad
    # despues pide la placa para verificarla en usuarios,json y comprobar el registro y extraer los datos de la persona
    global edificio
    global clasificacion
    global actualidad
    placa =  input('Placa\n')
    if not ingresoRepetido(placa):
        if verifivarusuarios(placa):
            with open('usuarios.json', 'r', encoding='utf-8') as archivo:
                usuarios = json.load(archivo)
                archivo.close()
            for persona in usuarios['usuarios']:
                if placa == persona[3]:
                    tipocarro = persona[4]
                    tipopersona = persona[2]
                    tipopago = persona[5]
                    break
        # si no se encuentra le solicita el tipo de vehiculo y le asigna el tipo de persona "visitante" y el tipo de pago diario
        else:
            tipocarro = input('Tipo de carro (Automóvil, Motocicleta, Automóvil Eléctrico, Discapacitado)\n')
            tipopersona = 'Visitantes'
            tipopago = 'Diario'
        # llama a la funcion contarcupos y a la funcion indice, a esta ultima pasandole como parametro el tipo de vehiculo 
        # para despues verificar si puede parquear en diversos espacios o no segun el tipo
        cupos = contarcuposdisponibles()
        indice = indiceTipo(tipocarro)
        if indice == 0:
            iadicional = -1  # ultimo elemento de una lista
            tipocarro2 = 'nada'
        elif indice == 1:
            iadicional = 0
            tipocarro2 = 'Automóvil'
        elif indice == 2:
            iadicional = -1
            tipocarro2 = 'nada'
        elif indice == 3:
            iadicional = 0
            tipocarro2 = 'Automóvil'
        # Solicita al usuario el piso en el que va a estacionar,llama a la funcion elejircupo para evaluar las filas y las columnas de ese piso,
        # despues muestra en pantalla los cupos disponible en ese piso y permite al usuario seleccionar,
        # si el cupo seleccionado es valido y es selccionado en la matriz edificio marca ese espacion con "x", por ultimo modifica la lista actualidad
        # con la nueva imformacion
        piso = int(input('Cupos disponibles:\npiso1 : ' + str(cupos[0][indice] + cupos[0][iadicional]) + '\npiso2 : ' + str(cupos[1][indice] + cupos[1][iadicional]) + '\npiso3 : ' + str(cupos[2][indice]+ cupos[2][iadicional]) + '\npiso4 : ' + str(cupos[3][indice]+ cupos[3][iadicional]) + '\npiso5 : ' + str(cupos[4][indice]+ cupos[4][iadicional]) + '\npiso6 : ' + str(cupos[5][indice]+ cupos[5][iadicional]) + '\n'))
        fila, columna = elejircupo(piso, tipocarro, tipocarro2, clasificacion['Piso' + str(piso)].copy())
        edificio['Piso' + str(piso)][fila][columna] = 'X'
        actualidad.append([placa, tipopago, tipopersona, tipocarro, piso, fila, columna])
    else:
        print('Usted ya ingreso el carro')
def contarcuposdisponibles():
    # utilizar la matriz edificio y la clasificacion de los cupos del edificio para marcar los cupos disponibles
    global edificio
    global clasificacion
    pisos = []
    tipo = [0,0,0,0,0]  # tipo [1,2,3,4]
    for piso in clasificacion:
        for fila in range(len(clasificacion[piso])):
            for columna in  range(len(clasificacion[piso][fila])):  # [piso][fila][col]
                if edificio[piso][fila][columna] == 'O':
                    indice = indiceTipo(clasificacion[piso][fila][columna])
                    tipo[indice] += 1
        pisos.append(tipo)
        tipo = [0,0,0,0,0]
    # retornando la matriz "pisos" con los cupos marcados
    return pisos
def escribirpiso(piso):
    # parametros: "piso"
    # la funcion genera la fila y la columna del piso seleccionado, despues modifica la lista mpiso y la retorna. 
    if piso == 6:
        f = 5
    else:
        f = 10
    c = 10
    mpiso = []
    for fila in range(f):
        listaF = []
        for columna in range(c):
            listaF.append('O')
        mpiso.append(listaF)
        listaF = []
    return mpiso
def elejircupo(numpiso, tipocarro1, tipocarro2, clasificacion): 
    # parametros: numpiso,tipocarro1,tipocarro2,clasificacion,variable global "edificio"
    # llama a la funcion escribir piso pasandole el numero para generar la ocupacion de este.
    # despues compara la calificacion con el tipo de vehiculo(note que hay cupos que permiten 2 tipos de vehiculo, por eso "tipocarro1 y 2")
    # , marcando con una "x" si el cupo no es disponible

    global edificio
    piso = escribirpiso(numpiso)
    for fila in range(len(clasificacion)):
        for columna in range(len(clasificacion[fila])):
            elemento = clasificacion[fila][columna]
            cupo = edificio['Piso'+str(numpiso)][fila][columna]
            if (elemento != tipocarro1 and elemento != tipocarro2) or cupo == 'X':
                piso[fila][columna] = 'X'
    print('Los cupos disponibles son representados por (O)\n', piso)

    # Pide al usuario la fila y la columna para seleccionar el cupo, si el cupo esta disponible retorna las elecciones, 
    # sino imprime 'Espacio no Disponible'

    cupoDisponible = True
    while cupoDisponible:
        eleccionfila = int(input('Por favor digitar la fila en donde desea parquear:\n')) -1
        eleccioncolumna = int(input('Por favor digitar la columna en donde desea parquear:\n')) -1
        if piso[eleccionfila][eleccioncolumna] == 'O':
            print('Puede pasar')
            return eleccionfila, eleccioncolumna
        else:
            print('Espacio no Disponible')
def verifivarusuarios(placaingreso):
    # parametros: placaingreso
    # Abre usuarios.json para verificar si la placa esta en ese archivo. si la placa se encuentra retorna "TRUE", sino retorna "FALSE"
    with open('usuarios.json', 'r', encoding='utf-8') as archivo:
        usuarios = json.load(archivo)
        archivo.close()
    for usuario in usuarios['usuarios']:
        placa = usuario[3]
        if placa == placaingreso:
            return True
    return False
def indiceTipo(categoria):
    if categoria == 'Automóvil' or categoria == 'Estudiante':
        return 0
    elif categoria == 'Automóvil Eléctrico' or categoria == 'Profesor':
        return 1
    elif categoria == 'Motocicleta' or categoria == 'Personal Administrativo':
        return 2
    elif categoria == 'Discapacitado' or categoria == 'Visitantes':
        return 3
def ingresoRepetido(placa):
    # Parametros: placa
    # Verifica la placa ingresada en la lista actualidad. si esta se encuentra retorna "TRUE", sino retorna "FALSE".
    global actualidad
    for carro in actualidad:
        if carro[0] == placa:
            return True
    return False
def salircarro():

    # variables globales(actualidad,edificio)
    # Solicita la placa y la verifica en la funcion "IngresoRepetido", si esta se encuentra extrae toda la informacion de la lista de actualidad
    # Solicita las horas que el vehiculo estuvo estacionado, despues llama a la funcion "pago" pasandole la informacion extraida de actualiad
    # Imprime el monto a pagar, marca en la matriz edificio el cupo como vacio y borra el vehiculo y su informacion de "actualidad"

    global actualidad
    global edificio
    placa = input('Ingrese su placa para salir:\n')
    if ingresoRepetido(placa):
        for carro in range(len(actualidad)):
            if actualidad[carro][0] == placa:  # [placa, tipopago, tipopersona, tipocarro, piso, fila, columna]
                tipopago = actualidad[carro][1]
                tipopersona = actualidad[carro][2]
                numpiso = actualidad[carro][4]
                fila = actualidad[carro][5]
                columna = actualidad[carro][6]
                break
        horas = int(input('Cuantas horas estuvo el carro dentro del parqueadero:\n'))
        print('Su monto a pagar es de: ' + str(pago(tipopersona, tipopago, horas)))
        edificio['Piso' + str(numpiso)][fila][columna] = 'O'
        del actualidad[carro]
def registrarUsuario():

    # Abre los usuarios.json y guarda su contenido en la variable "usuarios"
    # ,solicita el numero de identificacion del usuario y genera la variable "esta" como un "FALSE"
    with open('usuarios.json', 'r', encoding='utf-8') as archivo:
        usuarios = json.load(archivo)
        archivo.close()
    numid = int(input('Ingrese su numero de identificacioin\n'))
    esta = False

    # utiliza el indice donde se encuentra el numero de identificacion y si coincide con la ingresada modifica "esta" volviendola "TRUE"

    for usuario in usuarios['usuarios']:
        if usuario[1] == numid:
            esta = True
            break

    # Si el numero de identificacion no esta genera una lista como "nuevousuario", y llena los indices de la lista con los datos necesarios.
    # Guarda el usuario en la lista de los usuarios.
    # Si el numero ya estaba en la variable "usuarios" no entra en el siguente "if" y imprime 'Un usuario no pude registrar mas de un carro'

    if not esta:
        nuevousuario = [0,0,0,0,0,0]
        nuevousuario[0] = input('Ingrese su nombre\n')
        nuevousuario[1] = numid
        tipo = input('Ingrese el tipo de usuario\n')
        while tipo == 'Visitantes':
            print('No se puede registrar como visitante')
            tipo = input('Ingrese el tipo de usuario\n')
        nuevousuario[2] = tipo
        nuevousuario[3] = input('Ingrese su placa\n')
        nuevousuario[4] = input('Ingrese su tipo de vehiculo\n')
        nuevousuario[5] = input('Ingrese su plan de pago\n')
        usuarios['usuarios'].append(nuevousuario)
    else:
        print('Un usuario no pude registrar mas de un carro')

    # por ultimo, convierte la variable "usuarios" en un archivo .json y lo añade a los "usuarios.json" ya existentes 

    with open('usuarios.json', 'w', encoding='utf-8') as archivo:
        json.dump(usuarios, archivo,ensure_ascii=False)
        archivo.close()
def pago(persona, pago, horas):

    # Parametros: persona,pago,horas
    # convierte las horas en minutos, se evalua si el pago se hace en "mensualidad" y si lo hace retorna "0"
    # si pago != "Mensualidad", se multiplican los minutos por la tarifa establecida por cada tipo de persona y retorna el resultado de la multiplicacion

    minutos = horas * 60
    if pago == 'Mensualidad':
        return 0
    else:
        if persona == 'Estudiante':
            return minutos * 1000
        if persona == 'Profesor':
            return minutos * 2000
        if persona == 'Personal Administrativo':
            return minutos * 1500
        if persona == 'Visitantes':
            return minutos * 3000
def generarEstadisticas():
    segunTipoUsuario()
    segunVehiculo()
    ocupacion()
def segunTipoUsuario():

    # Variable global "actualidad"
    # la funcion raliza un conteo de los ingresos al parqueadero segun el tipo de persona que entra
    # Para carro[2](que es el indice donde se encuentra el tippo de persona) en actualidad (la cantidad de vehiculos que han ingresado)
    # suma 1 a la variable relacionada al tipo de persona correspondiente 

    global actualidad
    estudiante = 0
    profesor = 0
    admin = 0
    visitante = 0
    for carro in actualidad:
        tipo = carro[2]
        if tipo == 'Estudiante':
            estudiante += 1
        elif tipo == 'Profesor':
            profesor += 1
        elif tipo == 'Personal Administrativo':
            admin += 1
        elif tipo == 'Visitantes':
            visitante += 1
    
    # En la variable archivo genera el archivo "primer reporte.txt" y lo llena con las estadisticas de cada uno de los tipos de personas

    archivo = open('PrimerReporte.txt', 'w', encoding='utf-8')
    archivo.write('estudiantes = ' + str(estudiante) + '\nprofesores = ' + str(profesor) + '\nPersonal Administrativo = ' + str(admin) + '\nVisitantes = ' + str(visitante))
    archivo.close()
def segunVehiculo():

    # variable global "actualidad"
    # la funcion raliza un conteo de los ingresos al parqueadero segun el tipo de vehiculo que entra
    # Para carro[3](que es el indice donde se encuentra el tippo de vehiculo) en actualidad (la cantidad de vehiculos que han ingresado)
    # suma 1 a la variable relacionada al tipo de vehiculo correspondiente 

    global actualidad
    auto = 0
    autoe = 0
    moto = 0
    disca = 0
    for carro in actualidad:
        tipo = carro[3]
        if tipo == 'Automóvil':
            auto += 1
        elif tipo == 'Automóvil Eléctrico':
            autoe += 1
        elif tipo == 'Motocicleta':
            moto += 1
        elif tipo == 'Discapacitado':
            disca += 1

     # En la variable archivo genera el archivo "segundo reporte.txt" y lo llena con las estadisticas de cada uno de los tipos de vehiculos

    archivo = open('SegundoReporte.txt', 'w', encoding='utf-8')
    archivo.write('Automóvil = ' + str(auto) + '\nAutomóvil Eléctrico = ' + str(autoe) + '\nMotocicleta = ' + str(moto) + '\nDiscapacitado = ' + str(disca))   
    archivo.close()  
def ocupacion():

    # Variable global "actualidad"
    # La funcion se encarga de contar el numero total de vehiculos que se encuentran en el parqueadero
    # ,despues sacar el porcentaje total y por pisos de ocupacion del parqueadero
    # totalcarros = cantidad de vehiculos ingresados, guardados en "actualidad"
    global actualidad
    totalcarros = len(actualidad)
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p5 = 0
    p6 = 0

    # A cada carro[4] a las variable piso = 0 definidas anteriormente les suma 1, contando los vehiculos por piso

    for carro in actualidad:
        tipo = carro[4]
        if tipo == 1:
            p1 += 1
        elif tipo == 2:
            p2 += 1
        elif tipo == 3:
            p3 += 1
        elif tipo == 4:
            p4 += 1
        elif tipo == 5:
            p5 += 1
        elif tipo == 6:
            p6 += 1
    # En la variable archivo genera el archivo "tercer reporte.txt", realiza las operaciones de los porcentajes del total del parqueadero y el 6to piso. 
    # el resto de piso quedan igual ya que son una matriz 10x10, por lo que multiplicar y dividir entre 100 resulta en el mismo numero inicial.
    # Por ultimo escribe las estadisticas en archivo .txt y lo cierra
    archivo = open('TercerReporte.txt', 'w', encoding='utf-8')
    archivo.write('Porcentaje de ocupacion global = ' + str((totalcarros/550)*100) + '%\nPiso 1  = ' + str((p1)) + '%\nPiso 2 = ' + str(p2) + '%\nPiso 3 = ' + str(p3) + '%\nPiso 4 = ' + str(p4)+ '%\nPiso 5 = ' + str(p5)+ '%\nPiso 6 = ' + str((p6/50)*100) + '%')   
    archivo.close()

edificio = crearEdificio()
clasificacion = extraerClasificiacion()
actualidad = []

# El siguente condicional evalua cada una de las opciones para llamar a la funcion requerida por cada una de la opciones

print('Menu parqueadero')
opcion = input('Digite la opcion deseada: Exit, Ingresar, SalirParqueadero, GenerarEstadisticas, RegistrarUsuario\n')
while opcion != 'Exit':
    if opcion != 'Exit':
        if opcion == 'Ingresar':
            ingresodecarro()
        elif opcion == 'SalirParqueadero': 
            salircarro()
        elif opcion == 'GenerarEstadisticas':
            generarEstadisticas()
        elif opcion == 'RegistrarUsuario':
            registrarUsuario()
    opcion = input('Digite la opcion deseada: Exit, Ingresar, SalirParqueadero, GenerarEstadisticas, RegistrarUsuario\n')