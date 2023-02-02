#!/bin/bash

# CONST 1GB

CONST_1GB="1024*1024*1024"

# VARIABLE WORKERS

CMD_W=0

# VARIABLE MAX MEMORY PERCENT

CMD_M=80

# VARIABLE IS HELP

CMD_H=0

# VARIABLE IS VERBOSE

CMD_V=0

# FUNCTIONS

arithmetic() {
  echo "scale=0; $1" | bc
}

calculateWorkers(){
  if [ $CMD_W -gt 0 ]; then echo $CMD_W
  elif [ $(calculateMaxMemory) -le $(arithmetic "$CONST_1GB") ]; then echo 1 # 1GB
  elif [ $(calculateMaxMemory) -le $(arithmetic "2*$CONST_1GB") ]; then echo 2 # 2GB
  elif [ $(calculateMaxMemory) -le $(arithmetic "3*$CONST_1GB") ]; then echo 3 # 3GB
  else
    echo $(arithmetic "1+$(calculateNumCores)*2")
  fi
}

calculateMemTotal () {
  echo $(arithmetic "$(cat /proc/meminfo | grep MemTotal | awk '{ print $2 }')*1024")
}

calculateNumCores(){
  echo $(nproc)
}

calculateMaxMemory() {
  echo $(arithmetic "$(calculateMemTotal)*$CMD_M/100")
}

calculateLimitMemoryHard() {
  echo $(arithmetic "$(calculateMaxMemory)/$(calculateWorkers)")
}

calculateLimitMemorySoft() {
  echo $(arithmetic "$(calculateLimitMemoryHard)*80/100")
}

# COMMANDS

v() {
  echo
  echo "System Information"
  echo "------------------"
  echo "Cores (CORES):  $(calculateNumCores)"
  echo "Total Memory (TOTAL_M): $(calculateMemTotal) bytes"
  echo "Max Allowed Memory (ALLOW_M): $(calculateMaxMemory) bytes"
  echo "Max Allowed Memory Percent, default 80%: $CMD_M%"
  echo
  echo
  echo "Functions to calculate configutarion"
  echo "------------------------------------"
  echo "workers = if not used -w then"
  echo "               if ALLOW_M < 1GB then 1"
  echo "               else ALLOW_M < 2GB then 2"
  echo "               else ALLOW_M < 3GB then 3"
  echo "               else 1+CORES*2"
  echo "          else -w"
  echo "limit_memory_hard = ALLOW_M / workers"
  echo "limit_memory_soft = limit_memory_hard * 80%"
  echo "limit_request = DEFAULT 8192"
  echo "limit_time_cpu = DEFAULT 120"
  echo "limit_time_real = DEFAULT 180"
  echo "max_cron_threads = DEFAULT 2"
  echo
  echo
  echo "Add to the odoo-server.conf"
  echo "---------------------------"
  c
  echo
}

h() {
  echo "This file enables us to optimally configure multithreading settings Odoo"
  echo "   -h    Help"
  echo "   -m    Max memory percent to use"
  echo "   -v    Verbose"
  echo "   -w    Set static workers number"
}

c() {
  echo "workers = $(calculateWorkers)"
  echo "limit_memory_hard = $(calculateLimitMemoryHard)"
  echo "limit_memory_soft = $(calculateLimitMemorySoft)"
  echo "limit_request = 8192"
  echo "limit_time_cpu = 120"
  echo "limit_time_real = 180"
  echo "max_cron_threads = 2"
}

# PROCESS PARAMETERS
i=1
while ["$i" -le $# ]
do
  case "${!i}" in '-w') ((i++))
    CMD_W=${!i}
    ;;
    '-m') ((i++))
    if [ ${!i} -gt 0 ] && [ ${!i} -lt 80 ]; then CMD_M=${!i}
    fi
    ;;
    '-v')
    CMD_V=1
    ;;
    '-h')
    CMD_H=1
    ;;
    *)
    # NOTHING
    ;;
  esac
done

# EXEC ACTION

if [ $CMD_H -eq 1 ]; then h
elif [ $CMD_V -eq 1 ]; then v
else c
fi

exit 0
