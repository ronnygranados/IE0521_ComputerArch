from optparse import OptionParser
import gzip
import sys
from cache import *

parser = OptionParser()
parser.add_option("--l1_s", dest="l1_s") # Capacidad de caché L1
parser.add_option("--l1_a", dest="l1_a") # Asociatividad d ecaché L1
parser.add_option("--l2", action="store_true", dest="has_l2") # Existencia de L2
parser.add_option("--l2_s", dest="l2_s") # Capacidad de caché L2
parser.add_option("--l2_a", dest="l2_a") # Asociatividad de caché L2
parser.add_option("--l3", action="store_true", dest="has_l3") # Existencia de L3
parser.add_option("--l3_s", dest="l3_s") # Capacidad de caché L3
parser.add_option("--l3_a", dest="l3_a") # Asociatividad de caché L3
parser.add_option("-b", dest="block_size", default="64") # Tamaño del bloque en bytes
parser.add_option("-t", dest="TRACE_FILE") # Trace file

(options, args) = parser.parse_args()

# if options.l3_s == None and options.l2_s == None:
#     l1_cache = cache(options.l1_s, options.l1_a, options.block_size, options.TRACE_FILE)

# elif options.l3_s == None and options.l2_s != None:
#     l1_cache = cache(options.l1_s, options.l1_a, options.l2_s, options.l2_a, options.block_size, options.TRACE_FILE)

# else:
#     l1_cache = cache(options.l1_s, options.l1_a, 
#                      options.block_size, options.TRACE_FILE,
#                      options.l2_s, options.l2_a,
#                      options.l3_s, options.l3_a)

# Caso: caché L3 sin caché L2
if options.has_l3 and not options.has_l2:
    raise Exception("No se puede inicializar el caché L3 sin la existencia del caché L2.")

# Casos
if not options.has_l3 and not options.has_l2:
    print("Caso 1")
    l1_cache = cache(options.l1_s, options.l1_a, options.block_size, options.TRACE_FILE)
elif not options.has_l3 and options.has_l2:
    print("Caso 2")
    l1_cache = cache(options.l1_s, options.l1_a, options.block_size, options.TRACE_FILE, options.l2_s, options.l2_a)
else:
    print("Caso 3")
    l1_cache = cache(options.l1_s, options.l1_a, 
                     options.block_size, options.TRACE_FILE,
                     options.l2_s, options.l2_a,
                     options.l3_s, options.l3_a)


with gzip.open(options.TRACE_FILE,'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        access_type, hex_str_address  = line.split(" ")
        address = int(hex_str_address, 16)
        l1_cache.access(access_type, address)
l1_cache.print_stats()