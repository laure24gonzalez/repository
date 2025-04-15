import sqlite3

# conecta a la base de datos
conexion = sqlite3.connect("provincias_ciudades.db")
cursor = conexion.cursor()

# tabla Provincias
cursor.execute("""
CREATE TABLE Provincias (
    ID INTEGER PRIMARY KEY,
    Nombre TEXT NOT NULL
)
""")

# tabla Ciudades
cursor.execute("""
CREATE TABLE Ciudades (
    ID INTEGER PRIMARY KEY,
    CodPostal TEXT NOT NULL,
    CPA TEXT NOT NULL,
    Nombre TEXT NOT NULL,
    IDProvincia INTEGER NOT NULL,
    FOREIGN KEY (IDProvincia) REFERENCES Provincias(ID)
)
""")

conexion.commit()
print("Tablas creadas exitosamente.")
conexion.close()

conexion = sqlite3.connect("provincias_ciudades.db")
cursor = conexion.cursor()

# datos en la tabla Provincias
provincias = [
    (1, "Buenos Aires"),
    (2, "Córdoba"),
    (3, "Santa Fe"),
    (4, "San Luis")
]

cursor.executemany("INSERT INTO Provincias (ID, Nombre) VALUES (?, ?)", provincias)

# datos en la tabla Ciudades
ciudades = [
    (1, "6550", "CPA1", "Bolivar", 1),
    (2, "7263", "CPA2", "Alvear", 1),
    (3, "6465", "CPA3", "Henderson", 1),
    (4, "2233", "CPA4", "Villa Maria", 2),
    (5, "8575", "CPA5", "San Francisco", 2),
    (6, "9282", "CPA6", "Rio Tercero", 2),
    (7, "3223", "CPA7", "Rosario", 3),
    (8, "6699", "CPA8", "Rafaela", 3),
    (9, "7898", "CPA9", "Justo Daract", 4),
    (10, "4828", "CPA10", "Merlo", 4)
]

cursor.executemany("""
INSERT INTO Ciudades (ID, CodPostal, CPA, Nombre, IDProvincia)
VALUES (?, ?, ?, ?, ?)
""", ciudades)

conexion.commit()
print("Datos insertados exitosamente.")
conexion.close()

def consultar_ciudades_por_provincias(nombres_provincias):
    conexion = sqlite3.connect("provincias_ciudades.db")
    cursor = conexion.cursor()

    placeholders = ', '.join('?' for _ in nombres_provincias)
    query = f"""
    SELECT c.Nombre FROM Ciudades c
    JOIN Provincias p ON c.IDProvincia = p.ID
    WHERE p.Nombre IN ({placeholders})
    """
    cursor.execute(query, nombres_provincias)
    ciudades = cursor.fetchall()

    print("Ciudades encontradas:", [ciudad[0] for ciudad in ciudades])
    conexion.close()

# consulta
consultar_ciudades_por_provincias(["Buenos Aires", "Santa Fe"])

def consultar_ciudades_ordenadas(id_provincia, orden="Nombre"):
    conexion = sqlite3.connect("provincias_ciudades.db")
    cursor = conexion.cursor()

    query = f"SELECT * FROM Ciudades WHERE IDProvincia = ? ORDER BY {orden}"
    cursor.execute(query, (id_provincia,))
    ciudades = cursor.fetchall()

    print("Ciudades ordenadas:", ciudades)
    conexion.close()


consultar_ciudades_ordenadas(1, orden="CodPostal")

def actualizar_nombre_ciudad(id_ciudad, nuevo_nombre):
    conexion = sqlite3.connect("provincias_ciudades.db")
    cursor = conexion.cursor()

    cursor.execute("""
    UPDATE Ciudades SET Nombre = ? WHERE ID = ?
    """, (nuevo_nombre, id_ciudad))

    conexion.commit()
    print(f"Ciudad con ID {id_ciudad} actualizada a {nuevo_nombre}.")
    conexion.close()

# actualización
actualizar_nombre_ciudad(1, "Bolívar 2.0")

def eliminar_ciudad(id_ciudad):
    conexion = sqlite3.connect("provincias_ciudades.db")
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Ciudades WHERE ID = ?", (id_ciudad,))
    conexion.commit()
    print(f"Ciudad con ID {id_ciudad} eliminada.")
    conexion.close()

def eliminar_provincia(id_provincia):
    conexion = sqlite3.connect("provincias_ciudades.db")
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Ciudades WHERE IDProvincia = ?", (id_provincia,))
    cursor.execute("DELETE FROM Provincias WHERE ID = ?", (id_provincia,))
    conexion.commit()
    print(f"Provincia con ID {id_provincia} y sus ciudades eliminadas.")
    conexion.close()

# eliminación
eliminar_ciudad(10)
eliminar_provincia(4)
