pid=$(pgrep -f main.py)
if [[ -n $pid ]]; then
    kill -9 "$pid"
    echo kill process [$pid]
fi

nohup python3 main.py 2>&1 &
sleep 1
if pgrep -a -f main.py; then
    echo server start success
fi


