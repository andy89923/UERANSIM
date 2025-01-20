#!/usr/bin/env bash
PID_LIST=()
sudo echo "run the UE..."
echo $$ > run.pid
#function terminate()
#{
#    exit 0
#}

echo "Start the test" > ue.log
echo "Start the test" > deregister.log

#trap terminate INT
for i in {1..400}
do
    echo "$i th test" >> ue.log
    sudo build/nr-ue -c config/free5gc-ue.yaml >> ue.log &

    PID1=($!)
    printf "execute $i time\r\n"
    printf "pid1: $PID1 \r\n"
    sleep 0.1s
    build/nr-cli imsi-208930000000001 -e "deregister switch-off" >> deregister.log &
    PID2=($!)
    printf "pid2: $PID2 \r\n"
    sudo kill -SIGTERM ${PID2}
    sudo kill -SIGTERM ${PID1}
    wait ${PID2}
    wait ${PID1}
    printf "done\r\n"
    #sleep 0.1s
done