(trap 'kill 0' SIGINT; python3 bot_server.py && sleep 1000 & python3 main.py)

