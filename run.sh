#!/usr/bin/env bash

sudo -v

PID_LIST+=()


function terminate() { 
    sudo kill ${PID_LIST}
    exit 0
}

trap terminate SIGINT

./build/nr-gnb -c config/free5gc-gnb.yaml &
PID=$!
PID_LIST+=($PID)

sleep 1

sudo ./build/nr-ue -c config/free5gc-ue.yaml  &
PID=$!
PID_LIST+=($PID)

sleep 1

wait ${PID_LIST}
