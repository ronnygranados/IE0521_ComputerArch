# Tarea 4 IE0521-Estructuras de Computadoras II
# Lorena Solís Extteny B97657
# Ronny Granados Perez C03505
#-*- coding: utf-8 -*-
from math import log2, floor
import random

class cache:
    def __init__(self, cache_capacity, cache_assoc, block_size, repl_policy):
        # Inicializa las variables de acceso y fallos
        self.total_access = 0
        self.total_misses = 0
        
        # Configuración del caché
        self.cache_capacity = int(cache_capacity)  # Capacidad del caché en kB
        self.cache_assoc = int(cache_assoc)  # Asociatividad del caché
        self.block_size = int(block_size)  # Tamaño del bloque en Bytes
        self.repl_policy = repl_policy  # Política de reemplazo ('l' para LRU, 'r' para Random)
        
        # Calcular el número de sets en el caché
        self.num_sets = (self.cache_capacity * 1024) // (self.cache_assoc * self.block_size)
        self.cache = [[] for _ in range(self.num_sets)]  # Estructura del caché como lista de listas
        
        # Estructuras para LRU
        if repl_policy == 'l':
            # Inicializa contadores LRU para cada set
            self.lru_counters = [[] for _ in range(self.num_sets)]

    def print_info(self):
        # Imprime los parámetros del caché
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t" + str(self.cache_capacity) + "kB")
        print("\tAssociatividad:\t\t\t" + str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t" + str(self.block_size) + "B")
        print("\tPolítica de Reemplazo:\t\t\t" + str(self.repl_policy))
    
    def print_stats(self):
        # Imprime los resultados de la simulación
        print("Resultados de la simulación")
        miss_rate = (100.0 * self.total_misses) / self.total_access
        miss_rate = "{:.3f}".format(miss_rate)
        result_str = str(self.total_misses) + "," + miss_rate + "%"
        print(result_str)
    
    def access(self, access_type, address):
        # Incrementa el contador de accesos totales
        self.total_access += 1
        
        # Calcula el índice del set y el tag a partir de la dirección
        set_index = (address // self.block_size) % self.num_sets
        tag = address // (self.block_size * self.num_sets)
        cache_set = self.cache[set_index]
        
        # Verifica si es un hit
        for i, block in enumerate(cache_set):
            if block == tag:
                if self.repl_policy == 'l':
                    # Actualiza el contador LRU
                    self.lru_counters[set_index].remove(tag)
                    self.lru_counters[set_index].append(tag)
                return True
        
        # Manejo de misses
        self.total_misses += 1
        if len(cache_set) < self.cache_assoc:
            # Añade el nuevo bloque si el set no está lleno
            cache_set.append(tag)
            if self.repl_policy == 'l':
                self.lru_counters[set_index].append(tag)
        else:
            # Reemplaza un bloque existente si el set está lleno
            if self.repl_policy == 'l':
                # Reemplazo LRU
                evict = self.lru_counters[set_index].pop(0)
                cache_set.remove(evict)
                cache_set.append(tag)
                self.lru_counters[set_index].append(tag)
            elif self.repl_policy == 'r':
                # Reemplazo Random
                evict = random.choice(cache_set)
                cache_set.remove(evict)
                cache_set.append(tag)
        
        return False
