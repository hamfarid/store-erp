"""
FILE: ml_service/train_disease_model.py | PURPOSE: YOLO model training
OWNER: ML Team | RELATED: yolo_detector.py | LAST-AUDITED: 2026-01-31

Train YOLOv8 model for plant disease detection.

Usage:
    python train_disease_model.py --data dataset/data.yaml --epochs 100
"""

import argparse
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CLASS_NAMES = [
    "healthy_leaf", "bacterial_spot", "early_blight", "late_blight",
    "leaf_mold", "septoria_leaf_spot", "spider_mites", "target_spot",
    "yellow_leaf_curl", "mosaic_virus"
]


def create_dataset_yaml(dataset_dir: Path, class_names: list = None) -> Path:
    """Create YOLO dataset configuration file."""
    yaml_path = dataset_dir / "data.yaml"
    names = class_names or CLASS_NAMES
    content = f"""path: {dataset_dir.absolute()}
train: images/train
val: images/val
nc: {len(names)}
names: {names}
"""
    with open(yaml_path, 'w') as f:
        f.write(content)
    return yaml_path


def prepare_dataset_structure(base_dir: Path) -> dict:
    """Create YOLO-compatible directory structure."""
    dirs = {
        'train_images': base_dir / 'images' / 'train',
        'val_images': base_dir / 'images' / 'val',
        'train_labels': base_dir / 'labels' / 'train',
        'val_labels': base_dir / 'labels' / 'val',
    }
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    return dirs


def train_model(data_yaml: str, epochs: int = 100, batch_size: int = 16,
                img_size: int = 640, model_name: str = "yolov8n.pt",
                output_dir: str = "runs/train", device: str = "auto") -> Optional[str]:
    """Train YOLO model for plant disease detection."""
    try:
        from ultralytics import YOLO
        logger.info(f"Loading base model: {model_name}")
        model = YOLO(model_name)
        logger.info(f"Training: {epochs} epochs, batch {batch_size}")
        
        results = model.train(
            data=data_yaml, epochs=epochs, batch=batch_size, imgsz=img_size,
            project=output_dir,
            name=f"disease_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            device=device, patience=50, save=True, plots=True, pretrained=True,
            lr0=0.01, momentum=0.937, weight_decay=0.0005,
            hsv_h=0.015, hsv_s=0.7, hsv_v=0.4,
            translate=0.1, scale=0.5, fliplr=0.5, mosaic=1.0,
        )
        
        best_path = Path(output_dir) / results.save_dir.name / "weights" / "best.pt"
        if best_path.exists():
            logger.info(f"Training complete! Model: {best_path}")
            return str(best_path)
        return None
    except ImportError:
        logger.error("ultralytics not installed. Run: pip install ultralytics")
        return None
    except Exception as e:
        logger.error(f"Training failed: {e}")
        return None


def deploy_model(model_path: str, models_dir: str = "models") -> bool:
    """Copy trained model to production."""
    try:
        dest = Path(models_dir)
        dest.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        target = dest / f"disease_model_{timestamp}.pt"
        shutil.copy2(model_path, target)
        latest = dest / "disease_model_latest.pt"
        if latest.exists():
            latest.unlink()
        shutil.copy2(model_path, latest)
        logger.info(f"Deployed to: {target}")
        return True
    except Exception as e:
        logger.error(f"Deploy failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Train YOLO for plant disease')
    parser.add_argument('--data', type=str, required=True, help='Dataset YAML')
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--batch', type=int, default=16)
    parser.add_argument('--img-size', type=int, default=640)
    parser.add_argument('--model', type=str, default='yolov8n.pt')
    parser.add_argument('--output', type=str, default='runs/train')
    parser.add_argument('--device', type=str, default='auto')
    parser.add_argument('--deploy', action='store_true')
    args = parser.parse_args()
    
    if not Path(args.data).exists():
        logger.error(f"Dataset not found: {args.data}")
        return 1
    
    best = train_model(args.data, args.epochs, args.batch, args.img_size,
                       args.model, args.output, args.device)
    if best:
        if args.deploy:
            deploy_model(best)
        return 0
    return 1


if __name__ == "__main__":
    exit(main())
