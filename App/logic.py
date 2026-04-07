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
    os_counts = al.new_list()
    keys = lp.key_set(catalog["computers_by_os"])
    for i in range(al.size(keys)):
        os_name = al.get_element(keys, i)
        os_list = lp.get(catalog["computers_by_os"], os_name)
        al.add_last(os_counts, (os_name, al.size(os_list)))
 
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
 
    sorted_computers = al.sub_list(catalog["computers"], 0, al.size(catalog["computers"]))
    al.merge_sort(sorted_computers, sort_by_price_desc_model_asc)
 
    n = al.size(sorted_computers)
    if n <= 10:
        first_five = al.sub_list(sorted_computers, 0, n)
        last_five  = al.new_list()
    else:
        first_five = al.sub_list(sorted_computers, 0, 5)
        last_five  = al.sub_list(sorted_computers, n - 5, 5)
 
    return (
        total_computers,
        os_counts,
        min_year, max_year,
        min_price, max_price,
        delta_time, delta_memory,
        first_five, last_five,
    )
 

# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass

def req_2(catalog, nucleos, año_de_lanzamiento):
    cumplen=0
    peso_total=0
    inicio=getTime()
    mapa=sc.new_map()
    tamaño=al.size(catalog["computers"])
    for i in range (tamaño):
        computador=al.get_element(catalog["computers"],i)
        clave = (computador["cpu_cores"], computador["release_year"])
        if not sc.contains(mapa,clave):  #si no esta la clave en el mapa creo la lista de computadores y meto la nueva llave
            lista=al.new_list()
            sc.put(mapa, clave, lista)
            
        else: #si la llave ya existe
            lista=sc.get(mapa,clave)
            
        al.add_last(lista,computador)
        
    #debo ordenar con merge me interesa comparar por peso y el criterio de desempate es model
        
        
    clave_busqueda=nucleos,año_de_lanzamiento # de lo que ya filtre previamente ahora solo busco lo que me interesa
    
    if sc.contains(mapa,clave_busqueda):
        lista_onjetivo=sc.get(mapa,clave_busqueda)
        tamaño_objetivo=al.size(lista_onjetivo)
        for i in range(tamaño_objetivo):
            computador=al.get_element(lista_onjetivo,i)
            cumplen+=1
            peso_total+=computador["weight_kg"]
            
    else:
        return 0, 0, None, deltaTime(inicio, getTime())
    
    peso_promedio=peso_total/cumplen
    fin=getTime()
    
    return cumplen, peso_promedio, lista_onjetivo, deltaTime(inicio, fin)
    


    
   


def req_3(catalog, n, gpu_model, brand):
    
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    Inicio = getTime()
    

   
    GPU = lp.get(catalog["computers_by_gpu"], gpu_model)

    lista_filtrada = al.new_list()
    ram = 0

    if GPU is not None:
        gpu_list = GPU["value"]
        
        for i in range(al.size(gpu_list)):
            comp = al.get_element(gpu_list, i)

            if comp.get("brand", "") == brand:
                al.add_last(lista_filtrada, comp)
                ram += float(comp.get("ram", 0))
               

    
    total = al.size(lista_filtrada)
    if total > 0:
        promedio_ram = ram / total
    else:
        promedio_ram = 0

    al.merge_sort(lista_filtrada)

   
    if n > total:
        n = total

    resultado_n  = al.sub_list(lista_filtrada, 0, n)

    Final  = getTime()
    

    Tiempo_final = Final - Inicio

    return {
        "execution_time": Tiempo_final,
        "total": total,
        "avg_ram": promedio_ram,
        "top_n": resultado_n
    }


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
def sort_by_price_desc_model_asc(comp_a, comp_b):
    """
    Criterio de ordenamiento para merge_sort (retorna True si comp_a debe ir ANTES que comp_b).
    Ordena por precio de forma descendente y, en caso de empate, por modelo de forma ascendente.
    """
    try:
        price_a = float(comp_a.get("price", 0) or 0)
    except ValueError:
        price_a = 0.0
    try:
        price_b = float(comp_b.get("price", 0) or 0)
    except ValueError:
        price_b = 0.0
 
    if price_a != price_b:
        return price_a > price_b          # desc por precio
    model_a = str(comp_a.get("model", "") or "")
    model_b = str(comp_b.get("model", "") or "")
    return model_a < model_b  
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