class Producto:
    
    #Representa un producto del almacén.
    

    def __init__(self, referencia, nombre, stock, precio, coste, categoria, provincia):
        self.referencia = referencia
        self.nombre = nombre
        self.stock = stock
        self.precio = precio
        self.coste = coste
        self.categoria = categoria
        self.provincia = provincia
class Almacen:

    def __init__(self, productos):
        self.productos = productos
        self.logs_errores = []

    def get_aggregate_data(self, campo_a_sumar, campo_de_agrupacion):
        resultado = {}

        for producto in self.productos:
            try:
                clave = getattr(producto, campo_de_agrupacion)
                valor = getattr(producto, campo_a_sumar)

                resultado[clave] = resultado.get(clave, 0) + valor

            except Exception as error:
                self.logs_errores.append(
                    f"Error en producto {producto.referencia}: {error}"
                )

        return resultado
    
if __name__ == "__main__":
        productos = [
        Producto("PROD001", "Monitor", 10, 199.99, 120.0, "Hardware", "Madrid"),
        Producto("PROD002", "Teclado", 20, 49.99, 20.0, "Software", "Murcia"),
        Producto("PROD003", "Ratón", 15, 19.99, 5.0, "Malware", "Valencia"),
        ]

        almacen = Almacen(productos)
        print(almacen.get_aggregate_data("stock", "provincia"))