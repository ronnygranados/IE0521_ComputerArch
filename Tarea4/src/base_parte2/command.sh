for i in traces/*; do
    # Caso: L3 de 512 kB y 16-ways
    python3 cache_simm.py --l1_s 32 --l1_a 8 -b 64 -t "$i" --l2 --l2_s 256 --l2_a 8 --l3 --l3_s 1024 --l3_a 32
done
