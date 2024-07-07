from optparse import OptionParser
import gzip
from cache import *

parser = OptionParser()
parser.add_option("-s", dest="cache_capacity")
parser.add_option("-a", dest="cache_assoc")
parser.add_option("-b", dest="block_size")
parser.add_option("-r", dest="repl_policy")
parser.add_option("-t", dest="TRACE_FILE")

(options, args) = parser.parse_args()

cache = cache(options.cache_capacity, options.cache_assoc, options.block_size, options.repl_policy)

# print(options.TRACE_FILE)

if options.TRACE_FILE:
    print(f"TRACE_FILE: {options.TRACE_FILE}")
else:
    print("No se pudo abrir el archivo")


# # i = 0 #SOLO PARA DEBUG
# with gzip.open(options.TRACE_FILE,'rt') as trace_fh:
#     for line in trace_fh:
#         line = line.rstrip()
#         access_type, hex_str_address  = line.split(" ")
#         address = int(hex_str_address, 16)
#         cache.access(access_type, address)

# cache.print_stats()
