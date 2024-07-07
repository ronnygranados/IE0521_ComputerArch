foreach ($f in Get-ChildItem "traces/*.gz") {
    python3 cache_sim.py -s 128 -a 16 -b 64 -r l -t $f.FullName
}
