
Build image:
```bash
docker build -t <image-name>:<tag> .
```

Run container. It will try to execute `main.py` script by default.
```bash
docker run --rm -v $(pwd):/app <image-name>:<tag>
```

To run different command (e.g. check python version), simply add it at the end:
```bash
docker run --rm -v $(pwd):/app <image-name>:<tag> python --version
```

Webserver port binding:
```bash
docker run --rm -v $(pwd):/app -p 127.0.0.1:8888:80 <image-name>:<tag>
```
