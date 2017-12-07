SCRHOME=/home/boltzmann/Development/GH_cloning_stats
PYHOME=/home/boltzmann/apps/anaconda/bin
export GH_CLONE_TOKEN=4cf9a1e77ea580a58a8bab3c896a918a28b75b00
${PYHOME}/python $SCRHOME/pull_stats.py -gu westpa -gr westpa -pu ASinanSaglam -pt -o ${SCRHOME}/ghstats.pickle
${PYHOME}/python $SCRHOME/print_stats.py -i ${SCRHOME}/ghstats.pickle > $SCRHOME/dl_stats.txt
scp $SCRHOME/dl_stats.txt ali@chongweb.chem.pitt.edu:~/.
