if ! pgrep -f main.py >/dev/null; then
    echo "server process is not exist, auto restart!" >> /data/get_xq_data/call.log
    # 在这里添加重启服务器的命令
    cd /data/get_xq_data; sh restart.sh; 
fi