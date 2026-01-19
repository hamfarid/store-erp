#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for advanced image data augmentation techniques.

This module expands on basic augmentation by adding more sophisticated methods
like CutMix, Mixup, and advanced color/geometric transformations, often used
to improve model robustness and generalization in computer vision tasks.
"""

import cv2
import numpy as np
import random

# --- Configuration ---
DEFAULT_AUGMENTATION_CONFIG = {
    "brightness_contrast": {"alpha_range": (0.8, 1.2), "beta_range": (-20, 20), "p": 0.5},
    "hsv_jitter": {"hue_delta": 10, "sat_delta": 30, "val_delta": 30, "p": 0.5},
    "blur": {"kernel_size_range": (3, 7), "p": 0.3},
    "noise": {"mean": 0, "std_dev_range": (5, 20), "p": 0.3},
    "cutout": {"num_holes": 1, "max_h_size": 40, "max_w_size": 40, "fill_value": 0, "p": 0.4},
    "cutmix": {"alpha": 1.0, "p": 0.3}, # Probability applied per batch if used in batch context
    "mixup": {"alpha": 0.4, "p": 0.3},   # Probability applied per batch if used in batch context
    "rotate": {"angle_range": (-15, 15), "p": 0.5},
    "scale": {"scale_range": (0.9, 1.1), "p": 0.5},
    "translate": {"translate_fraction": 0.1, "p": 0.3},
    "shear": {"shear_range": (-10, 10), "p": 0.3},
    "flip_lr": {"p": 0.5},
    "flip_ud": {"p": 0.1} # Usually less common for plants unless orientation invariant
}

# --- Basic Augmentations (Refined) ---

def apply_brightness_contrast(image, alpha_range=(0.8, 1.2), beta_range=(-20, 20)):
    """Applies random brightness and contrast adjustment."""
    alpha = random.uniform(alpha_range[0], alpha_range[1])
    beta = random.uniform(beta_range[0], beta_range[1])
    # Apply alpha (contrast) and beta (brightness)
    # new_image = alpha * image + beta
    # Ensure the result is clipped to [0, 255]
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

def apply_hsv_jitter(image, hue_delta=10, sat_delta=30, val_delta=30):
    """Applies random jitter to Hue, Saturation, and Value channels."""
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)

    hue_shift = random.uniform(-hue_delta, hue_delta)
    sat_shift = random.uniform(1 - sat_delta/100.0, 1 + sat_delta/100.0)
    val_shift = random.uniform(1 - val_delta/100.0, 1 + val_delta/100.0)

    # Apply shifts, handling hue wrap-around and saturation/value clipping
    h = cv2.add(h, hue_shift)
    # h = np.mod(h + hue_shift, 180) # Hue is 0-179 in OpenCV
    s = np.clip(s * sat_shift, 0, 255)
    v = np.clip(v * val_shift, 0, 255)

    final_hsv = cv2.merge((h, s.astype(np.uint8), v.astype(np.uint8)))
    jittered_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return jittered_image

def apply_blur(image, kernel_size_range=(3, 7)):
    """Applies Gaussian blur with a random kernel size."""
    ksize = random.randrange(kernel_size_range[0], kernel_size_range[1] + 1, 2) # Must be odd
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def add_gaussian_noise(image, mean=0, std_dev_range=(5, 20)):
    """Adds Gaussian noise to the image."""
    std_dev = random.uniform(std_dev_range[0], std_dev_range[1])
    noise = np.random.normal(mean, std_dev, image.shape).astype(np.float32)
    noisy_image = image.astype(np.float32) + noise
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image

# --- Advanced Augmentations ---

def apply_cutout(image, num_holes=1, max_h_size=40, max_w_size=40, fill_value=0):
    """Applies Cutout augmentation by masking random rectangles."""
    h, w = image.shape[:2]
    img_cutout = image.copy()
    for _ in range(num_holes):
        y = np.random.randint(h)
        x = np.random.randint(w)
        h_hole = np.random.randint(1, max_h_size + 1)
        w_hole = np.random.randint(1, max_w_size + 1)

        y1 = np.clip(y - h_hole // 2, 0, h)
        y2 = np.clip(y + h_hole // 2, 0, h)
        x1 = np.clip(x - w_hole // 2, 0, w)
        x2 = np.clip(x + w_hole // 2, 0, w)

        img_cutout[y1:y2, x1:x2] = fill_value
    return img_cutout

def rand_bbox(size, lam):
    """Generates a random bounding box for CutMix."""
    W = size[1]
    H = size[0]
    cut_rat = np.sqrt(1. - lam)
    cut_w = int(W * cut_rat)
    cut_h = int(H * cut_rat)

    # Uniform
    cx = np.random.randint(W)
    cy = np.random.randint(H)

    bbx1 = np.clip(cx - cut_w // 2, 0, W)
    bby1 = np.clip(cy - cut_h // 2, 0, H)
    bbx2 = np.clip(cx + cut_w // 2, 0, W)
    bby2 = np.clip(cy + cut_h // 2, 0, H)

    return bbx1, bby1, bbx2, bby2

def apply_cutmix(image1, label1, image2, label2, alpha=1.0):
    """Applies CutMix augmentation between two images and their labels."""
    # Note: Labels are assumed to be one-hot encoded or compatible with mixing
    lam = np.random.beta(alpha, alpha)
    bbx1, bby1, bbx2, bby2 = rand_bbox(image1.shape, lam)

    mixed_image = image1.copy()
    mixed_image[bby1:bby2, bbx1:bbx2] = image2[bby1:bby2, bbx1:bbx2]

    # Adjust lambda to match pixel ratio
    lam = 1 - ((bbx2 - bbx1) * (bby2 - bby1) / (image1.shape[0] * image1.shape[1]))
    mixed_label = lam * label1 + (1. - lam) * label2

    return mixed_image, mixed_label

def apply_mixup(image1, label1, image2, label2, alpha=0.4):
    """Applies Mixup augmentation between two images and their labels."""
    # Note: Labels are assumed to be one-hot encoded or compatible with mixing
    lam = np.random.beta(alpha, alpha)
    mixed_image = lam * image1 + (1 - lam) * image2
    mixed_label = lam * label1 + (1 - lam) * label2
    # Clip image to valid range if necessary (though beta dist usually keeps it okay)
    mixed_image = np.clip(mixed_image, 0, 255).astype(np.uint8)
    return mixed_image, mixed_label

# --- Geometric Augmentations (Refined) ---

def apply_rotate(image, angle_range=(-15, 15), border_mode=cv2.BORDER_CONSTANT, border_value=0):
    """Rotates the image by a random angle."""
    angle = random.uniform(angle_range[0], angle_range[1])
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=border_mode, borderValue=border_value)
    return rotated

def apply_scale(image, scale_range=(0.9, 1.1), border_mode=cv2.BORDER_CONSTANT, border_value=0):
    """Scales the image randomly."""
    scale = random.uniform(scale_range[0], scale_range[1])
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, 0, scale)
    # Adjust output size or use warpAffine carefully if size changes
    scaled = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=border_mode, borderValue=border_value)
    return scaled

def apply_translate(image, translate_fraction=0.1, border_mode=cv2.BORDER_CONSTANT, border_value=0):
    """Translates the image randomly."""
    h, w = image.shape[:2]
    max_dx = w * translate_fraction
    max_dy = h * translate_fraction
    dx = random.uniform(-max_dx, max_dx)
    dy = random.uniform(-max_dy, max_dy)
    matrix = np.float32([[1, 0, dx], [0, 1, dy]])
    translated = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=border_mode, borderValue=border_value)
    return translated

def apply_shear(image, shear_range=(-10, 10), border_mode=cv2.BORDER_CONSTANT, border_value=0):
    """Applies shear transformation randomly."""
    shear_x = random.uniform(shear_range[0], shear_range[1])
    shear_y = random.uniform(shear_range[0], shear_range[1])
    h, w = image.shape[:2]
    center = (w / 2, h / 2)
    
    # Convert degrees to radians for tan function
    shear_x_rad = np.deg2rad(shear_x)
    shear_y_rad = np.deg2rad(shear_y)
    
    # Shear matrix
    matrix = np.float32([[1, np.tan(shear_x_rad), 0], 
                         [np.tan(shear_y_rad), 1, 0]])
    
    # Apply shear around the center
    # Translate center to origin, shear, translate back
    M = cv2.getRotationMatrix2D(center, 0, 1.0)
    M[0, 2] -= center[0]
    M[1, 2] -= center[1]
    
    shear_matrix = np.dot(matrix, M[:2])
    
    # Add translation back
    shear_matrix[0, 2] += center[0]
    shear_matrix[1, 2] += center[1]

    sheared = cv2.warpAffine(image, shear_matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=border_mode, borderValue=border_value)
    return sheared

def apply_flip_lr(image):
    """Applies horizontal flip."""
    return cv2.flip(image, 1)

def apply_flip_ud(image):
    """Applies vertical flip."""
    return cv2.flip(image, 0)

# --- Main Augmentation Pipeline ---

def augment_image(image, config=None):
    """
    Applies a sequence of augmentations based on the provided config.
    Note: CutMix and Mixup require pairs of images/labels and are typically applied
          at the batch level in the data loader, not here on single images.
    """
    if config is None:
        config = DEFAULT_AUGMENTATION_CONFIG

    augmented_image = image.copy()

    # Color/Pixel Augmentations
    if "brightness_contrast" in config and random.random() < config["brightness_contrast"]["p"]:
        augmented_image = apply_brightness_contrast(augmented_image, **{k:v for k,v in config["brightness_contrast"].items() if k != 'p'})
    if "hsv_jitter" in config and random.random() < config["hsv_jitter"]["p"]:
        augmented_image = apply_hsv_jitter(augmented_image, **{k:v for k,v in config["hsv_jitter"].items() if k != 'p'})
    if "blur" in config and random.random() < config["blur"]["p"]:
        augmented_image = apply_blur(augmented_image, **{k:v for k,v in config["blur"].items() if k != 'p'})
    if "noise" in config and random.random() < config["noise"]["p"]:
        augmented_image = add_gaussian_noise(augmented_image, **{k:v for k,v in config["noise"].items() if k != 'p'})
    if "cutout" in config and random.random() < config["cutout"]["p"]:
        augmented_image = apply_cutout(augmented_image, **{k:v for k,v in config["cutout"].items() if k != 'p'})

    # Geometric Augmentations
    if "rotate" in config and random.random() < config["rotate"]["p"]:
        augmented_image = apply_rotate(augmented_image, **{k:v for k,v in config["rotate"].items() if k != 'p'})
    if "scale" in config and random.random() < config["scale"]["p"]:
        augmented_image = apply_scale(augmented_image, **{k:v for k,v in config["scale"].items() if k != 'p'})
    if "translate" in config and random.random() < config["translate"]["p"]:
        augmented_image = apply_translate(augmented_image, **{k:v for k,v in config["translate"].items() if k != 'p'})
    if "shear" in config and random.random() < config["shear"]["p"]:
        augmented_image = apply_shear(augmented_image, **{k:v for k,v in config["shear"].items() if k != 'p'})
    if "flip_lr" in config and random.random() < config["flip_lr"]["p"]:
        augmented_image = apply_flip_lr(augmented_image)
    if "flip_ud" in config and random.random() < config["flip_ud"]["p"]:
        augmented_image = apply_flip_ud(augmented_image)

    return augmented_image

# --- Example Usage ---
if __name__ == "__main__":
    # Load a sample image
    # Create a dummy image for demonstration if no file exists
    sample_image = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.rectangle(sample_image, (50, 50), (250, 250), (0, 255, 0), -1)
    cv2.putText(sample_image, "Original", (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    print("Applying augmentations...")
    augmented = augment_image(sample_image)

    # --- CutMix/Mixup Example (requires two images/labels) ---
    sample_image2 = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.circle(sample_image2, (150, 150), 100, (0, 0, 255), -1)
    # Dummy labels (e.g., one-hot encoded)
    label1 = np.array([1.0, 0.0])
    label2 = np.array([0.0, 1.0])

    # Apply CutMix
    if DEFAULT_AUGMENTATION_CONFIG["cutmix"]["p"] > 0:
        cutmix_img, cutmix_label = apply_cutmix(sample_image, label1, sample_image2, label2, alpha=DEFAULT_AUGMENTATION_CONFIG["cutmix"]["alpha"])
        print(f"CutMix Label: {cutmix_label}")
        # cv2.imshow("CutMix Image", cutmix_img)

    # Apply Mixup
    if DEFAULT_AUGMENTATION_CONFIG["mixup"]["p"] > 0:
        mixup_img, mixup_label = apply_mixup(sample_image, label1, sample_image2, label2, alpha=DEFAULT_AUGMENTATION_CONFIG["mixup"]["alpha"])
        print(f"Mixup Label: {mixup_label}")
        # cv2.imshow("Mixup Image", mixup_img)

    # Display the single-image augmented result
    # cv2.imshow("Original Image", sample_image)
    # cv2.imshow("Augmented Image", augmented)
    print("Augmentation applied. (Display commented out)")

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

