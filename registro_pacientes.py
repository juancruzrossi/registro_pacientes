#Importamos paquetes necesarios
from tkinter import *
from tkinter import messagebox
import sqlite3 

#5)---------- Funciones ----------

#Creacion de la Base de datos
def conexionBBDD():

    miConexion = sqlite3.connect("Usuarios")

    miCursor = miConexion.cursor()

    try:
        miCursor.execute('''
            CREATE TABLE DATOSUSUARIOS (
                DNI INTEGER PRIMARY KEY UNIQUE,
                NOMBRE_USUARIO VARCHAR(50),
                APELLIDO VARCHAR(50),
                TELEFONO VARCHAR(50),
                OBRASOCIAL VARCHAR(50),
                HISTORIA_CLINICA VARCHAR(100))
                ''')

        messagebox.showinfo("REGISTRO DE PACIENTES", "Base De Datos creada con éxito.")

    except:
        messagebox.showwarning("¡Atención!", "La Base De Datos ya existe.")

    cuadroDNI.focus_set()


#Que hace el boton Salir
def salirAplicacion():

    valor = messagebox.askquestion("SALIR.", "¿Deseas salir de la aplicación?")

    if valor == "yes":
        root.destroy()


#Limpiar los campos cada vez que apretemos Borrar campos. BOTON BORRAR.
def limpiarCampos():

    miDNI.set("")
    miNombre.set("")
    miApellido.set("")
    miTelefono.set("")
    miObraSocial.set("")
    textoComentario.delete(1.0, END) #Borrar desde el primer caracter hasta el final

    cuadroDNI.focus_set()


#Crear un nuevo usuario al apretar el boton Crear. BOTON CREAR.
def crear():

    miConexion=sqlite3.connect("Usuarios")

    miCursor = miConexion.cursor()

    try:

        personas=[
            miDNI.get(),
            miNombre.get(),
            miApellido.get(),
            miTelefono.get(),
            miObraSocial.get(),
            textoComentario.get("1.0", END)
            ]

        miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES (?,?,?,?,?,?)", personas)

        miConexion.commit()

        messagebox.showinfo("REGISTRO DE PACIENTES", "Registro insertado con éxito.")
    
    except:

        messagebox.showwarning("¡ATENCIÓN!", "El registro ingresado no es válido o ya se encuentra registrado.")

    limpiarCampos()
    



#Leer nuestra Base de Datos. BOTON LEER.
def leer():

    miConexion=sqlite3.connect("Usuarios")

    miCursor = miConexion.cursor()

    miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE DNI = " + miDNI.get())
    
    #El fetchall nos devuelve una lista con la consulta que hicimos
    elUsuario = miCursor.fetchall()

    for usuarioConsultado in elUsuario:

        miDNI.set(usuarioConsultado[0])
        miNombre.set(usuarioConsultado[1])
        miApellido.set(usuarioConsultado[2])
        miTelefono.set(usuarioConsultado[3])
        miObraSocial.set(usuarioConsultado[4])
        textoComentario.insert(1.0, usuarioConsultado[5])

    miConexion.commit()

#Cuando apretamos actualizar. BOTON ACTUALIZAR.
def actualizar():

    miConexion=sqlite3.connect("Usuarios")

    miCursor = miConexion.cursor()

    personas=[
        miDNI.get(),
        miNombre.get(),
        miApellido.get(),
        miTelefono.get(),
        miObraSocial.get(),
        textoComentario.get("1.0", END)
        ]

    miCursor.execute("UPDATE DATOSUSUARIOS SET DNI=?, NOMBRE_USUARIO=?, APELLIDO=?, TELEFONO=?, OBRASOCIAL=?, HISTORIA_CLINICA=? WHERE DNI=" + miDNI.get(), personas)
    
    miConexion.commit()

    limpiarCampos()

    messagebox.showinfo("REGISTRO DE PACIENTES", "Registro actualizado con éxito.")


#Cuando apretamos borrar. BOTON BORRAR.
def borrar():

    miConexion=sqlite3.connect("Usuarios")

    miCursor = miConexion.cursor()

    miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE DNI=" + miDNI.get())

    messagebox.showinfo("REGISTRO DE PACIENTES", "Registro borrado con éxito.")

    miConexion.commit()

    #messagebox.showinfo("REGISTRO DE PACIENTES", "El paciente no existe o ya ha sido borrado.")

    limpiarCampos()

def acercade():

    messagebox.showinfo("REGISTRO DE PACIENTES", " Registro con el objetivo de cargar datos de pacientes para su posterior consulta. Juan Cruz Rossi en colaboración con CEO, 2020.")


#---------- Inicio ----------

# Iniciamos, y le ponemos titulo a la ventana.
root = Tk()
root.title("REGISTRO DE PACIENTES")

#root.iconbitmap('@descarga.xbm')
img = PhotoImage(file='logo2.png')
root.tk.call('wm', 'iconphoto', root._w, img)

#1) Primer seccion de botones (BB DD, Borrar, CRUD, Ayuda)
barraMenu = Menu(root)
root.config(menu = barraMenu, width = 300, height = 300)

#Contenido de los botones
bbddMenu = Menu(barraMenu, tearoff = 0)
bbddMenu.add_command(label = "Crear Tabla", command = conexionBBDD)
bbddMenu.add_command(label = "Salir", command = salirAplicacion)

borrarMenu = Menu(barraMenu, tearoff = 0)
borrarMenu.add_command(label = "Borrar Campos", command = limpiarCampos)

crudMenu = Menu(barraMenu, tearoff = 0)
crudMenu.add_command(label = "Crear", command = crear)
crudMenu.add_command(label = "Leer", command = leer)
crudMenu.add_command(label = "Actualizar", command = actualizar)
crudMenu.add_command(label = "Borrar", command = borrar)

ayudaMenu = Menu(barraMenu, tearoff = 0)
ayudaMenu.add_command(label = "Acerca De...", command = acercade)

#Agregado del desplegable al hacer click en los botones 
barraMenu.add_cascade(label="Menú", menu=bbddMenu)
barraMenu.add_cascade(label="Campos", menu=borrarMenu)
barraMenu.add_cascade(label="Opciones", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

#2)---------- Ahora vamos a hacer el comienzo de los Labels, y su respectivo frame ----------

miFrame = Frame(root)
miFrame.pack()

#Vamos a rescatar lo que escriben los usuarios en los campos
miDNI=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miTelefono=StringVar()
miObraSocial=StringVar()


DNIlabel = Label(miFrame, text="DNI: ")
DNIlabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)

NombreLabel = Label(miFrame, text="Nombre: ")
NombreLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

ApellidoLabel = Label(miFrame, text="Apellido: ")
ApellidoLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

PassLabel = Label(miFrame, text="Teléfono: ")
PassLabel.grid(row=3, column=0, sticky="e", padx=10, pady=10)

ObraSocialLabel = Label(miFrame, text="Obra Social: ")
ObraSocialLabel.grid(row=4, column=0, sticky="e", padx=10, pady=10)

HistoriaClinicaLabel = Label(miFrame, text="Historia Clínica: ")
HistoriaClinicaLabel.grid(row=5, column=0, sticky="e", padx=10, pady=10)



#3)---------- Campos a rellenar, y tambien pertenecen al Frame 1 ----------

cuadroDNI=Entry(miFrame, textvariable=miDNI)
cuadroDNI.grid(row=0, column=1, padx=10, pady=10)
cuadroDNI.config(justify="center")
cuadroDNI.focus_set()

cuadroNombre=Entry(miFrame, textvariable=miNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)
cuadroNombre.config(justify="center")

cuadroApellido=Entry(miFrame, textvariable=miApellido)
cuadroApellido.grid(row=2, column=1, padx=10, pady=10)
cuadroApellido.config(justify="center")

cuadroTelefono=Entry(miFrame, textvariable=miTelefono)
cuadroTelefono.grid(row=3, column=1, padx=10, pady=10)
cuadroTelefono.config(justify="center")

cuadroObraSocial=Entry(miFrame, textvariable=miObraSocial)
cuadroObraSocial.grid(row=4, column=1, padx=10, pady=10)
cuadroObraSocial.config(justify="center")


textoComentario=Text(miFrame, width=20, height=5)
textoComentario.grid(row=5, column=1, padx=10, pady=10)
scrollVert=Scrollbar(miFrame, command=textoComentario.yview)
scrollVert.grid(row=5, column=2, sticky="nsew")

textoComentario.config(yscrollcommand=scrollVert.set)

#4)---------- Botones ----------

miFrame2=Frame(root)
miFrame2.pack()

botonCrear=Button(miFrame2, text="Crear", command = crear)
botonCrear.grid(row=0, column=0, sticky ="e", padx=10, pady=10)

botonLeer=Button(miFrame2, text="Leer", command = leer)
botonLeer.grid(row=0, column=1, sticky ="e", padx=10, pady=10)

botonActualizar=Button(miFrame2, text="Actualizar", command = actualizar)
botonActualizar.grid(row=0, column=2, sticky ="e", padx=10, pady=10)

botonBorrar=Button(miFrame2, text="Borrar", command = borrar)
botonBorrar.grid(row=0, column=3, sticky ="e", padx=10, pady=10)


root.mainloop()