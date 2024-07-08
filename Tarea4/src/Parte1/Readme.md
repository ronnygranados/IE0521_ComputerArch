# Cache Simulator

Este proyecto es una simulación de caché de un único nivel, implementado en Python, que permite analizar el efecto de varios parámetros de configuración del caché en la tasa de fallos (miss rate). Los parámetros incluyen tamaño del caché, asociatividad, tamaño de los bloques y políticas de reemplazo.

## Autores

- Lorena Solís Extteny B97657
- Ronny Granados Perez C03505

## Requisitos

- Python 3.x

## Uso

Para ejecutar la simulación, utilice el siguiente comando en la terminal:

```sh
for f in traces/*.gz; do python3 cache_sim.py -s <tamaño_cache> -a <asociatividad> -b <tamaño_bloques> -r <política_reemplazo> -t "$f"; done
for f in traces/*.gz; do python3 cache_sim.py -s 128 -a 16 -b 64 -r l -t "$f"; done
