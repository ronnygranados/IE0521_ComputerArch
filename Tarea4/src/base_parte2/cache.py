
from math import log2, floor
import random

class cache:
    def __init__(self, cache_l1_capacity, cache_l1_assoc,
                       block_size, trace, 
                       cache_l2_capacity=0, cache_l2_assoc=0,
                       cache_l3_capacity=0, cache_l3_assoc=0, repl_policy="l"):
        
        self.total_access = 0
        self.total_misses = 0
        
        # Parámetros de interés
        
        self.total_access_l1 = 0
        self.total_misses_l1 = 0
        
        self.total_access_l2 = 0
        self.total_misses_l2 = 0
        
        self.total_access_l3 = 0
        self.total_misses_l3 = 0
        
        self.trace = trace

        # Caché: L1
        self.cache_l1_capacity = int(cache_l1_capacity)  # en kB
        self.cache_l1_assoc = int(cache_l1_assoc)
        
        # Caché: L2
        # if int(cache_l2_capacity) == 0:
        self.cache_l2_capacity = int(cache_l2_capacity)  # en kB
        self.cache_l2_assoc = int(cache_l2_assoc)
        
        # Caché: L3
        # if int(cache_l3_capacity) == 0:]
        self.cache_l3_capacity = int(cache_l3_capacity)  # en kB
        self.cache_l3_assoc = int(cache_l3_assoc)
        
        self.block_size = int(block_size)  # en Bytes
        self.repl_policy = repl_policy

        # Calcular el número de sets
        self.num_sets = (self.cache_l1_capacity * 1024) // (self.cache_l1_assoc * self.block_size)
        
        if self.cache_l2_capacity != 0:
            self.num_l2_sets = (self.cache_l2_capacity * 1024) // (self.cache_l2_assoc * self.block_size)
            
            if self.cache_l3_capacity != 0:
                self.num_l3_sets = (self.cache_l3_capacity * 1024) // (self.cache_l3_assoc * self.block_size)
            else:
                self.num_l3_sets = 0
        else:
            self.num_l2_sets = 0
            self.num_l3_sets = 0

        self.cache = [[] for _ in range(self.num_sets)]  # Estructura del caché L1
        
        if self.num_l2_sets != 0:
            self.cache_l2 = [[] for _ in range(self.num_l2_sets)]  # Estructura del caché L1
            if self.num_l3_sets != 0:
                self.cache_l3 = [[] for _ in range(self.num_l3_sets)]  # Estructura del caché L1
            else:
                self.cache_l3 = None
        else:
            self.cache_l2 = None
            self.cache_l3 = None
            
            
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
        
        if self.total_access_l1 != 0:
            miss_rate_l1 = (100.0 * self.total_misses_l1) / self.total_access_l1
            miss_rate_l1_p = "{:.3f}".format(miss_rate_l1)
        else:
            miss_rate_l1 = 0
            
        if self.total_access_l2 != 0:
            miss_rate_l2 = (100.0 * self.total_misses_l2) / self.total_access_l2
            miss_rate_l2_p = "{:.3f}".format(miss_rate_l2)
        else:
            miss_rate_l2 = 0
        
        if self.total_access_l3 != 0:
            miss_rate_l3 = (100.0 * self.total_misses_l3) / self.total_access_l3
            miss_rate_l3_p = "{:.3f}".format(miss_rate_l3)
        else:
            miss_rate_l3 = 0
            
        amat_3_levels = 4 + (miss_rate_l1/100)*(12 + (miss_rate_l2/100)*(60 + (miss_rate_l3/100) * 500))
        amat_3_levels_formatted = "{:.3f}".format(amat_3_levels)
        
        print(f"Miss rate L1: {miss_rate_l1_p} %")
        print(f"Miss rate L2: {miss_rate_l2_p} %")
        print(f"Miss rate L3: {miss_rate_l3_p} %") 
        print(f"AMAT: {amat_3_levels_formatted}")
        print()

    def access(self, access_type, address):
        self.total_access_l1 += 1

        # L1
        set_index = (address // self.block_size) % self.num_sets
        tag = address // (self.block_size * self.num_sets)
        cache_set = self.cache[set_index]

        # Check L1 cache
        if tag in cache_set:
            if self.repl_policy == 'l':
                self.lru_counters[set_index].remove(tag)
                self.lru_counters[set_index].append(tag)
            return "L1 hit"

        # L1 miss
        self.total_misses_l1 += 1

        if self.cache_l2_capacity > 0:
            # L2
            self.total_access_l2 += 1
            set_index_l2 = (address // self.block_size) % self.num_l2_sets
            tag_l2 = address // (self.block_size * self.num_l2_sets)
            cache_set_l2 = self.cache_l2[set_index_l2]

            # Check L2 cache
            if tag_l2 in cache_set_l2:
                if self.repl_policy == 'l':
                    self.lru_counters_l2[set_index_l2].remove(tag_l2)
                    self.lru_counters_l2[set_index_l2].append(tag_l2)
                self._add_to_cache(self.cache, set_index, tag, self.cache_l1_assoc, self.lru_counters)
                return "L2 hit"

            # L2 miss
            self.total_misses_l2 += 1

            if self.cache_l3_capacity > 0:
                # L3
                self.total_access_l3 += 1
                set_index_l3 = (address // self.block_size) % self.num_l3_sets
                tag_l3 = address // (self.block_size * self.num_l3_sets)
                cache_set_l3 = self.cache_l3[set_index_l3]

                # Check L3 cache
                if tag_l3 in cache_set_l3:
                    if self.repl_policy == 'l':
                        self.lru_counters_l3[set_index_l3].remove(tag_l3)
                        self.lru_counters_l3[set_index_l3].append(tag_l3)
                    self._add_to_cache(self.cache_l2, set_index_l2, tag_l2, self.cache_l2_assoc, self.lru_counters_l2)
                    self._add_to_cache(self.cache, set_index, tag, self.cache_l1_assoc, self.lru_counters)
                    return "L3 hit"

                # L3 miss
                self.total_misses_l3 += 1

                # Fetch from memory and update all caches
                self._add_to_cache(self.cache_l3, set_index_l3, tag_l3, self.cache_l3_assoc, self.lru_counters_l3)
                self._add_to_cache(self.cache_l2, set_index_l2, tag_l2, self.cache_l2_assoc, self.lru_counters_l2)
            else:
                # Fetch from memory and update L1 and L2 caches
                self._add_to_cache(self.cache_l2, set_index_l2, tag_l2, self.cache_l2_assoc, self.lru_counters_l2)

        # Fetch from memory and update L1 cache
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