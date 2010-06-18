for i in configs/*py ; do time ./check_neo.py --evolve 3000 --prerandomize 1000000 -v -q --controlled-tail --config $i >> $i-3000.txt & done

