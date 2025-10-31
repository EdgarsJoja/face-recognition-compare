
Build image:
```bash
docker build -t <image-name>:<tag> .
```

Run container. It will try to execute `main.py` script by default.
```bash
docker run -v $(pwd):/app <image-name>:<tag>
```

To run different command (e.g. check python version), simply add it at the end:
```bash
docker run -v $(pwd):/app <image-name>:<tag> python --version
```
