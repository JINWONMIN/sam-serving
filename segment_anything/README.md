## Building the container for creating the .mar archives
Both models will be downloaded using the vit_h weights.
```bash
docker build -t sam-builder -f Dockerfile-build .
```

<br>

## Copying the .mar archives to host for local testing
```bash
docker run -d --name sam-builder1 sam-builder
docker cp sam-builder1:/home/model-store ./
```
Copy these to model-store and use this locally by both the GPU and the CPU Torchserve containers. <br>
Delete the container once models are copied

```bash
docker rm -f sam-builder1
```

<br>

## Building the gpu torchserve container for image encoding
With the GPU, inference time should be about 1.8 seconds or less depending on the GPU. On an RTX 3090 GPU, inference time is `445 ms` without compilation.
```bash
docker build -t sam-gpu -f Dockerfile-gpu .
bash start_serve_encode_gpu.sh
```

<br>

Building the cpu torchserve container for image decoding
```bash
docker build -t sam-cpu -f Dockerfile-cpu .
bash start_serve_decode_cpu.sh
```

## Test the encode service on the GPU or CPU
The CPU service is served on 7080 by default. 8080 for the GPU service by default.
```bash
curl http://127.0.0.1:8080/predictions/sam_vit_h_encode -T ./coco.png
```