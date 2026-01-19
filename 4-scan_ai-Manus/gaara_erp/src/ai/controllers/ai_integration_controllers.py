"""
AI Integration Controllers - Enhanced for Distributed Training

Handles API requests related to AI model training, diagnosis, etc.,
and coordinates with the Training Service via RabbitMQ.
"""

from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import uuid
import logging
import sys

# Add core utils path to sys.path to import RabbitMQClient
# Adjust the path depth as necessary based on the actual file structure
core_utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../core/utils"))
if core_utils_path not in sys.path:
    sys.path.append(core_utils_path)

try:
    from rabbitmq_client import RabbitMQClient
except ImportError:
    logging.error("Failed to import RabbitMQClient. Ensure rabbitmq_client.py is in the correct path.")
    # Define a dummy class if import fails to avoid crashing the server on startup
    class RabbitMQClient:
        def __init__(self, *args, **kwargs):
            logging.error("Using dummy RabbitMQClient due to import failure.")
        def publish_message(self, *args, **kwargs):
            logging.error("Dummy publish_message called.")
            return False
        def start_consuming(self, *args, **kwargs):
            logging.error("Dummy start_consuming called.")
        def close(self):
            logging.error("Dummy close called.")

# --- Configuration & Globals ---
logging.basicConfig(level=logging.INFO, format=	'%(asctime)s - %(levelname)s - %(message)s	')

rabbit_host = os.getenv("RABBITMQ_HOST", "message-queue") # Use service name within Swarm
rabbit_port = int(os.getenv("RABBITMQ_PORT", 5672))
rabbit_user = os.getenv("RABBITMQ_USER", "rabbit_user")
rabbit_pass = os.getenv("RABBITMQ_PASS", "rabbit_password")

TRAINING_JOB_QUEUE = "training_jobs"
TRAINING_RESULT_QUEUE = "training_results"

# Initialize RabbitMQ Client
rabbit_client = RabbitMQClient(rabbit_host, rabbit_port, rabbit_user, rabbit_pass)

# In-memory storage for job status (Replace with database interaction)
job_status_db = {}

router = APIRouter(
    prefix="/ai/integration",
    tags=["AI Integration"],
)

# --- Pydantic Models ---
class TrainingRequest(BaseModel):
    model_type: str = "resnet50"
    dataset_name: str
    epochs: int = 10
    learning_rate: float = 0.001
    # Add other relevant parameters

class TrainingJobStatus(BaseModel):
    job_id: str
    status: str
    details: str | None = None
    model_path: str | None = None

# --- Helper Functions ---
def update_job_status(job_id: str, status: str, details: str | None = None, model_path: str | None = None):
    """Updates the status of a training job (in memory for now)."""
    logging.info(f"Updating job 	{job_id}	 status to 	{status}	")
    job_status_db[job_id] = {
        "status": status,
        "details": details,
        "model_path": model_path
    }
    # TODO: Replace with actual database update logic

def handle_training_result(message_data: dict) -> bool:
    """Callback function to process messages from the training_results queue."""
    try:
        job_id = message_data.get("job_id")
        status = message_data.get("status")
        details = message_data.get("details")
        model_path = message_data.get("model_path")

        if not job_id or not status:
            logging.error(f"Received invalid result message: {message_data}")
            return True # Acknowledge invalid message to remove it

        logging.info(f"Received training result for job 	{job_id}	: Status=	{status}	")
        update_job_status(job_id, status, details, model_path)
        return True # Acknowledge successful processing

    except Exception as e:
        logging.error(f"Error processing training result message: {e}")
        return False # Do not acknowledge if error occurs during processing

# --- API Endpoints ---
@router.post("/train", response_model=TrainingJobStatus, status_code=202)
def submit_training_job(request: TrainingRequest, background_tasks: BackgroundTasks):
    """
    Submits a new AI model training job.
    Generates a job ID, saves initial status, and publishes the job to RabbitMQ.
    """
    job_id = str(uuid.uuid4())
    logging.info(f"Received training request: {request.dict()}, assigned Job ID: {job_id}")

    # Define the job message
    job_message = {
        "job_id": job_id,
        "model_type": request.model_type,
        "dataset_name": request.dataset_name,
        "epochs": request.epochs,
        "learning_rate": request.learning_rate,
        # Construct paths based on shared storage mount point inside API container
        "dataset_path": os.path.join(os.getenv("SHARED_DATASETS_PATH", "/mnt/shared_storage/datasets"), request.dataset_name),
        "output_model_dir": os.path.join(os.getenv("SHARED_MODELS_PATH", "/mnt/shared_storage/models"), job_id)
    }

    # Save initial job status (e.g., "PENDING")
    update_job_status(job_id, "PENDING", "Job submitted to queue.")

    # Publish job to RabbitMQ
    success = rabbit_client.publish_message(TRAINING_JOB_QUEUE, job_message)

    if not success:
        update_job_status(job_id, "FAILED", "Failed to publish job to queue.")
        raise HTTPException(status_code=500, detail="Failed to publish training job to queue.")

    logging.info(f"Training job 	{job_id}	 published successfully to queue 	{TRAINING_JOB_QUEUE}	.")

    return TrainingJobStatus(job_id=job_id, status="PENDING", details="Job submitted to queue.")

@router.get("/train/{job_id}", response_model=TrainingJobStatus)
def get_training_job_status(job_id: str):
    """
    Retrieves the status of a specific training job.
    """
    status_info = job_status_db.get(job_id)
    if not status_info:
        raise HTTPException(status_code=404, detail="Training job not found.")

    return TrainingJobStatus(job_id=job_id, **status_info)

# --- Background Task for Consuming Results ---
def start_results_consumer():
    """Starts the RabbitMQ consumer for training results."""
    logging.info("Starting RabbitMQ consumer for training results...")
    rabbit_client.start_consuming(TRAINING_RESULT_QUEUE, handle_training_result)

# --- Event Handlers for FastAPI App Startup/Shutdown (if using FastAPI directly) ---
# If integrating into an existing FastAPI app, add these handlers

# @router.on_event("startup")
# async def startup_event():
#     start_results_consumer()

# @router.on_event("shutdown")
# async def shutdown_event():
#     rabbit_client.close()

# --- Initialization (if running this file directly or called from main app) ---
# Ensure the consumer starts when the application initializes.
# This might need adjustment depending on how the FastAPI app is structured.
# For simplicity, we call it here, but in a real app, use startup events.
start_results_consumer()

# Example of how to include this router in a main FastAPI app:
# from fastapi import FastAPI
# app = FastAPI()
# app.include_router(router)

# @app.on_event("shutdown")
# async def shutdown_event():
#     rabbit_client.close()

