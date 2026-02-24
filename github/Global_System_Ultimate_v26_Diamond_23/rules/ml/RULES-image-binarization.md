# Image Binarization Rules (v26.0)

> **Scope**: Computer Vision Preprocessing
> **Compliance**: Multi-View Plant Disease Detection
> **Version**: 26.0.0

## 1. Thresholding Strategy

### 1.1 Adaptive Thresholding (Default for Field Images)
*   **Method**: `cv2.adaptiveThreshold`
*   **Block Size**: 11 (Must be odd)
*   **C Constant**: 2
*   **Why**: Handles uneven lighting conditions better than global Otsu.
*   **When**: Field photos, variable lighting, partial shade.

### 1.2 Otsu’s Binarization (Lab Conditions)
*   **Method**: `cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)`
*   **Use Case**: High contrast images with bimodal histogram.
*   **Constraint**: Input image must be grayscale.
*   **When**: Controlled lab lighting, uniform background.

### 1.3 SAM2 Segmentation (Complex Scenes)
*   **Method**: Meta SAM2 with automatic point prompting.
*   **Use Case**: Overlapping leaves, complex canopy, multiple plants.
*   **Constraint**: Requires GPU. ~200ms per image vs ~3ms for Otsu.
*   **When**: Accuracy priority, GPU available, field-level analysis.

### 1.4 Decision Tree
```mermaid
graph TD
    A[Is GPU available AND accuracy > speed?]
    A -- YES --> B{Complex scene (overlapping)?}
    B -- YES --> C[SAM2]
    B -- NO --> D[Adaptive Threshold]
    A -- NO --> E{Uniform lighting?}
    E -- YES --> F[Otsu]
    E -- NO --> D
```

## 2. Morphological Operations

### 2.1 HARD LIMITS (Never Exceed)
*   **Maximum Kernel Size**: 15×15 pixels.
*   **Maximum Iterations**: 5 per operation.
*   **Kernel Shape**: Elliptical (`cv2.MORPH_ELLIPSE`) default.

### 2.2 Standard Pipeline
*   **Noise Removal (Opening)**: `kernel=(3,3)`, `iterations=1`
*   **Hole Filling (Closing)**: `kernel=(5,5)`, `iterations=2`

### 2.3 Advanced Cleanup
*   **Top Hat**: `(9,9)` → Isolate bright spots on dark background.
*   **Black Hat**: `(9,9)` → Isolate dark spots on bright background.

## 3. Quality Gates
| Metric | Min | Max | Action on Failure |
| :--- | :--- | :--- | :--- |
| **Foreground Ratio** | 5% | 60% | Reject image |
| **Contour Count** | 1 | 50 | Reject (noisy) |
| **Min Contour Area** | 100 px² | — | Filter noise |

## 4. Color Space Conversion

### 4.1 HSV Ranges (OpenCV Scale)
| Condition | H | S | V |
| :--- | :--- | :--- | :--- |
| **Healthy Green** | 35-85 | 40-255 | 40-255 |
| **Chlorosis** | 20-35 | 50-255 | 50-255 |
| **Necrosis** | 10-20 | 50-200 | 20-150 |
| **Powdery Mildew** | 0-180 | 0-30 | 200-255 |
| **Rust** | 10-25 | 150-255 | 100-255 |

### 4.2 Vegetation Indices
*   **ExGR**: `(2*G - R - B) - (1.4*R - G)` (Zero threshold)
*   **ExG**: `2*G - R - B` (Otsu threshold)
*   **NGRDI**: `(G-R)/(G+R)`

## 5. Multi-View Binary Generation
| View | Method | Purpose |
| :--- | :--- | :--- |
| **Green Mask** | HSV green threshold | Healthy tissue |
| **Disease Mask** | HSV disease threshold | Diseased regions |
| **Edge Binary** | Canny (σ=1.5) | Lesion boundaries |
| **Texture Binary** | LBP variance threshold | Textural changes |
| **Saturation Binary** | S-channel adaptive | Foreground/background |

## 6. Disease-Specific Patterns
*   **Early Blight**: V-channel < 100, S > 50. Opening(3,3) → Closing(5,5).
*   **Late Blight**: H=60-100, S=20-60, V=40-120. Closing(7,7).
*   **Powdery Mildew**: V > 200, S < 30. Opening(5,5).
*   **Rust**: H=10-25, S > 150, V > 100. min_area=50px².

## 7. Code Example (OpenCV)
```python
import cv2
import numpy as np

def binarize_leaf(image_path: str, method: str = "adaptive") -> np.ndarray:
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s_channel = hsv[:, :, 1]

    if method == "otsu":
        _, binary = cv2.threshold(s_channel, 0, 255,
                                  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method == "adaptive":
        binary = cv2.adaptiveThreshold(
            s_channel, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
    else:
        raise ValueError(f"Unknown method: {method}")

    # Morphological Cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_close, iterations=2)

    # Quality Gate
    fg_ratio = np.count_nonzero(binary) / binary.size
    if fg_ratio < 0.05 or fg_ratio > 0.60:
        raise ValueError(f"Foreground ratio {fg_ratio:.2%} outside 5-60% range")

    return binary
```

## 8. Cross-References
*   **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md`
*   **Error Catalog**: `errors/ml/ERROR-multi-view-pipeline-catalog.md` → `ERR-BIN-001`
