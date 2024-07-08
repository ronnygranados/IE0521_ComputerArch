for i in traces/*; do
    # python3 cache_simm.py --l1_s 128 --l1_a 16 -b 64 -t "$i"
    python3 cache_simm.py --l1_s 32 --l1_a 8 --l2 --l3 --l2_s 256 --l2_a 8 --l3_s 512 --l3_a 16 -b 64 -t "$i"
done
