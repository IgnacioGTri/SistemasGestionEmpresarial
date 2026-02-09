import json
from datetime import datetime


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
    
    #Motor de Business Intelligence del almacén.
    

    def __init__(self, productos):
        self.productos = productos
        self.logs_errores = []
        self.procesados_ok = 0
        self.procesados_error = 0

    def get_aggregate_data(self, campo_a_sumar, campo_de_agrupacion):
        
       # Agrupa y suma datos dinámicamente usando getattr.
       
        resultado = {}

        for producto in self.productos:
            try:
                clave = getattr(producto, campo_de_agrupacion)
                valor = getattr(producto, campo_a_sumar)

                if not isinstance(valor, (int, float)):
                    raise TypeError("Dato no numérico")

                resultado[clave] = resultado.get(clave, 0) + valor
                self.procesados_ok += 1

            except Exception as error:
                self.procesados_error += 1
                self.logs_errores.append(
                    f"Error en producto {producto.referencia}: {error}"
                )

        return resultado

    #he tenido que buscar ayuda con el tena de rankis, no me quedaba del todo claro
    def get_kpi_ranking(self, n=5, criterio="precio"):
        #Genera un ranking de los productos basado en un criterio específico (precio, coste o stock).
        productos_validos = []
        
        for producto in self.productos:
            try:
                valor = getattr(producto, criterio)

                if not isinstance(valor, (int, float)):
                    raise TypeError("Dato no numérico")

                productos_validos.append(producto)

            except Exception as error:
                self.logs_errores.append(
                    f"Error al obtener {criterio} para producto {producto.referencia}: {error}"
                )

        total = sum(getattr(p, criterio) for p in productos_validos)   
        
        ranking = sorted( 
            #esto basicamente lo ha escrito el IDE
            productos_validos, key=lambda x: getattr(x, criterio), reverse=True
        )[:n]
        
        resultado = []
        for producto in ranking:
            valor = getattr(producto, criterio)
            porcentaje = (valor / total) * 100 if total > 0 else 0
            resultado.append({
                "producto": producto.nombre,
                "valor": valor,
                "porcentaje": round(porcentaje, 2)
            })

        return resultado


def exportar_a_json(datos):
  
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"informe_almacen_{fecha}.json"

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    return nombre_archivo


if __name__ == "__main__":
    productos = [
        Producto("PROD001", "Monitor", 10, 199.99, 120.0, "Hardware", "Madrid"),
        Producto("PROD002", "Teclado", 20, 49.99, 20.0, "Hardware", "Madrid"),
        Producto("PROD003", "Ratón", 15, 19.99, 5.0, "Hardware", "Valencia"),
        Producto("PROD004", "Portátil", 5, 899.99, 600.0, "Hardware", "Murcia"),
        Producto("PROD005", "Impresora", 7, 149.99, 90.0, "Hardware", "Valencia"),
        Producto("PROD006", "Tablet", 12, 299.99, 180.0, "Software", "Madrid"),
        Producto("PROD007", "Router", 9, 79.99, 40.0, "Software", "Murcia"),
        Producto("PROD008", "Webcam", 14, 59.99, 25.0, "Hardware", "Valencia"),
        Producto("PROD009", "Altavoces", 11, 89.99, 45.0, "Software", "Madrid"),
        Producto("PROD010", "Disco SSD", 8, 129.99, 70.0, "Hardware", "Murcia"),

        # productos corruptos a propósito como el enunciado del HIto 3
        Producto("PROD011", "Pantalla rota", "ERROR_DATA", 99.99, 50.0, "Hardware", "Madrid"),
        Producto("PROD012", "Cámara", None, 59.99, 30.0, "Hardware", "Murcia"),
    ]

    almacen = Almacen(productos)

    totales = almacen.get_aggregate_data("stock", "provincia")
    ranking = almacen.get_kpi_ranking(n=5, criterio="precio")

    informe = {
        "totales_stock_por_provincia": totales,
        "ranking_top_5_por_precio": ranking,
        "errores": almacen.logs_errores,
        "procesados_ok": almacen.procesados_ok,
        "procesados_error": almacen.procesados_error
    }

    archivo_generado = exportar_a_json(informe)
    
    print("Informe generado correctamente")
    print("Totales por provincia:", totales)
    print("Ranking Top 5 por precio:")
    for item in ranking:
        print(item)

    print("Procesados correctamente:", almacen.procesados_ok)
    print("Procesados con error:", almacen.procesados_error)
