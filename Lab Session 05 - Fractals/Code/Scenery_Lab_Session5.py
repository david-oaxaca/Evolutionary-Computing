# Paisaje usando fractales
# Alumno: Oaxaca Pérez David Arturo
# Materia: Evolutionary Computing
# Profesor: Jorge Luis Rosas Trigueros
# Lab Session 05: Fractals
# Basado en el codigo del Dr. Jorge Luis Rosas Trigueros visto en clase
# Grupo: 3CV11
# Fecha de realización: 15/10/2021

# Variable global del color que se usara para el fractal
RGB_color = (255, 255, 255)

# Función recursiva para la creación de fractales
def ec(img,x,y,l,a,sl,da,n, tipo):
    if n<0:
        return

    global RGB_color

    x2=x+l
    y2=y
    ar=math.radians(a)

    coseno=math.cos(ar)
    seno=math.sin(ar)
    xrot= (x2-x)*seno + (y2-y)*coseno
    yrot= (x2-x)*coseno - (y2-y)*seno

    x2=xrot + x
    y2=yrot + y

    cv2.line(img, (int(x),int(y)), (int(x2),int(y2)), RGB_color, (1)) 

    if(tipo == 0):   
      ##1 - Fractal de Arbol
      ec(img,x2,y2,l*sl,a-da,sl,da,n-1, tipo)
      ec(img,x2,y2,l*sl,a+da,sl,da,n-1, tipo)
      ec(img,x2,y2,l*sl,a,sl,da,n-1, tipo)
    elif(tipo == 1):
      ##2 - Fractal de Estrella
      ec(img,x,y,l*sl,a-da,sl,da,n-1, tipo)
    elif(tipo == 2):
      ##3 - Fractal de cordillera
      if(y>280):return
      ec(img,x2,y2,l*sl,a-da,sl,da,n-1, tipo)
      ec(img,x2,y2,l*sl,a-2*da,sl,da,n-1, tipo)
      ec(img,x2,y2,l*sl,a-3*da,sl,da,n-1, tipo)
    elif(tipo == 3):
      ##4 - Fractal de Nube
      cv2.circle(img,(int(x),int(y)),int(l),RGB_color,-1)
      cv2.circle(img,(int(x),int(y)),int(l),(0,0,0),1)
      ec(img,x2,y2,l*sl,a-da,sl,da,n-1, tipo)
      ec(img,x2,y2,l*sl,a-2*da,sl,da,n-1, tipo)
      ec(img,x2,y2,l*sl,a-3*da,sl,da,n-1, tipo)
    elif(tipo == 4):
      ##5 - Fractal de caparazon
      ec(img,x2,y2,l+sl,a+da,sl,da,n-1, tipo)
    return

# Función para la creación de una figura compuesta por varios fractales
def pine(eje_x, leaf_color, trunk_color, star_color):
    global RGB_color
    
    RGB_color = trunk_color
    ec(img, eje_x,470,12,180,0.7,120,9, 0)
    RGB_color =leaf_color
    ec(img, eje_x,450,35,180,0.7,120,9, 0)
    ec(img, eje_x,410,30,180,0.7,120,9, 0)
    ec(img, eje_x,380,25,180,0.7,120,9, 0)

    #Estrella
    RGB_color = star_color
    ec(img,eje_x,290,10,30,1,50,100, 1)

    #Esferas
    RGB_color = (random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))
    ec(img, eje_x, 310,10,180,0.97,33,11, 1)
    ec(img, eje_x+10, 350,10,180,0.97,33,11, 1)
    ec(img, eje_x-10, 345,10,180,0.97,33,11, 1)
    ec(img, eje_x+15, 380,10,180,0.97,33,11, 1)
    ec(img, eje_x-15, 380,10,180,0.97,33,11, 1)
    ec(img, eje_x+30, 420,10,180,0.97,33,11, 1)
    ec(img, eje_x, 420,10,180,0.97,33,11, 1)
    ec(img, eje_x-30, 420,10,180,0.97,33,11, 1)

# Función para la creación de estrellas en posiciones aleatorias dentro de determinados limites
def stars(num_stars, lower_lim, upper_limit, left_limit, right_limit):
    global RGB_color
    RGB_color = (255,255,255)
    for i in range(num_stars):
      ec(img, random.randrange(left_limit, right_limit, 25), random.randrange(lower_lim, upper_limit, 20),25,180,0.97,33,50, 1)

img = np.zeros((500, 1000, 3), dtype="uint8")
# Creación del cielo nocturno
cv2.rectangle(img, (0,0), (1000, 500), (70,12,29), (-1))
# Creación de la tierra en el fondo
cv2.rectangle(img, (0,470), (1000, 500), (60,72,112), (-1))

# Creación de los arboles navideños
for i in range(15):
    pine(80*i, (41,41,0), (20,29,43), (0,168,189))

# Creación de los arboles navideños de fondo, usando colores más opacos
for i in range(8):
    pine(136*i, (69,85,44), (66,97,141), (28,215,249))

# Creación de las estrellas pasando como parametros el numero de estrellas y limites
stars(25, 0, 280, 340, 1000)

# Creación de la luna, usando un fractal con forma de caparazon pero con un angulo más pequeño
ec(img,95,95,10,30,1,75,150, 4)

cv2_imshow(img)