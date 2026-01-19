#!/bin/bash

# Script to initialize Docker Swarm and deploy the Gaara ERP stack
# Run this script on the designated Swarm Manager node (e.g., gaara - 100.78.19.7)

set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration ---
MANAGER_IP="100.78.19.7" # IP address of the manager node
WORKER_IPS=("100.109.208.97" "100.104.23.62") # IP addresses of the worker nodes
STACK_NAME="gaara_stack"
COMPOSE_FILE="docker-compose.swarm.yml"
SSH_USER="hady.m.farid" # SSH user for connecting to worker nodes
SHARED_STORAGE_SERVER="100.77.215.80"
SHARED_STORAGE_BASE_PATH="/path/to/shared" # Base path on the NFS server (e.g., /mnt/pool/shared)
MOUNT_POINT="/mnt/shared_storage" # Mount point on all Swarm nodes

# --- Helper Functions ---
echo_info() {
    echo "[INFO] $1"
}

echo_warn() {
    echo "[WARN] $1"
}

echo_error() {
    echo "[ERROR] $1" >&2
    exit 1
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo_error "Docker could not be found. Please install Docker."
    fi
    if ! docker info &> /dev/null; then
        echo_error "Docker daemon is not running or user doesn't have permission."
    fi
}

check_nfs_utils() {
    if ! command -v showmount &> /dev/null; then
        echo_warn "NFS utilities (nfs-common) not found. Attempting to install..."
        sudo apt-get update && sudo apt-get install -y nfs-common || echo_error "Failed to install nfs-common. Please install it manually."
    fi
}

mount_shared_storage() {
    echo_info "Checking and mounting shared storage (${SHARED_STORAGE_SERVER}:${SHARED_STORAGE_BASE_PATH}) on ${MOUNT_POINT}..."
    check_nfs_utils

    # Check if mount point exists, create if not
    if [ ! -d "${MOUNT_POINT}" ]; then
        echo_info "Creating mount point ${MOUNT_POINT}..."
        sudo mkdir -p "${MOUNT_POINT}" || echo_error "Failed to create mount point ${MOUNT_POINT}"
    fi

    # Check if already mounted
    if mount | grep -q "${MOUNT_POINT}"; then
        echo_info "Shared storage already mounted on ${MOUNT_POINT}."
    else
        echo_info "Attempting to mount NFS share..."
        # Create necessary subdirectories on the NFS server *before* mounting if they don't exist
        # This part should ideally be done once on the NFS server itself.
        # Example: ssh ${SSH_USER}@${SHARED_STORAGE_SERVER} "mkdir -p ${SHARED_STORAGE_BASE_PATH}/{db_data,rabbitmq_data,prometheus_data,grafana_data,logs,models,datasets}"

        sudo mount -t nfs "${SHARED_STORAGE_SERVER}:${SHARED_STORAGE_BASE_PATH}" "${MOUNT_POINT}" || echo_error "Failed to mount NFS share. Check NFS server, export path, and permissions."
        echo_info "NFS share mounted successfully."
        # Add to /etc/fstab for persistence (optional, requires careful checking)
        # echo "${SHARED_STORAGE_SERVER}:${SHARED_STORAGE_BASE_PATH} ${MOUNT_POINT} nfs defaults 0 0" | sudo tee -a /etc/fstab
    fi

    # Verify mount
    if ! mount | grep -q "${MOUNT_POINT}"; then
        echo_error "Mount verification failed for ${MOUNT_POINT}."
    fi

    # Ensure subdirectories exist on the mount point (needed for volume drivers)
    echo_info "Ensuring subdirectories exist on mount point..."
    sudo mkdir -p "${MOUNT_POINT}/db_data" "${MOUNT_POINT}/rabbitmq_data" "${MOUNT_POINT}/prometheus_data" "${MOUNT_POINT}/grafana_data" "${MOUNT_POINT}/logs" "${MOUNT_POINT}/models" "${MOUNT_POINT}/datasets"
    sudo chown -R $(id -u):$(id -g) "${MOUNT_POINT}" # Adjust ownership if needed
}

# --- Main Script ---

echo_info "Starting Docker Swarm setup..."
check_docker

# --- Mount Shared Storage on Manager ---
mount_shared_storage

# --- Initialize Swarm ---
if ! docker node ls &> /dev/null; then
    echo_info "Initializing Docker Swarm on manager node (${MANAGER_IP})..."
    docker swarm init --advertise-addr ${MANAGER_IP} || echo_error "Failed to initialize Swarm."
else
    echo_info "Docker Swarm already initialized."
fi

# --- Get Join Tokens ---
WORKER_TOKEN=$(docker swarm join-token worker -q)
MANAGER_TOKEN=$(docker swarm join-token manager -q)

if [ -z "${WORKER_TOKEN}" ]; then
    echo_error "Failed to retrieve worker join token."
fi

echo_info "Worker Join Token: ${WORKER_TOKEN}"
echo_info "Manager Join Token (for adding more managers): ${MANAGER_TOKEN}"

# --- Join Worker Nodes ---
JOIN_COMMAND="docker swarm join --token ${WORKER_TOKEN} ${MANAGER_IP}:2377"

for worker_ip in "${WORKER_IPS[@]}"; do
    echo_info "Attempting to join worker node ${worker_ip}..."
    # SSH into the worker node, mount storage, and execute the join command
    ssh -o StrictHostKeyChecking=no ${SSH_USER}@${worker_ip} "\
        echo '[INFO] Checking Docker on worker ${worker_ip}...'; \
        if ! command -v docker &> /dev/null; then echo '[ERROR] Docker not found on worker.'; exit 1; fi; \
        if ! docker info &> /dev/null; then echo '[ERROR] Docker daemon not running on worker.'; exit 1; fi; \
        echo '[INFO] Mounting shared storage on worker ${worker_ip}...'; \
        if ! command -v showmount &> /dev/null; then sudo apt-get update && sudo apt-get install -y nfs-common || exit 1; fi; \
        if [ ! -d \"${MOUNT_POINT}\" ]; then sudo mkdir -p \"${MOUNT_POINT}\" || exit 1; fi; \
        if ! mount | grep -q \"${MOUNT_POINT}\"; then sudo mount -t nfs \"${SHARED_STORAGE_SERVER}:${SHARED_STORAGE_BASE_PATH}\" \"${MOUNT_POINT}\" || exit 1; fi; \
        if ! mount | grep -q \"${MOUNT_POINT}\"; then echo '[ERROR] Mount verification failed on worker.'; exit 1; fi; \
        echo '[INFO] Leaving existing Swarm if necessary...'; \
        docker swarm leave --force || true; \
        echo '[INFO] Joining Swarm...'; \
        ${JOIN_COMMAND} \
    " || echo_warn "Failed to automatically join worker ${worker_ip}. Please join manually using the token."
    sleep 2
done

# --- Verify Nodes ---
echo_info "Current Swarm Nodes:"
docker node ls

# --- Deploy Stack ---
if [ -f "${COMPOSE_FILE}" ]; then
    echo_info "Deploying stack '${STACK_NAME}' from ${COMPOSE_FILE}..."
    # Note: Docker stack deploy uses the volume definitions from the compose file.
    # Ensure the volume driver options correctly point to your NFS setup.
    # You might need to pre-create the NFS export paths on the NFS server.
    docker stack deploy -c "${COMPOSE_FILE}" "${STACK_NAME}" || echo_error "Failed to deploy stack."
    echo_info "Stack deployment initiated. Services are starting..."
else
    echo_error "Compose file '${COMPOSE_FILE}' not found."
fi

# --- Show Service Status ---
sleep 10 # Give services some time to start
echo_info "Current Service Status:"
docker service ls

echo_info "Docker Swarm setup and stack deployment complete."
echo_info "Access RabbitMQ UI: http://${MANAGER_IP}:15672 (user: rabbit_user)"
echo_info "Access Prometheus: http://${MANAGER_IP}:9090"
echo_info "Access Grafana: http://${MANAGER_IP}:3000 (user: admin)"
echo_info "Access Web UI: http://${MANAGER_IP}:2050"
echo_info "Access API Server: http://${MANAGER_IP}:8000"
