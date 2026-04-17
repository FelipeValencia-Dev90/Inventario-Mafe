import pyodbc  

conexion = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
    'DATABASE=InventarioAVA;'
    'Trusted_Connection=yes;'
)

cursor = conexion.cursor()  

while True: 
    print("\nOpciones:")
    print("1 - Agregar Producto")
    print("2 - Salir")
    print("3 - mostrar Inventario")

    opcion = input("Elija una opcion: ")

    if opcion == "1":
        nombre = input("Ingrese el nombre del producto: ").strip().title() 
        precio = float(input("Ingresa el precio unítario del producto: "))
        cantidad = int(input("Ingrese la cantidad: "))
        descripcion = input("Ingrese la descripcion del producto: ").strip().title() 

        # INSERT DINÁMICO
        cursor.execute("""
        INSERT INTO Productos (nombre, precio, cantidad, descripcion)
        VALUES (?, ?, ?, ?)
        """, (nombre, precio, cantidad, descripcion))

        conexion.commit()   

        print("\n✅ Producto guardado correctamente")

    elif opcion == "2":
        print("\n✋ Salida del Sistema...")
        break

    elif opcion == "3":
        print("\n📦 Inventario Actual")

        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()

        if not productos:
            print("⚠ Inventario vacío")
        else:
            for producto in productos:
                print("-" * 40)
                print(f"ID: {producto[0]}")
                print(f"Nombre: {producto[1]}")
                print(f"Precio: {producto[2]}")
                print(f"Cantidad: {producto[3]}")
                print(f"Descripción: {producto[4]}")

    else: 
        print("\n❌ ¡Opción Inválida! Elija una opción valida")