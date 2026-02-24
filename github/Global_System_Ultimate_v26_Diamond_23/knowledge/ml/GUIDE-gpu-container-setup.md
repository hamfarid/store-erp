# GUIDE-gpu-container-setup.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. Prerequisites
*   **Host OS:** Ubuntu 22.04 LTS (Recommended).
*   **NVIDIA Driver:** Version 550.54.14 (CUDA 12.4).
*   **Docker:** Version 25.0.3 (Engine).
*   **NVIDIA Container Toolkit:** Version 1.14.5.

## 2. Installation Steps
1.  **Install NVIDIA Driver:**
    ```bash
    sudo apt install nvidia-driver-550
    sudo reboot
    ```
2.  **Install Docker:**
    ```bash
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    ```
3.  **Install NVIDIA Container Toolkit:**
    ```bash
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
      sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
      sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    ```

## 3. Verification
*   **Run `nvidia-smi` inside container:**
    ```bash
    docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
    ```
*   **Expected Output:** GPU details (Name, Memory, Driver Version).

## 4. Docker Compose Configuration
```yaml
services:
  training:
    image: nvidia/cuda:12.4.0-cudnn9-devel-ubuntu22.04
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## 5. Troubleshooting
*   **Error:** `could not select device driver "" with capabilities: [[gpu]]`
    *   **Fix:** Reinstall NVIDIA Container Toolkit and restart Docker.
*   **Error:** `CUDA error: no kernel image is available`
    *   **Fix:** Mismatch between PyTorch CUDA version and installed driver. Check compatibility matrix.
