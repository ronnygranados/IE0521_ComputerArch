
from math import log2, floor
import random

class cache:
    def __init__(self, cache_l1_capacity, cache_l1_assoc,
                       cache_l2_capacity, cache_l2_assoc,
                       cache_l3_capacity, cache_l3_assoc,
                       block_size, trace, repl_policy="l"):
        
    # def __init__(self, cache_l1_capacity, cache_l1_assoc, block_size, repl_policy="l"):
        
        self.total_access = 0
        self.total_misses = 0
        
        self.trace = trace

        # Caché: L1
        self.cache_l1_capacity = int(cache_l1_capacity)  # en kB
        self.cache_l1_assoc = int(cache_l1_assoc)
        
        # Caché: L2
        self.cache_l2_capacity = int(cache_l2_capacity)  # en kB
        self.cache_l2_assoc = int(cache_l2_assoc)
        
        # Caché: L3
        self.cache_l3_capacity = int(cache_l3_capacity)  # en kB
        self.cache_l3_assoc = int(cache_l3_assoc)
        
        self.block_size = int(block_size)  # en Bytes
        self.repl_policy = repl_policy

        # Calcular el número de sets
        self.num_sets = (self.cache_l1_capacity * 1024) // (self.cache_l1_assoc * self.block_size)
        self.num_l2_sets = (self.cache_l2_capacity * 1024) // (self.cache_l2_assoc * self.block_size)
        self.num_l3_sets = (self.cache_l3_capacity * 1024) // (self.cache_l3_assoc * self.block_size)

        self.cache = [[] for _ in range(self.num_sets)]  # Estructura del caché L1
        self.cache_l2 = [[] for _ in range(self.num_l2_sets)]  # Estructura del caché L1
        self.cache_l3 = [[] for _ in range(self.num_l3_sets)]  # Estructura del caché L1

        # Estructuras para LRU
        if repl_policy == 'l':
            self.lru_counters = [[] for _ in range(self.num_sets)]
            self.lru_counters_l2 = [[] for _ in range(self.num_l2_sets)]
            self.lru_counters_l3 = [[] for _ in range(self.num_l3_sets)]

    def print_info(self):
            print("Parámetros del caché:")
            print("\tCapacidad:\t\t\t" + str(self.cache_l1_capacity) + "kB")
            print("\tAssociatividad:\t\t\t" + str(self.cache_l1_assoc))
            print("\tTamaño de Bloque:\t\t\t" + str(self.block_size) + "B")
            print("\tPolítica de Reemplazo:\t\t\t" + str(self.repl_policy))

    def print_stats(self):
        print(f"Resultados de la simulación: {self.trace}")
        miss_rate = (100.0 * self.total_misses) / self.total_access
        miss_rate = "{:.3f}".format(miss_rate)
        result_str = str(self.total_misses) + "," + miss_rate + "%"
        print(result_str)

    def access(self, access_type, address):
        self.total_access += 1
        
        # L1
        set_index = (address // self.block_size) % self.num_sets
        tag = address // (self.block_size * self.num_sets)
        cache_set = self.cache[set_index]
        
        # L1
        set_index_l2 = (address // self.block_size) % self.num_l2_sets
        tag_l2 = address // (self.block_size * self.num_l2_sets)
        cache_set_l2 = self.cache_l2[set_index_l2]
        
        set_index_l3 = (address // self.block_size) % self.num_l3_sets
        tag_l3 = address // (self.block_size * self.num_l3_sets)
        cache_set_l3 = self.cache_l3[set_index_l3]

        # Check L1 cache
        if tag in cache_set:
            if self.repl_policy == 'l':
                self.lru_counters[set_index].remove(tag)
                self.lru_counters[set_index].append(tag)
            return "L1 hit"
        
        # Check L2 cache
        if tag_l2 in cache_set_l2:
            if self.repl_policy == 'l':
                self.lru_counters_l2[set_index_l2].remove(tag_l2)
                self.lru_counters_l2[set_index_l2].append(tag_l2)
            self._add_to_cache(self.cache, set_index, tag, self.cache_l1_assoc, self.lru_counters)
            return "L2 hit"
        
        # Check L3 cache
        if tag_l3 in cache_set_l3:
            if self.repl_policy == 'l':
                self.lru_counters_l3[set_index_l3].remove(tag_l3)
                self.lru_counters_l3[set_index_l3].append(tag_l3)
            self._add_to_cache(self.cache_l2, set_index_l2, tag_l2, self.cache_l2_assoc, self.lru_counters_l2)
            self._add_to_cache(self.cache, set_index, tag, self.cache_l1_assoc, self.lru_counters)
            return "L3 hit"
        
        # Miss
        self.total_misses += 1
        self._add_to_cache(self.cache_l3, set_index_l3, tag_l3, self.cache_l3_assoc, self.lru_counters_l3)
        self._add_to_cache(self.cache_l2, set_index_l2, tag_l2, self.cache_l2_assoc, self.lru_counters_l2)
        self._add_to_cache(self.cache, set_index, tag, self.cache_l1_assoc, self.lru_counters)
        return "Miss"

    def _add_to_cache(self, cache, set_index, tag, assoc, lru_counters):
            cache_set = cache[set_index]
            if len(cache_set) < assoc:
                cache_set.append(tag)
                if self.repl_policy == 'l':
                    lru_counters[set_index].append(tag)
            else:
                if self.repl_policy == 'l':
                    evict = lru_counters[set_index].pop(0)
                    cache_set.remove(evict)
                elif self.repl_policy == 'r':
                    evict = random.choice(cache_set)
                    cache_set.remove(evict)
                cache_set.append(tag)
                if self.repl_policy == 'l':
                    lru_counters[set_index].append(tag)