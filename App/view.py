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
            storage = c["storage_gb"] or "N/A"
            if storage != "N/A":
                storage = f"{float(storage):,.0f} GB"
            else:
                storage = "N/A"
            price = "N/A"
            if c["price"]:
                price = f"${float(c["price"]):,.2f}"
            rows.append([
                c["brand"] or "N/A",
                c["model"] or "N/A",
                c["device_type"] or "N/A",
                c["cpu_model"] or "N/A",
                c["ram_gb"] or "N/A",
                storage,
                c["release_year"] or "N/A",
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
        print(f"\n! ID {id} fuera de rango. Total de registros: {size}")
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

def print_req_1(control, brand, form_factor):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    def build_row(comp):
        device_type = comp["device_type"] or "N/A"
        model = comp["model"] or "N/A"
        os = comp["os"] or "N/A"
        cpu_brand = comp["cpu_brand"] or "N/A"
        ram_gb = comp["ram_gb"] or "N/A"
        storage_capacity = comp["storage_gb"] or "N/A"
        price = "N/A"
        if comp["price"]:
            price = f"${float(comp["price"]):,.2f}"
        return [device_type, model, os, cpu_brand, ram_gb, storage_capacity, price]
    
    start_time = lg.getTime()
    total, avg_price, sorted_list = lg.req_1(control, brand, form_factor)
    stop_time = lg.getTime()
    delta_time = lg.deltaTime(stop_time, start_time)
    
    print(f"\nTiempo de ejecución: {delta_time:.2f} ms")
    print(f"Total de computadores encontrados: {total}")
    print(f"Precio promedio: ${avg_price:,.2f}")
    
    
    rows = []
    size = al.size(sorted_list)
    if size > 20:
        # primeros 10
        for i in range(10):
            comp = al.get_element(sorted_list, i)
            rows.append(build_row(comp))
        # ultimos 10
        for i in range(size - 10, size):
            comp = al.get_element(sorted_list, i)
            rows.append(build_row(comp))
    else:
        for i in range(size):
            comp = al.get_element(sorted_list, i)
            rows.append(build_row(comp))
    
    headers = ["Tipo", "Modelo", "OS", "CPU Brand", "RAM (GB)", "Almacenamiento", "Precio (USD)"]
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass



def print_req_3(control, n, gpu_model, brand):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    total, promedio_ram, resultado_n = lg.req_3(control, n, gpu_model, brand)

    print(f"\nTiempo de ejecución: {Tiempo_final:.2f} ms")
    print(f"Total de computadores encontrados: {total}")
    print(f"RAM promedio: {promedio_ram:.2f} GB")

    rows = []
    size = al.size(resultado_n)

    for i in range(size):
        comp = al.get_element(resultado_n, i)
        device_type = comp.get("device_type") or "N/A"
        model = comp.get("model") or "N/A"
        ram = comp.get("ram_gb") or "N/A"
        storage = comp.get("storage_gb") or "N/A"
        gpu_brand = comp.get("gpu_brand") or "N/A"
        gpu_mod = comp.get("gpu_model") or "N/A"
        weight = comp.get("weight_kg") or "N/A"
        price = f"${float(comp['price']):,.2f}" if comp.get("price") else "N/A"
        rows.append([device_type, model, ram, storage, gpu_brand, gpu_mod, weight, price])

    headers = ["Tipo", "Modelo", "RAM (GB)", "Almacenamiento", "Marca GPU", "Modelo GPU", "Peso", "Precio"]
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))


def print_req_4(control, cpu_brand, gpu_model):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    start_time = lg.getTime()
    total, avg_price, avg_vram, avg_ram, avg_boost, sorted_list = lg.req_4(control, cpu_brand, gpu_model)
    stop_time = lg.getTime()
    delta_time = lg.deltaTime(stop_time, start_time)
    
    print(f"\nTiempo de ejecución: {delta_time:.2f} ms")
    print(f"Total de computadores encontrados: {total}")
    print(f"Precio promedio: ${avg_price:,.2f}")
    print(f"VRAM promedio: {avg_vram:.2f} GB")
    print(f"RAM promedio: {avg_ram:.2f} GB")
    print(f"Boost promedio: {avg_boost:.2f} GHz")
    
    
    rows = []
    size = al.size(sorted_list)
    for i in range(min(2, size)):
        comp = al.get_element(sorted_list, i)
        model = comp["model"] or "N/A"
        brand = comp["brand"] or "N/A"
        year = comp["release_year"] or "N/A"
        cpu_model = comp["cpu_model"] or "N/A"
        price = f"${float(comp['price']):,.2f}" if comp["price"] else "N/A"
        rows.append([model, brand, year, cpu_model, price])
    
    headers = ["Modelo", "Marca", "Año", "CPU Model", "Precio"]
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))


def print_req_5(control, n, initial_release_year, final_release_year, brand, form_factor):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control, n, form_factor, display_type, año_inicial, año_final):
    """
    Función que imprime la solución del Requerimiento 6 en consola
    """
    tiempo_final, total, contador_windows, contador_linux, resultado_n = lg.req_6(control, n, form_factor, display_type, año_inicial, año_final)

    print(f"\nTiempo de ejecución: {tiempo_final:.2f} ms")
    print(f"Total de computadores encontrados: {total}")
    print(f"Total con Windows: {contador_windows}")
    print(f"Total con Linux: {contador_linux}")

    rows = []
    size = al.size(resultado_n)

    for i in range(size):
        comp = al.get_element(resultado_n, i)
        model = comp.get("model") or "N/A"
        ram = comp.get("ram_gb") or "N/A"
        cpu_model = comp.get("cpu_model") or "N/A"
        cpu_boost = comp.get("cpu_boost_ghz") or "N/A"
        cpu_max = comp.get("cpu_boost_ghz") or "N/A"
        score = f"{float(comp['efficiency_score']):.4f}" if comp.get("efficiency_score") else "N/A"
        rows.append([model, ram, cpu_model, cpu_boost, cpu_max, score])

    headers = ["Modelo", "RAM (GB)", "Modelo CPU", "Boost CPU", "Frec. Máx CPU", "Puntaje Eficiencia"]
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))

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
            brand = input("Ingrese la marca a buscar: ")
            form_factor = input("Ingrese el factor de forma a buscar (ATX, SFF, MICRO-ATX): ")
            print_req_1(control, brand, form_factor)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            n = int(input("Ingrese el número de resultados a mostrar: "))
            gpu_model = input("Ingrese el modelo de GPU a buscar: ")
            brand = input("Ingrese la marca a buscar: ")
            print_req_3(control, n, gpu_model, brand)

        elif int(inputs) == 4:
            cpu_brand = input("Ingrese la marca de CPU a buscar: ")
            gpu_model = input("Ingrese el modelo de GPU a buscar: ")
            print_req_4(control, cpu_brand, gpu_model)

        elif int(inputs) == 5:
            n = int(input("Ingrese el número de resultados a mostrar: "))
            initial_release_year = input("Ingrese el año de lanzamiento inicial: ")
            final_release_year = input("Ingrese el año de lanzamiento final: ")
            brand = input("Ingrese la marca a buscar: ")
            form_factor = input("Ingrese el factor de forma a buscar (ATX, SFF, MICRO-ATX): ")
            print_req_5(control, n, initial_release_year, final_release_year, brand, form_factor)

        elif int(inputs) == 6:
            n = int(input("Ingrese el número de resultados a mostrar: "))
            form_factor = input("Ingrese el factor de forma a buscar (ATX, SFF, MICRO-ATX): ")
            display_type = input("Ingrese el tipo de pantalla a buscar (LCD, LED, OLED): ")
            print_req_6(control, n, form_factor, display_type)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
