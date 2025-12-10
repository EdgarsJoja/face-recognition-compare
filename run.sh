# xhost +local:docker

# docker run --rm -it --device /dev/video0:/dev/video0 -v $(pwd):/app -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY elza-python:1 python main.py

# docker run --rm -it -v $(pwd):/app -e DISPLAY=$DISPLAY elza-python:1

docker run --rm -v $(pwd):/app -p 127.0.0.1:80:80 elza-python:1 python webserver.py
