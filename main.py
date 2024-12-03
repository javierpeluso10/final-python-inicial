import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, Frame
from tkinter import ttk, messagebox

# Crear base de datos y tabla
def inicializar_base_datos():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apellido TEXT,
            nombre TEXT,
            fecha_nacimiento TEXT,
            sexo TEXT,
            tipo_doc_primario TEXT,
            documento_primario TEXT,
            tipo_doc_secundario TEXT,
            documento_secundario TEXT,
            fecha_emision TEXT,
            fecha_vencimiento TEXT,
            telefono TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Guardar datos en la base de datos
def guardar_cliente():
    datos = (
        apellido_var.get(),
        nombre_var.get(),
        fecha_nacimiento_var.get(),
        sexo_var.get(),
        tipo_doc_primario_var.get(),
        documento_primario_var.get(),
        tipo_doc_secundario_var.get(),
        documento_secundario_var.get(),
        fecha_emision_var.get(),
        fecha_vencimiento_var.get(),
        telefono_var.get(),
        email_var.get()
    )

    if not datos[0] or not datos[1] or not datos[5]:
        messagebox.showerror("Error", "Los campos Apellido, Nombre y Documento son obligatorios.")
        return

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (apellido, nombre, fecha_nacimiento, sexo, tipo_doc_primario, documento_primario,
                              tipo_doc_secundario, documento_secundario, fecha_emision, fecha_vencimiento, telefono, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', datos)
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
    limpiar_campos()
    cargar_datos_en_tabla()

# Cargar datos en la tabla
def cargar_datos_en_tabla():
    for row in tabla.get_children():
        tabla.delete(row)

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, apellido, nombre, fecha_nacimiento, sexo, tipo_doc_primario, documento_primario, telefono, email FROM clientes")
    datos = cursor.fetchall()
    conn.close()

    for cliente in datos:
        tabla.insert("", "end", values=cliente)

# Eliminar cliente seleccionado
def eliminar_cliente():
    try:
        # Obtener ID del cliente seleccionado
        selected_item = tabla.selection()[0]
        cliente_id = tabla.item(selected_item, "values")[0]

        # Confirmación
        if not messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este cliente?"):
            return

        # Eliminar de la base de datos
        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conn.commit()
        conn.close()

        # Eliminar de la tabla
        tabla.delete(selected_item)
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
    except IndexError:
        messagebox.showerror("Error", "Por favor, selecciona un cliente para eliminar.")

# Limpiar campos del formulario
def limpiar_campos():
    for var in [apellido_var, nombre_var, fecha_nacimiento_var, sexo_var,
                tipo_doc_primario_var, documento_primario_var, tipo_doc_secundario_var,
                documento_secundario_var, fecha_emision_var, fecha_vencimiento_var,
                telefono_var, email_var]:
        var.set("")

# Validador para el campo de fecha de nacimiento
def validar_fecha_nacimiento(event):
    contenido = fecha_nacimiento_var.get()

    # Filtrar solo números
    contenido_filtrado = ''.join([c for c in contenido if c.isdigit()])

    # Formatear la fecha con las barras
    if len(contenido_filtrado) > 2 and len(contenido_filtrado) <= 4:
        contenido_formateado = contenido_filtrado[:2] + '/' + contenido_filtrado[2:]
    elif len(contenido_filtrado) > 4 and len(contenido_filtrado) <= 6:
        contenido_formateado = contenido_filtrado[:2] + '/' + contenido_filtrado[2:4] + '/' + contenido_filtrado[4:]
    elif len(contenido_filtrado) > 6:
        contenido_formateado = contenido_filtrado[:2] + '/' + contenido_filtrado[2:4] + '/' + contenido_filtrado[4:8]
    else:
        contenido_formateado = contenido_filtrado

    # Establecer el texto en la variable y mover el cursor al final del texto
    fecha_nacimiento_var.set(contenido_formateado)
    fecha_nacimiento_entry.icursor(len(contenido_formateado))

# Validador para el campo de documento
def validar_documento(event):
    contenido = documento_primario_var.get()

    # Filtrar solo números
    contenido_filtrado = ''.join([c for c in contenido if c.isdigit()])

    # Verificar si contiene algún carácter no numérico
    if len(contenido) != len(contenido_filtrado):
        messagebox.showerror("Error", "Solo se pueden ingresar números en el campo Documento.")
        documento_primario_var.set(contenido_filtrado)
        return

    # Actualizar el contenido con solo los números
    documento_primario_var.set(contenido_filtrado)

# Validador para el campo de teléfono
def validar_telefono(event):
    contenido = telefono_var.get()

    # Filtrar solo números
    contenido_filtrado = ''.join([c for c in contenido if c.isdigit()])

    # Verificar si contiene algún carácter no numérico
    if len(contenido) != len(contenido_filtrado):
        messagebox.showerror("Error", "Solo se pueden ingresar números en el campo Teléfono.")
        telefono_var.set(contenido_filtrado)
        return

    # Actualizar el contenido con solo los números
    telefono_var.set(contenido_filtrado)

# Configuración de la interfaz
root = Tk()
root.title("Gestor de Clientes")
root.geometry("1200x600")
root.resizable(False, False)

# Variables
apellido_var = StringVar()
nombre_var = StringVar()
fecha_nacimiento_var = StringVar()
sexo_var = StringVar()
tipo_doc_primario_var = StringVar()
documento_primario_var = StringVar()
tipo_doc_secundario_var = StringVar()
documento_secundario_var = StringVar()
fecha_emision_var = StringVar()
fecha_vencimiento_var = StringVar()
telefono_var = StringVar()
email_var = StringVar()

# Frames
frame_formulario = Frame(root, bg="white", padx=20, pady=10)
frame_formulario.pack(fill="x", pady=5)

frame_tabla = Frame(root, bg="white", padx=20, pady=10)
frame_tabla.pack(fill="both", expand=True)

# Etiquetas y Entradas del formulario
Label(frame_formulario, text="Apellido:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
Entry(frame_formulario, textvariable=apellido_var).grid(row=0, column=1, padx=5, pady=5)

Label(frame_formulario, text="Nombre:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
Entry(frame_formulario, textvariable=nombre_var).grid(row=0, column=3, padx=5, pady=5)

Label(frame_formulario, text="Fecha Nacimiento:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
fecha_nacimiento_entry = Entry(frame_formulario, textvariable=fecha_nacimiento_var)
fecha_nacimiento_entry.grid(row=1, column=1, padx=5, pady=5)
fecha_nacimiento_entry.bind("<KeyRelease>", validar_fecha_nacimiento)

Label(frame_formulario, text="Sexo:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
ttk.Combobox(frame_formulario, textvariable=sexo_var, values=["Masculino", "Femenino", "Otro"]).grid(row=1, column=3, padx=5, pady=5)

Label(frame_formulario, text="Tipo Doc.:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
ttk.Combobox(frame_formulario, textvariable=tipo_doc_primario_var, values=["DNI", "Pasaporte"]).grid(row=2, column=1, padx=5, pady=5)

Label(frame_formulario, text="Documento:").grid(row=2, column=2, sticky="e", padx=5, pady=5)
documento_entry = Entry(frame_formulario, textvariable=documento_primario_var)
documento_entry.grid(row=2, column=3, padx=5, pady=5)
documento_entry.bind("<KeyRelease>", validar_documento)

Label(frame_formulario, text="Teléfono:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
telefono_entry = Entry(frame_formulario, textvariable=telefono_var)
telefono_entry.grid(row=3, column=1, padx=5, pady=5)
telefono_entry.bind("<KeyRelease>", validar_telefono)

Label(frame_formulario, text="Email:").grid(row=3, column=2, sticky="e", padx=5, pady=5)
Entry(frame_formulario, textvariable=email_var).grid(row=3, column=3, padx=5, pady=5)

# Tabla
columns = ("ID", "Apellido", "Nombre", "Fecha Nac.", "Sexo", "Tipo Doc.", "Documento", "Teléfono", "Email")
tabla = ttk.Treeview(frame_tabla, columns=columns, show="headings")
tabla.pack(fill="both", expand=True)

for col in columns:
    tabla.heading(col, text=col)

# Botones
Button(root, text="Guardar", command=guardar_cliente).pack(side="left", padx=10, pady=10)
Button(root, text="Eliminar", command=eliminar_cliente).pack(side="left", padx=10, pady=10)

# Inicializar base de datos y cargar datos en la tabla
inicializar_base_datos()
cargar_datos_en_tabla()

root.mainloop()

