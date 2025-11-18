xhost +local:docker

docker run --rm -it --device /dev/video0:/dev/video0 -v $(pwd):/app -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY elza-python:1 python main2.py
