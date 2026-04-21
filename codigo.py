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
    print("3 - Mostrar Inventario")
    print("4 - Desactivar Producto")
    print("5 - Buscar Producto")

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

        cursor.execute("SELECT * FROM Productos WHERE activo = 1")
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

    elif opcion == "4":
        id_producto = int(input("Ingrese el ID del producto a desactivar: "))

        cursor.execute("""
                        UPDATE Productos
                        SET activo = 0
                        WHERE Id = ?
                        """, (id_producto,))
        
        conexion.commit()

        print("\n⚠ Producto desactivado Correctamente")


    elif opcion == "5":
        buscar_producto = input("Ingrese nombre a buscar: ").strip()

        buscar_producto = f"%{buscar_producto}%"

        cursor.execute("""
                       SELECT * FROM Productos
                       WHERE nombre LIKE ?
                       AND activo = 1 
                       """, (buscar_producto,))
        
        productos = cursor.fetchall()


        if not productos:
            print("❌ No hay productos con ese nombre")
        
        else:
            for producto in productos:
                print("-" * 40)
                print(f"ID: {producto[0]}")
                print(f"Nombre: {producto[1]}")
                print(f"Precio: {producto[2]}")
                print(f"Cantidad: {producto[3]}")
                print(f"Descripcion: {producto[4]}")


    else: 
        print("\n❌ ¡Opción Inválida! Elija una opción valida")
