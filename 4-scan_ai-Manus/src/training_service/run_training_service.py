"""
Training Service Entrypoint (run_training_service.py)

Runs on the Windows GPU node inside a Docker container.
Connects to RabbitMQ, consumes training jobs, executes training using GPU,
and publishes results back to RabbitMQ.
"""

import os
import sys
import logging
import time
import traceback

import torch
import torchvision
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image

# Add core utils path to sys.path to import RabbitMQClient
# Adjust the path depth as necessary based on the actual file structure
core_utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../core/utils"))
if core_utils_path not in sys.path:
    sys.path.append(core_utils_path)

try:
    from rabbitmq_client import RabbitMQClient
except ImportError:
    logging.error("Failed to import RabbitMQClient. Ensure rabbitmq_client.py is in the correct path.")

    # Define a dummy class if import fails to avoid crashing the service
    class RabbitMQClient:
        """Dummy RabbitMQ client for fallback when import fails."""

        def __init__(self, *_args, **_kwargs):
            """Initialize dummy client."""
            logging.error("Using dummy RabbitMQClient due to import failure.")

        def publish_message(self, *_args, **_kwargs):
            """Dummy publish method."""
            logging.error("Dummy publish_message called.")
            return False

        def start_consuming(self, *_args, **_kwargs):
            """Dummy consume method."""
            logging.error("Dummy start_consuming called.")

        def close(self):
            """Dummy close method."""
            logging.error("Dummy close called.")


# --- Configuration & Globals ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

rabbit_host = os.getenv("RABBITMQ_HOST")  # Must be provided via env var
rabbit_port = int(os.getenv("RABBITMQ_PORT", "5672"))
rabbit_user = os.getenv("RABBITMQ_USER", "rabbit_user")
rabbit_pass = os.getenv("RABBITMQ_PASS", "rabbit_password")

TRAINING_JOB_QUEUE = "training_jobs"
TRAINING_RESULT_QUEUE = "training_results"

# RabbitMQ client (initialized in main)
rabbit_client = None

# Shared storage paths (should match mounts in docker run)
DATASETS_BASE_PATH = os.getenv("SHARED_DATASETS_PATH", "/mnt/shared_storage/datasets")
MODELS_BASE_PATH = os.getenv("SHARED_MODELS_PATH", "/mnt/shared_storage/models")
LOGS_BASE_PATH = os.getenv("SHARED_LOGS_PATH", "/mnt/shared_storage/logs")


# --- Dummy Dataset Class (Replace with actual data loading) ---
class DummyImageDataset(Dataset):
    """Placeholder for actual dataset loading logic."""

    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        # Simulate finding image files and labels
        self.samples = []
        if os.path.exists(root_dir):
            # Example: find images in subfolders named by class
            for class_name in os.listdir(root_dir):
                class_dir = os.path.join(root_dir, class_name)
                if os.path.isdir(class_dir):
                    for img_name in os.listdir(class_dir):
                        if img_name.lower().endswith((".png", ".jpg", ".jpeg")):
                            self.samples.append((os.path.join(class_dir, img_name), class_name))
        else:
            logging.warning("Dataset directory not found: %s", root_dir)

        self.classes = sorted(list(set(s[1] for s in self.samples)))
        self.class_to_idx = {cls: i for i, cls in enumerate(self.classes)}
        logging.info("Found %d images in %d classes.", len(self.samples), len(self.classes))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, class_name = self.samples[idx]
        try:
            image = Image.open(img_path).convert("RGB")
            label = self.class_to_idx[class_name]
            if self.transform:
                image = self.transform(image)
            return image, label
        except (IOError, OSError, ValueError) as e:
            logging.error("Error loading image %s: %s", img_path, e)
            # Return a dummy item or raise error
            return torch.zeros((3, 224, 224)), -1  # Example dummy


# --- Training Logic ---
# pylint: disable=too-many-arguments,too-many-locals,too-many-statements,too-many-positional-arguments
def train_model(job_id, model_type, dataset_path, output_model_dir, epochs, learning_rate):
    """Executes the model training process."""
    logging.info("Starting training for job %s...", job_id)
    start_time = time.time()

    # Setup logging to file for this job
    log_dir = os.path.join(LOGS_BASE_PATH, job_id)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "training.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(file_handler)

    try:
        # 1. Check GPU availability
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA (GPU) not available on this node.")
        device = torch.device("cuda:0")
        logging.info("Using GPU: %s", torch.cuda.get_device_name(0))

        # 2. Prepare Dataset
        logging.info("Loading dataset from: %s", dataset_path)
        # Define transforms (adjust as needed)
        transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )
        # Replace DummyImageDataset with your actual dataset loading logic
        # dataset = torchvision.datasets.ImageFolder(root=dataset_path, transform=transform)
        dataset = DummyImageDataset(root_dir=dataset_path, transform=transform)
        if len(dataset) == 0:
            raise ValueError(f"No data found in dataset path: {dataset_path}")
        num_classes = len(dataset.classes)
        if num_classes == 0:
            raise ValueError("No classes found in the dataset.")
        logging.info("Dataset loaded: %d samples, %d classes.", len(dataset), num_classes)
        # Adjust batch_size/num_workers as needed
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=2)

        # 3. Load Model
        logging.info("Loading model: %s", model_type)
        if model_type == "resnet50":
            model = torchvision.models.resnet50(pretrained=True)
            num_ftrs = model.fc.in_features
            model.fc = nn.Linear(num_ftrs, num_classes)  # Adjust final layer
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        model = model.to(device)

        # 4. Define Loss and Optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        # 5. Training Loop
        logging.info("Starting training for %d epochs...", epochs)
        for epoch in range(epochs):
            model.train()
            running_loss = 0.0
            processed_samples = 0
            for i, (inputs, labels) in enumerate(dataloader):
                # Skip dummy items if any
                if torch.all(labels == -1):
                    logging.warning("Skipping batch with dummy data.")
                    continue

                inputs, labels = inputs.to(device), labels.to(device)

                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                processed_samples += inputs.size(0)

                if (i + 1) % 50 == 0:  # Log every 50 batches
                    logging.info(
                        "Epoch [%d/%d], Batch [%d/%d], Loss: %.4f",
                        epoch + 1, epochs, i + 1, len(dataloader), loss.item()
                    )

            epoch_loss = running_loss / processed_samples if processed_samples > 0 else 0
            logging.info("Epoch [%d/%d] completed. Loss: %.4f", epoch + 1, epochs, epoch_loss)
            # Add validation loop here if needed

        # 6. Save Model
        os.makedirs(output_model_dir, exist_ok=True)
        model_save_path = os.path.join(output_model_dir, "final_model.pth")
        torch.save(model.state_dict(), model_save_path)
        logging.info("Training complete. Model saved to: %s", model_save_path)

        end_time = time.time()
        duration = end_time - start_time
        logging.info("Training duration: %.2f seconds", duration)
        logging.getLogger().removeHandler(file_handler)
        file_handler.close()

        return True, "Training completed successfully.", model_save_path, log_file

    except (RuntimeError, ValueError, OSError) as e:
        error_msg = f"Training failed for job {job_id}: {traceback.format_exc()}"
        logging.error(error_msg)
        end_time = time.time()
        duration = end_time - start_time
        logging.info("Training duration before failure: %.2f seconds", duration)
        logging.getLogger().removeHandler(file_handler)
        file_handler.close()
        # Attempt to write error to log file one last time
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write("\n--- TRAINING FAILED ---\n")
                f.write(error_msg)
        except (IOError, OSError) as log_err:
            logging.error("Could not write final error to log file: %s", log_err)

        return False, str(e), None, log_file


# --- RabbitMQ Message Handling ---
def handle_training_job(message_data: dict) -> bool:
    """Callback function to process messages from the training_jobs queue."""
    job_id = message_data.get("job_id")
    logging.info("Received training job: %s", job_id)

    if not job_id:
        logging.error("Received job message without job_id. Discarding.")
        return True  # Acknowledge to remove invalid message

    try:
        # Extract job parameters
        model_type = message_data.get("model_type", "resnet50")
        dataset_path = message_data.get("dataset_path")
        output_model_dir = message_data.get("output_model_dir")
        epochs = int(message_data.get("epochs", 10))
        learning_rate = float(message_data.get("learning_rate", 0.001))

        if not dataset_path or not output_model_dir:
            raise ValueError("Missing dataset_path or output_model_dir in job message.")

        # Execute training
        success, details, model_path, log_path = train_model(
            job_id, model_type, dataset_path, output_model_dir, epochs, learning_rate
        )

        # Prepare result message
        result_message = {
            "job_id": job_id,
            "status": "COMPLETED" if success else "FAILED",
            "details": details,
            "model_path": model_path,  # Path relative to shared storage base
            "log_path": log_path,  # Path relative to shared storage base
        }

    except (ValueError, TypeError, KeyError) as e:
        error_msg = f"Error processing job {job_id}: {traceback.format_exc()}"
        logging.error(error_msg)
        result_message = {
            "job_id": job_id,
            "status": "FAILED",
            "details": str(e),
            "model_path": None,
            "log_path": None,
        }

    # Publish result back to RabbitMQ
    logging.info("Publishing result for job %s: %s", job_id, result_message["status"])
    publish_success = rabbit_client.publish_message(TRAINING_RESULT_QUEUE, result_message)

    if not publish_success:
        logging.error(
            "Failed to publish result for job %s. Manual intervention may be required.", job_id
        )
        # Decide if the original message should be ACKed or NACKed if publishing fails.
        # For now, we ACK to avoid reprocessing the job, but log the failure.
        return True

    return True  # Acknowledge original job message after processing


# --- Main Execution ---
if __name__ == "__main__":
    logging.info("Starting Training Service...")

    if not rabbit_host:
        logging.error("RABBITMQ_HOST environment variable not set. Exiting.")
        sys.exit(1)

    # Initialize RabbitMQ Client
    rabbit_client = RabbitMQClient(rabbit_host, rabbit_port, rabbit_user, rabbit_pass)

    # Start consuming training jobs
    # The client handles running this in a background thread and reconnecting
    rabbit_client.start_consuming(TRAINING_JOB_QUEUE, handle_training_job)

    logging.info("Training Service is running and waiting for jobs...")

    # Keep the main thread alive
    try:
        while True:
            time.sleep(60)  # Add health checks or other periodic tasks if needed
    except KeyboardInterrupt:
        logging.info("Shutting down Training Service...")
        rabbit_client.close()
        logging.info("Shutdown complete.")
