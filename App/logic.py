import os
import csv
import time
import tracemalloc
 
import DataStructures.Map.map_linear_probing as lp
import DataStructures.Map.map_separate_chaining as sc
import DataStructures.List.array_list as al
csv.field_size_limit(2147483647)
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'Data')
def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        "computers": None,
        "computers_by_os": None,
        "computers_by_brand": None,
        "computers_by_cores_year": None,
        "computers_by_gpu_brand": None,
        "computers_by_cpu_brand_gpu_model": None,
        "computers_by_brand_form": None,
        "computers_by_form_display": None,
    }
    # Lista general
    catalog["computers"] = al.new_list()
 
    # Mapas de primer nivel
    catalog["computers_by_os"]                 = lp.new_map(10)
    catalog["computers_by_brand"]              = lp.new_map(30)
    catalog["computers_by_cores_year"]         = lp.new_map(20)
    catalog["computers_by_gpu_brand"]          = lp.new_map(200)
    catalog["computers_by_cpu_brand_gpu_model"]= lp.new_map(5)   # solo Intel / AMD
    catalog["computers_by_brand_form"]         = lp.new_map(30)
    catalog["computers_by_form_display"]       = lp.new_map(10)
 
    return catalog


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    tracemalloc.start()
    start_time   = getTime()
    start_memory = getMemory()
 
    filepath = os.path.join(data_dir, filename)
    input_file = csv.DictReader(open(filepath, encoding='utf-8'))
 
    for computer in input_file:
        add_computer(catalog, computer)
 
    stop_time   = getTime()
    stop_memory = getMemory()
 
    delta_time   = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(start_memory, stop_memory)
    tracemalloc.stop()
    total_computers = al.size(catalog["computers"])
 
    # Total por sistema operativo
    os_counts = {}
    keys = lp.key_set(catalog["computers_by_os"])
    for i in range(al.size(keys)):
        os_name = al.get_element(keys, i)
        os_list = lp.get(catalog["computers_by_os"], os_name)
        os_counts[os_name] = al.size(os_list)
 
    # Año mínimo / máximo y precio mínimo / máximo
    min_year = max_year = None
    min_price = max_price = None
 
    computers_list = catalog["computers"]
    for i in range(al.size(computers_list)):
        comp = al.get_element(computers_list, i)
 
        year = comp.get("release_year", "")
        if year not in ("", None):
            try:
                year_int = int(float(year))
                if min_year is None or year_int < min_year:
                    min_year = year_int
                if max_year is None or year_int > max_year:
                    max_year = year_int
            except ValueError:
                pass
 
        price = comp.get("price", "")
        if price not in ("", None):
            try:
                price_float = float(price)
                if min_price is None or price_float < min_price:
                    min_price = price_float
                if max_price is None or price_float > max_price:
                    max_price = price_float
            except ValueError:
                pass
 
    return (
        total_computers,
        os_counts,
        min_year, max_year,
        min_price, max_price,
        delta_time, delta_memory,
    )
 

# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass



def add_computer(catalog, computer):
    """
    Agrega un equipo a todas las estructuras del catálogo.
    """
    #Lista general
    al.add_last(catalog["computers"], computer)
 
    #Índice por sistema operativo
    add_to_nested_list(catalog["computers_by_os"], computer["os"], computer)
 
    #Índice por marca
    add_to_nested_list(catalog["computers_by_brand"], computer["brand"], computer)
 
    #Índice por núcleos → año
    cores = computer.get("cpu_cores", "desconocido") or "desconocido"
    year  = computer.get("release_year", "desconocido") or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_cores_year"],
        cores, year, computer
    )
 
    #Índice por modelo de GPU → marca
    gpu_model = computer.get("gpu_model", "desconocido") or "desconocido"
    brand     = computer.get("brand", "desconocido") or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_gpu_brand"],
        gpu_model, brand, computer
    )
 
    #Índice por marca de CPU → modelo de GPU
    cpu_brand = computer.get("cpu_brand", "desconocido") or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_cpu_brand_gpu_model"],
        cpu_brand, gpu_model, computer
    )
 
    #Índice por marca → factor de forma
    form_factor = computer.get("form_factor", "desconocido") or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_brand_form"],
        brand, form_factor, computer
    )
 
    #Índice por factor de forma → tipo de pantalla
    display_type = computer.get("display_type", "desconocido") or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_form_display"],
        form_factor, display_type, computer
    )
 
    return catalog
 
 
def add_to_nested_list(my_map, key, element):
    """
    Auxiliar: agrega element a la lista asociada a key en my_map.
    Si la llave no existe, crea una nueva lista.
    """
    key = str(key) if key not in ("", None) else "desconocido"
    lst = lp.get(my_map, key)
    if lst is None:
        lst = al.new_list()
        lp.put(my_map, key, lst)
    al.add_last(lst, element)
 
 
def add_to_double_nested_list(mapa_externo, outer_key, inner_key, element):
    """
    Auxiliar: estructura de dos niveles (mapa_externo[outer_key][inner_key] = lista).
    Si alguno de los niveles no existe, lo crea.
    """
    outer_key = str(outer_key) if outer_key not in ("", None) else "desconocido"
    inner_key = str(inner_key) if inner_key not in ("", None) else "desconocido"
 
    inner_map = lp.get(mapa_externo, outer_key)
    if inner_map is None:
        # El mapa interno guarda sub-llaves (años, form_factors, etc.)
        inner_map = lp.new_map(20)
        lp.put(mapa_externo, outer_key, inner_map)
 
    lst = lp.get(inner_map, inner_key)
    if lst is None:
        lst = al.new_list()
        lp.put(inner_map, inner_key, lst)
 
    al.add_last(lst, element)
    
#  -------------------------------------------------------------
# Funciones utilizadas para obtener memoria y tiempo
#  -------------------------------------------------------------

def getTime():
    """
    Devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter() * 1000)

def getMemory():
    """
    Toma una muestra de la memoria alocada en un instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaTime(end, start):
    """
    Devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    return float(end - start)

def deltaMemory(start_memory, stop_memory):
    """
    Calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en kBytes
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = sum(stat.size_diff for stat in memory_diff) / 1024.0
    return delta_memory