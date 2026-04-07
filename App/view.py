import sys
from tabulate import tabulate
import App.logic as lg
import DataStructures.List.array_list as al
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    control = lg.new_logic()
    return control

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    filename = "computer_prices_100.csv"
    (total, os_counts,
     min_year, max_year,
     min_price, max_price,
     delta_time, delta_memory,
     first_five, last_five) = lg.load_data(control, filename)
    
    summary = [
        ["Total de computadores cargados", total],
        ["Año mínimo de lanzamiento",      min_year  if min_year  is not None else "N/A"],
        ["Año máximo de lanzamiento",      max_year  if max_year  is not None else "N/A"],
        ["Precio mínimo (USD)",            f"${min_price:,.2f}" if min_price is not None else "N/A"],
        ["Precio máximo (USD)",            f"${max_price:,.2f}" if max_price is not None else "N/A"],
        ["Tiempo de carga (ms)",           f"{delta_time:.2f}"],
        ["Memoria utilizada (KB)",         f"{delta_memory:.2f}"],
    ]
 
    print("\n" + "=" * 55)
    print("          RESUMEN DE CARGA DE DATOS")
    print("=" * 55)
    print(tabulate(summary,
                   headers=["Métrica", "Valor"],
                   tablefmt="rounded_outline",
                   colalign=("left", "right")))
 
    #  Distribución por sistema operativo 
    #os_rows = sorted(os_counts.items(), key=lambda x: x[1], reverse=True)
 
    print("\n" + "=" * 55)
    print("       DISTRIBUCIÓN POR SISTEMA OPERATIVO")
    print("=" * 55)
    os_rows = []
    for i in range(al.size(os_counts)):
        os_rows.append(al.get_element(os_counts, i))
    print(tabulate(os_rows,
                   headers=["Sistema Operativo", "Cantidad"],
                   tablefmt="rounded_outline",
                   colalign=("left", "right")))
    print()
 
    # Primeros 5 y últimos 5 ordenados desc. por precio
    def _comp_rows(lst):
        rows = []
        for i in range(al.size(lst)):
            c = al.get_element(lst, i)
            storage = c.get("storage_gb", "N/A") or "N/A"
            try:
                storage = f"{float(storage):,.0f} GB"
            except (ValueError, TypeError):
                storage = "N/A"
            price = c.get("price", "N/A") or "N/A"
            try:
                price = f"${float(price):,.2f}"
            except (ValueError, TypeError):
                price = "N/A"
            rows.append([
                c.get("brand",       "N/A") or "N/A",
                c.get("model",       "N/A") or "N/A",
                c.get("device_type", "N/A") or "N/A",
                c.get("cpu_model",   "N/A") or "N/A",
                c.get("ram_gb",      "N/A") or "N/A",
                storage,
                c.get("release_year","N/A") or "N/A",
                price,
            ])
        return rows
 
    headers_comp = ["Marca", "Modelo", "Tipo", "CPU", "RAM (GB)",
                    "Almacenamiento", "Año", "Precio"]
 
    print("\n" + "=" * 100)
    print("   PRIMEROS 5 EQUIPOS (mayor precio)")
    print("=" * 100)
    print(tabulate(_comp_rows(first_five), headers=headers_comp,
                   tablefmt="rounded_outline"))
 
    if al.size(last_five) > 0:
        print("\n" + "=" * 100)
        print("   ÚLTIMOS 5 EQUIPOS (menor precio)")
        print("=" * 100)
        print(tabulate(_comp_rows(last_five), headers=headers_comp,
                       tablefmt="rounded_outline"))
    print()


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    computers = control["model"]["computers"]
    size = al.size(computers)

    if id < 0 or id >= size:
        print(f"\n[!] ID {id} fuera de rango. Total de registros: {size}")
        return

    comp = al.get_element(computers, id)

    # Construye filas con todos los campos disponibles
    rows = [[key, value if value not in ("", None) else "N/A"]
            for key, value in comp.items()]

    print("\n" + "=" * 55)
    print(f"       DETALLE DEL COMPUTADOR  (índice {id})")
    print("=" * 55)
    print(tabulate(rows,
                   headers=["Campo", "Valor"],
                   tablefmt="rounded_outline",
                   colalign=("left", "left")))
    print()

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
