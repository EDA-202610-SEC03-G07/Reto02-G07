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
    catalog["computers_by_os"] = lp.new_map(10)
    catalog["computers_by_brand"] = lp.new_map(30)
    catalog["computers_by_cores_year"] = lp.new_map(20)
    catalog["computers_by_gpu_brand"] = lp.new_map(200)
    catalog["computers_by_cpu_brand_gpu_model"]= lp.new_map(5) 
    catalog["computers_by_brand_form"] = lp.new_map(30)
    catalog["computers_by_form_display"] = lp.new_map(10)
 
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
 
        price_float = 0.0
        if comp.get("price"):
            price_float = float(comp["price"])
            if min_price is None or price_float < min_price:
                min_price = price_float
            if max_price is None or price_float > max_price:
                max_price = price_float
 
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


def req_1(catalog, brand, form_factor):
    """
    Retorna el resultado del requerimiento 1
    """
    brand = brand.strip().upper()
    form_factor = form_factor.strip().upper()
    inner_map = lp.get(catalog["computers_by_brand_form"], brand)
    if inner_map is None:
        return (0, 0.0, al.new_list())
    lst = lp.get(inner_map, form_factor)
    if lst is None:
        return (0, 0.0, al.new_list())
    
    copied_list = al.new_list()
    for i in range(al.size(lst)):
        al.add_last(copied_list, al.get_element(lst, i))
    
    total = al.size(copied_list)

    sum_price = 0.0
    count = 0
    for i in range(total):
        comp = al.get_element(copied_list, i)
        price = 0.0
        if comp.get("price"):
            price = float(comp["price"])
            sum_price += price
            count += 1
    avg_price = sum_price / count if count > 0 else 0.0
    
    al.merge_sort(copied_list, sort_by_price_desc_model_asc)
    
    return (total, avg_price, copied_list)

def req_2(catalog, nucleos, año_de_lanzamiento):
    cumplen=0
    peso_total=0
    inicio=getTime()
    tamaño=al.size(catalog["computers"])
    mapa=sc.new_map(tamaño)
    for i in range (tamaño):
        computador=al.get_element(catalog["computers"],i)
        clave = (computador["cpu_cores"], computador["release_year"])
        if not sc.contains(mapa,clave):  #si no esta la clave en el mapa creo la lista de computadores y meto la nueva llave
            lista=al.new_list()
            sc.put(mapa, clave, lista)
            
        else: #si la llave ya existe
            lista=sc.get(mapa,clave)
            
        al.add_last(lista,computador)
        
        
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
    
    al.merge_sort(lista_onjetivo,sort_by_weight)
    
    fin=getTime()
        
    if al.size(lista_onjetivo)>20:
        primeros_10=al.sub_list(lista_onjetivo,0,10)
        ultimos_10=al.sub_list(lista_onjetivo,cumplen-10,10)
        return cumplen, peso_promedio, primeros_10, ultimos_10, deltaTime(inicio, fin)
    
    return cumplen, peso_promedio, lista_onjetivo, deltaTime(inicio, fin)

def req_3(catalog, n, gpu_model, brand):
    
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    gpu_model = gpu_model.strip().upper()
    brand = brand.strip().upper()
    Inicio = getTime()
    

   
    GPU = lp.get(catalog["computers_by_gpu_brand"], gpu_model)

    lista_filtrada = al.new_list()
    ram = 0
    
    if GPU is not None:
        gpu_list = lp.get(GPU, brand)

        if gpu_list is not None:
            for i in range(al.size(gpu_list)):
                comp = al.get_element(gpu_list, i)
                al.add_last(lista_filtrada, comp)
                ram += int(comp.get("ram_gb", 0))

               

    
    total = al.size(lista_filtrada)
    if total > 0:
        promedio_ram = ram / total
    else:
        promedio_ram = 0
        
    def criterio_ordenamiento(comp1, comp2):
        precio1 = float(comp1.get("price"))
        precio2 = float(comp2.get("price"))

        if precio1 > precio2:
            return True
        elif precio1 < precio2:
            return False
        else:
            peso1 = float(comp1.get("weight"))
            peso2 = float(comp2.get("weight"))
            return peso1 > peso2

    al.merge_sort(lista_filtrada,criterio_ordenamiento)

   
    if n > total:
        n = total

    resultado_n  = al.sub_list(lista_filtrada, 0, n)

    Final  = getTime()
    

    Tiempo_final = Final - Inicio

    return Tiempo_final,total,promedio_ram,resultado_n


def req_4(catalog, cpu_brand, gpu_model):
    """
    Retorna el resultado del requerimiento 4
    """
    cpu_brand = cpu_brand.strip().upper() 
    gpu_model = gpu_model.strip().upper() 
    
    inner_map = lp.get(catalog["computers_by_cpu_brand_gpu_model"], cpu_brand)
    # print("\n|-----------------------------|")
    # print(f"Inner map for CPU brand '{cpu_brand}': {inner_map}")
    # print(inner_map)
    # print("|-----------------------------|\n")
    if inner_map is None:
        return (0, 0.0, 0.0, 0.0, 0.0, al.new_list())
    lst = lp.get(inner_map, gpu_model)
    if lst is None:
        return (0, 0.0, 0.0, 0.0, 0.0, al.new_list())
    
   
    copied_list = al.new_list()
    for i in range(al.size(lst)):
        al.add_last(copied_list, al.get_element(lst, i))
    
    total = al.size(copied_list)

    sum_price = 0.0
    sum_vram = 0.0
    sum_ram = 0.0
    sum_boost = 0.0
    for i in range(total):
        comp = al.get_element(copied_list, i)
        price = float(comp["price"]) if comp["price"] else 0.0
        vram = float(comp["vram_gb"]) if comp["vram_gb"] else 0.0
        ram = float(comp["ram_gb"]) if comp["ram_gb"] else 0.0
        boost = float(comp["cpu_boost_ghz"]) if comp["cpu_boost_ghz"] else 0.0
        sum_price += price
        sum_vram += vram
        sum_ram += ram
        sum_boost += boost
    
    avg_price = sum_price / total if total > 0 else 0.0
    avg_vram = sum_vram / total if total > 0 else 0.0
    avg_ram = sum_ram / total if total > 0 else 0.0
    avg_boost = sum_boost / total if total > 0 else 0.0
    
   
    al.merge_sort(copied_list, sort_by_price_desc_weight_asc)
    
    return (total, avg_price, avg_vram, avg_ram, avg_boost, copied_list)


def req_5(catalog, n, initial_release_year, final_release_year, brand, form_factor):
    inicio=getTime()
    
    numero_AMD=0
    numero_INTEL=0
    cumplen=0
    tamaño=al.size(catalog["computers"])
    lista_cumplen=al.new_list()
    
    brand = brand.strip().upper()
    form_factor = form_factor.strip().upper() #el form factor que me intereza
    initial_release_year = int(initial_release_year) #el año en el que inicia el rango que me interesa 
    final_release_year = int(final_release_year) #el año en el que finaliza el rango que me interesa
    
    mapa=sc.new_map(tamaño)
    for i in range(tamaño):
        computador=al.get_element(catalog["computers"],i)
        clave = (computador["form_factor"].strip().upper(), computador["brand"].strip().upper())
        if not sc.contains(mapa,clave):
            lista=al.new_list()
            sc.put(mapa,clave,lista)
            
        else:
            lista=sc.get(mapa,clave)
            
        al.add_last(lista,computador) #hasta aca cree las llaves marca y factor de forma y las listas y añado cada computador
        
        #necesito recorrer la lsta de la clave que me interesa
        
    clave_busqueda=(form_factor,brand)
    
    if not sc.contains(mapa,clave_busqueda):# si la clave no existe dentro del mapa retorno falso
        fin=getTime()
        return 0, 0, None, 0, deltaTime(inicio, fin)
    
    else:
        lista_objetivo=sc.get(mapa,clave_busqueda) # si la llave existe saco la lista y la recorro en busca de los computadores q me sirven
        tamaño_obj=al.size(lista_objetivo)
        
        for i in range(tamaño_obj):
            computador=al.get_element(lista_objetivo,i)
            if initial_release_year <= computador["release_year"] <= final_release_year:
                cumplen+=1
                al.add_last(lista_cumplen,computador)
                if computador["cpu_brand"].strip().upper()=="INTEL":
                    numero_INTEL+=1
                    
                elif computador["cpu_brand"].strip().upper()=="AMD":  # reviso que los filtrados sean AMD o INTEL
                    numero_AMD+=1
                    
    #solo me interesan los N solicitados. Adicionalmente debo ordenarlos por Ram si es igual el primer criterio de 
    #desempate es por la cpu y el segundo por ram
    if cumplen == 0:
        fin=getTime()
        return 0, 0, None, 0, deltaTime(inicio, fin)
        
    al.merge_sort(lista_cumplen,sort_crit_req_6)
    
    if n > al.size(lista_cumplen): # si el n solicitado excede el numero de los que cumplen retorno los que cumplieron
        n=al.size(lista_cumplen)
    
    n_elements=al.sub_list(lista_cumplen,0,n) 
    
    fin=getTime()    
    return numero_AMD, numero_INTEL, n_elements, cumplen, deltaTime(inicio, fin)  
            
                    
        
        
        
        
        
     
    
    
    """
    1.debo recorrer todos los computadores
    2.para cada computador me intereza que se encuetre en el rango de años y que su form factor coincida con el que estoy consultando.
    3. 
    
    """
  

def req_6(catalog, n, form_factor, display_type, año_inicial, año_final):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    form_factor = form_factor.strip().upper()
    display_type = display_type.strip().upper() 
    Inicio = getTime()

    lista_filtrada = al.new_list()
    contador_windows = 0
    contador_linux = 0
    contador_total = 0
    
    mapa_pantallas = lp.get(catalog["computers_by_form_display"], form_factor)
    
    if mapa_pantallas is not None:
        computadoras_pantalla = lp.get(mapa_pantallas, display_type)
        
        if computadoras_pantalla is not None:
            for i in range(al.size(computadoras_pantalla)):
                comp = al.get_element(computadoras_pantalla, i)
                
                laptops = comp.get("device_type").strip().upper()
                año = int(comp.get("release_year"))
                
                if laptops == "LAPTOP" and int(año_final) >= año >= int(año_inicial):
                    battery_wh = float(comp.get("battery_wh"))
                    cpu_boost = float(comp.get("cpu_boost_ghz"))
                    charger_watts = float(comp.get("charger_watts"))
                    
                    puntaje_eficiente = (battery_wh * cpu_boost) / charger_watts 
                    comp["efficiency_score"] = puntaje_eficiente
                    al.add_last(lista_filtrada, comp)
                    
                    sistema_operativo = comp.get("os", "").strip().upper()
                    if sistema_operativo == "WINDOWS":
                        contador_windows += 1
                    elif sistema_operativo == "LINUX":
                        contador_linux += 1
    total = al.size(lista_filtrada)
    
    def criterio_ordenamiento(comp1, comp2):
        puntaje1 = comp1.get("efficiency_score", 0)
        puntaje2 = comp2.get("efficiency_score", 0)
        
        if puntaje1 > puntaje2:
            return True 
        elif puntaje1 < puntaje2:
            return False
        else:
            precio1 = float(comp1.get("price"))
            precio2 = float(comp2.get("price"))
            return precio1 < precio2
        
    al.merge_sort(lista_filtrada, criterio_ordenamiento)
    resultado_n = al.new_list()
    if n > total:
        n = total
        
    for i in range(n):
        al.add_last(resultado_n, al.get_element(lista_filtrada, i))
    Final = getTime()
    tiempo_final = Final - Inicio
    
    return tiempo_final,total,contador_windows,contador_linux,resultado_n


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
 
    #Índice por núcleos -> año
    cores = computer["cpu_cores"] or "desconocido"
    year  = computer["release_year"] or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_cores_year"],
        cores, year, computer
    )
 
    #Índice por modelo de GPU -> marca
    gpu_model = computer["gpu_model"] or "desconocido"
    brand     = computer["brand"] or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_gpu_brand"],
        gpu_model, brand, computer
    )
 
    #Índice por marca de CPU -> modelo de GPU
    cpu_brand = computer["cpu_brand"] or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_cpu_brand_gpu_model"],
        cpu_brand, gpu_model, computer
    )
 
    #Índice por marca -> factor de forma
    form_factor = computer["form_factor"] or "desconocido"
    add_to_double_nested_list(
        catalog["computers_by_brand_form"],
        brand, form_factor, computer
    )
 
    #Índice por factor de forma -> tipo de pantalla
    display_type = computer["display_type"] or "desconocido"
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
    outer_key = str(outer_key).strip().upper() if outer_key not in ("", None) else "DESCONOCIDO"
    inner_key = str(inner_key).strip().upper() if inner_key not in ("", None) else "DESCONOCIDO"
 
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
    is_sorted = False
    price_a = 0.0
    if comp_a["price"]:
        price_a = float(comp_a["price"])
    price_b = 0.0
    if comp_b["price"]:
        price_b = float(comp_b["price"])

    if price_a > price_b:
        is_sorted = True
    elif price_a == price_b:
        model_a = comp_a["model"] or ""
        model_b = comp_b["model"] or ""
        if model_a < model_b:
            is_sorted = True
    return is_sorted

def sort_by_weight(comp_a, comp_b):
    is_sorted = False
    weight_a = 0.0
    if comp_a["weight_kg"]:
        weight_a = float(comp_a["weight_kg"])
    weight_b = 0.0
    if comp_b["weight_kg"]:
        weight_b = float(comp_b["weight_kg"])

    if weight_a < weight_b:
        is_sorted = True
    elif weight_a == weight_b:
        model_a = comp_a["model"] or ""
        model_b = comp_b["model"] or ""
        if model_a < model_b:
            is_sorted = True
    return is_sorted

def sort_by_price_desc_weight_asc(comp_a, comp_b):
    """
    Criterio de ordenamiento para merge_sort (retorna True si comp_a debe ir ANTES que comp_b).
    Ordena por precio de forma descendente y, en caso de empate, por weight_kg de forma ascendente.
    """
    is_sorted = False
    price_a = float(comp_a["price"]) if comp_a["price"] else 0.0
    price_b = float(comp_b["price"]) if comp_b["price"] else 0.0

    if price_a > price_b:
        is_sorted = True
    elif price_a == price_b:
        weight_a = float(comp_a["weight_kg"]) if comp_a["weight_kg"] else 0.0
        weight_b = float(comp_b["weight_kg"]) if comp_b["weight_kg"] else 0.0
        if weight_a < weight_b:
            is_sorted = True
    return is_sorted

def sort_crit_req_6(comp_a, comp_b):
    is_sorted = False

    RAM_a = float(comp_a["ram_gb"] or 0)
    RAM_b = float(comp_b["ram_gb"] or 0)

    if RAM_a > RAM_b:
        is_sorted = True
    elif RAM_a < RAM_b:
        is_sorted = False
    else:
        vel_cpu_a = float(comp_a["cpu_boost_ghz"] or 0)
        vel_cpu_b = float(comp_b["cpu_boost_ghz"] or 0)

        if vel_cpu_a > vel_cpu_b:
            is_sorted = True
        elif vel_cpu_a < vel_cpu_b:
            is_sorted = False
        else:
            price_a = float(comp_a["price"] or 0)
            price_b = float(comp_b["price"] or 0)

            if price_a < price_b:
                is_sorted = True
            elif price_a > price_b:
                is_sorted = False

    return is_sorted
    
    
    
    
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