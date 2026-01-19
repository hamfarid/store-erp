# /home/ubuntu/ai_web_organized/src/modules/internal_diagnosis/service.py

"""Service class for performing internal diagnosis, including disease detection.
Enhanced to support flexible knowledge base (YAML/DB) and integration with external diagnostic tools.
"""

import json
import os
import sqlite3  # For DB-based knowledge base
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml

# Add project root to sys.path to allow imports
project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", ".."))  # Adjusted for new depth
sys.path.insert(0, project_root)

# Import logger
try:
    from src.modules.log_activity.activity_logger import (
        actividad_logger,  # Corrected import
    )
    logger = actividad_logger  # Use the specific logger instance
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(
        "Log Activity module (actividad_logger) not found. Using standard logging.")

# Import Model Registry and Preprocessor
try:
    from src.modules.training_pipeline import DataPreprocessor, ModelRegistry
except ImportError:
    logger.error(
        "Training Pipeline module (ModelRegistry, DataPreprocessor) not found. Diagnosis service cannot load models.")
    ModelRegistry = None
    DataPreprocessor = None

# Placeholder for deep learning framework (PyTorch)
try:
    import torch
    import torch.nn as nn
    from PIL import Image
except ImportError:
    logger.warning(
        "PyTorch or Pillow not installed. Image-based diagnosis will be simulated.")
    torch = None
    nn = None
    Image = None

# Mock models (unchanged from previous version, kept for compatibility
# with tests)
if nn:
    class MockBaseForDiagnosis(nn.Module):
        def __init__(self):
            super().__init__()

        def predict(self, *args, **kwargs) -> Dict[str, Any]:
            logger.debug("{self.__class__.__name__} predict called")
            return {"mock_result": "success", "model_type": "nn-based"}

    class MockVarietyIDModel(MockBaseForDiagnosis):
        def predict(self, image_path: str, **kwargs) -> Dict[str, Any]:
            logger.info("[MockVarietyIDModel] Predicting for {image_path}")
            return {
                "name": "Mocked Tomato - Roma",
                "confidence": 0.98,
                "details": "Mocked variety"}

    class MockAnomalyDetectionModel(MockBaseForDiagnosis):
        def predict(self, image_path: str,
                    variety_info: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            logger.info(
                "[MockAnomalyDetectionModel] Predicting for {image_path} with variety {variety_info.get('name')}")
            return {
                "detected": True,
                "details": "Mocked irregular yellow spots",
                "methods_used": ["mock_method"]}

    class MockClassificationModel(MockBaseForDiagnosis):
        def predict(self,
                    image_path: str,
                    variety_info: Dict[str,
                                       Any],
                    anomaly_info: Dict[str,
                                       Any],
                    **kwargs) -> Dict[str,
                                      Any]:
            logger.info(
                "[MockClassificationModel] Predicting for {image_path} with anomaly detected: {anomaly_info.get('detected')}")
            if anomaly_info.get("detected"):
                return {
                    "diagnosis": "Mocked Early Blight",
                    "confidence": 0.91,
                    "treatment_suggestion": "Mocked treatment"}
            return {"diagnosis": "Mocked Healthy", "confidence": 0.99}
else:
    class MockBaseForDiagnosis:
        def predict(self, *args, **kwargs) -> Dict[str, Any]:
            logger.debug("{self.__class__.__name__} (no-nn) predict called")
            return {"mock_result": "success (no-nn)", "model_type": "basic"}

    class MockVarietyIDModel(MockBaseForDiagnosis):
        def predict(self, image_path: str, **kwargs) -> Dict[str, Any]:
            logger.info(
                "[MockVarietyIDModel no-nn] Predicting for {image_path}")
            return {
                "name": "Mocked Tomato - Roma (no-nn)",
                "confidence": 0.98,
                "details": "Mocked variety (no-nn)"}

    class MockAnomalyDetectionModel(MockBaseForDiagnosis):
        def predict(self, image_path: str,
                    variety_info: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            logger.info(
                "[MockAnomalyDetectionModel no-nn] Predicting for {image_path} with variety {variety_info.get('name')}")
            return {
                "detected": True,
                "details": "Mocked irregular yellow spots (no-nn)",
                "methods_used": ["mock_method_no_nn"]}

    class MockClassificationModel(MockBaseForDiagnosis):
        def predict(self,
                    image_path: str,
                    variety_info: Dict[str,
                                       Any],
                    anomaly_info: Dict[str,
                                       Any],
                    **kwargs) -> Dict[str,
                                      Any]:
            logger.info(
                "[MockClassificationModel no-nn] Predicting for {image_path} with anomaly detected: {anomaly_info.get('detected')}")
            if anomaly_info.get("detected"):
                return {
                    "diagnosis": "Mocked Early Blight (no-nn)",
                    "confidence": 0.91,
                    "treatment_suggestion": "Mocked treatment (no-nn)"}
            return {"diagnosis": "Mocked Healthy (no-nn)", "confidence": 0.99}


class InternalDiagnosisService:
    """Provides functionality for diagnosing plant issues based on various inputs."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        default_registry_path = "/app/model_registry"
        self.registry_path = os.getenv(
            "MODEL_REGISTRY_PATH", self.config.get(
                "model_registry_path", default_registry_path))
        logger.info("Using Model Registry Path: {self.registry_path}")

        # Knowledge Base Configuration
        self.kb_type = self.config.get(
            "knowledge_base_type", "yaml")  # yaml or db
        self.kb_path = self.config.get(
            "knowledge_base_path",
            "knowledge_base.yaml")  # Path for YAML or DB file
        if self.kb_type == "yaml" and not os.path.isabs(self.kb_path):
            self.kb_path = os.path.join(
                os.path.dirname(__file__), self.kb_path)
        elif self.kb_type == "db" and not os.path.isabs(self.kb_path):
            self.kb_path = os.path.join(
                os.path.dirname(__file__), self.kb_path)

        logger.info(
            "Using Knowledge Base Type: {self.kb_type}, Path: {self.kb_path}")

        self.default_model_name = self.config.get(
            "default_diagnosis_model_name",
            "plant_disease_classifier_resnet50")
        self.default_model_version = self.config.get(
            "default_diagnosis_model_version", "latest")
        self.device = self.config.get("device", "cpu")

        self.model_registry = None
        self.preprocessor = None
        self.loaded_models: Dict[str,
                                 Tuple[Optional[Union[nn.Module,
                                                      object]],
                                       Dict[str,
                                            Any]]] = {}
        self.label_maps: Dict[str, Dict[int, str]] = {}

        if ModelRegistry:
            try:
                if not os.path.isdir(self.registry_path):
                    logger.warning(
                        "Model registry path does not exist: {self.registry_path}. Model loading might fail.")
                self.model_registry = ModelRegistry(
                    registry_path=self.registry_path)
                logger.info(
                    "ModelRegistry initialized for path: {self.registry_path}")
            except Exception as e:
                logger.error(
                    "Failed to initialize ModelRegistry: %s", e,
                    exc_info=True)
                self.model_registry = None
        else:
            logger.error("ModelRegistry class could not be imported.")

        if DataPreprocessor:
            preprocessor_config = self.config.get("preprocessor_config", {})
            self.preprocessor = DataPreprocessor(config=preprocessor_config)
            logger.info("DataPreprocessor initialized.")
        else:
            logger.error("DataPreprocessor could not be initialized.")

        self.knowledge_base = self._load_knowledge_base()
        # If DB is empty or failed to load, try to initialize schema
        if self.kb_type == "db" and not self.knowledge_base:
            self._initialize_db_kb_schema()

        # Mock models initialization (unchanged)
        self.variety_model = MockVarietyIDModel()
        self.anomaly_model = MockAnomalyDetectionModel()
        self.classification_model = MockClassificationModel()
        logger.info(
            "InternalDiagnosisService initialized with enhanced KB and external tool integration placeholders.")

    def _initialize_db_kb_schema(self):
        """Initializes the schema for the SQLite knowledge base if it doesn't exist."""
        if self.kb_type != "db":
            return
        try:
            conn = sqlite3.connect(self.kb_path)
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_name TEXT UNIQUE NOT NULL,
                symptoms TEXT,
                causes TEXT,
                treatment_protocols TEXT, -- JSON string for multiple protocols
                preventive_measures TEXT, -- JSON string
                affected_crops TEXT, -- JSON string of crop names
                references TEXT, -- JSON string of URLs or citations
                additional_notes TEXT,
                severity_levels TEXT, -- JSON mapping severity to description
                image_examples TEXT -- JSON list of image URLs/paths
            )
            """)
            conn.commit()
            logger.info(
                "SQLite knowledge base schema initialized/verified at {self.kb_path}")
        except sqlite3.Error as e:
            logger.error(
                "Error initializing SQLite KB schema at %s: %s",
                self.kb_path,
                e,
                exc_info=True)
        finally:
            if conn:
                conn.close()

    def _load_knowledge_base(self) -> Union[List[Dict[str, Any]], None]:
        """Loads the knowledge base from YAML or DB."""
        if self.kb_type == "yaml":
            if not os.path.exists(
                    self.kb_path) or not os.path.isfile(
                    self.kb_path):
                logger.error(
                    "YAML Knowledge base file not found or not a file: {self.kb_path}")
                return []
            try:
                with open(self.kb_path, 'r', encoding='utf-8') as f:
                    kb = yaml.safe_load(f)
                if isinstance(kb, list):
                    logger.info(
                        "YAML Knowledge base loaded from {self.kb_path} ({len(kb)} entries).")
                    return kb
                else:
                    logger.error(
                        "YAML KB format incorrect (expected list): {self.kb_path}")
                    return []
            except Exception as e:
                logger.error(
                    "Error loading YAML KB from %s: %s", self.kb_path, e,
                    exc_info=True)
                return []
        elif self.kb_type == "db":
            if not os.path.exists(self.kb_path):
                logger.warning(
                    "SQLite KB file not found: {self.kb_path}. Will attempt to create.")
                self._initialize_db_kb_schema()  # Attempt to create if not found
                # After creation, it will be empty, so return empty list or
                # None
                return []  # Or None, depending on how you want to handle a fresh DB
            try:
                conn = sqlite3.connect(self.kb_path)
                conn.row_factory = sqlite3.Row  # Access columns by name
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM knowledge_entries")
                rows = cursor.fetchall()
                kb_entries = [dict(row) for row in rows]
                # Deserialize JSON fields
                for entry in kb_entries:
                    for field in [
                        'treatment_protocols',
                        'preventive_measures',
                        'affected_crops',
                        'references',
                        'severity_levels',
                            'image_examples']:
                        if entry.get(field) and isinstance(entry[field], str):
                            try:
                                entry[field] = json.loads(entry[field])
                            except json.JSONDecodeError:
                                logger.warning(
                                    "Could not decode JSON for field {field} in entry ID {entry.get('id')}")
                                # Or keep as string, or handle error
                                entry[field] = None
                logger.info(
                    "SQLite Knowledge base loaded from {self.kb_path} ({len(kb_entries)} entries).")
                return kb_entries
            except sqlite3.Error as e:
                logger.error(
                    "Error loading SQLite KB from %s: %s", self.kb_path, e,
                    exc_info=True)
                return None  # Indicate failure to load
            finally:
                if conn:
                    conn.close()
        else:
            logger.error("Unsupported knowledge_base_type: {self.kb_type}")
            return None

    def add_kb_entry(self, entry_data: Dict[str, Any]) -> bool:
        """Adds a new entry to the knowledge base."""
        if self.kb_type == "yaml":
            logger.warning(
                "Adding entries to YAML KB directly is not recommended for live systems. Consider DB.")
            # For simplicity, this example won't write back to YAML. In a real
            # scenario, you'd append and save.
            if isinstance(self.knowledge_base, list):
                self.knowledge_base.append(entry_data)
                # self._save_yaml_kb() # Implement this if you need to persist
                logger.info(
                    "Entry for {entry_data.get('disease_name')} added to in-memory YAML KB.")
                return True
            return False
        elif self.kb_type == "db":
            try:
                conn = sqlite3.connect(self.kb_path)
                cursor = conn.cursor()
                # Serialize JSON fields
                for field in [
                    'treatment_protocols',
                    'preventive_measures',
                    'affected_crops',
                    'references',
                    'severity_levels',
                        'image_examples']:
                    if field in entry_data and not isinstance(
                            entry_data[field], str):
                        entry_data[field] = json.dumps(entry_data[field])

                columns = ', '.join(entry_data.keys())
                placeholders = ', '.join(['?'] * len(entry_data))
                sql = f"INSERT INTO knowledge_entries ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(entry_data.values()))
                conn.commit()
                logger.info(
                    "Entry for {entry_data.get('disease_name')} added to SQLite KB.")
                self.knowledge_base = self._load_knowledge_base()  # Refresh cache
                return True
            except sqlite3.Error as e:
                logger.error(
                    "Error adding entry to SQLite KB: %s", e,
                    exc_info=True)
                return False
            finally:
                if conn:
                    conn.close()
        return False

    def update_kb_entry(self, disease_name: str,
                        update_data: Dict[str, Any]) -> bool:
        """Updates an existing entry in the knowledge base by disease_name."""
        if self.kb_type == "yaml":
            logger.warning(
                "Updating YAML KB directly is complex. Consider DB.")
            # Find and update in-memory list; persistence would require saving
            # the whole list.
            return False  # Placeholder
        elif self.kb_type == "db":
            try:
                conn = sqlite3.connect(self.kb_path)
                cursor = conn.cursor()
                # Serialize JSON fields in update_data
                for field in [
                    'treatment_protocols',
                    'preventive_measures',
                    'affected_crops',
                    'references',
                    'severity_levels',
                        'image_examples']:
                    if field in update_data and not isinstance(
                            update_data[field], str):
                        update_data[field] = json.dumps(update_data[field])

                set_clause = ', '.join(
                    [f"{key} = ?" for key in update_data.keys()])
                sql = f"UPDATE knowledge_entries SET {set_clause} WHERE disease_name = ?"
                values = list(update_data.values()) + [disease_name]
                cursor.execute(sql, values)
                conn.commit()
                if cursor.rowcount > 0:
                    logger.info(
                        "Entry for {disease_name} updated in SQLite KB.")
                    self.knowledge_base = self._load_knowledge_base()  # Refresh cache
                    return True
                else:
                    logger.warning(
                        "No entry found for {disease_name} to update in SQLite KB.")
                    return False
            except sqlite3.Error as e:
                logger.error(
                    "Error updating entry in SQLite KB: %s", e,
                    exc_info=True)
                return False
            finally:
                if conn:
                    conn.close()
        return False

    def _get_model_key(
            self,
            model_name: Optional[str] = None,
            version: Optional[str] = None) -> str:
        name = model_name or self.default_model_name
        ver = version or self.default_model_version
        return f"{name}:{ver}"

    def _load_model_if_needed(self,
                              model_name: Optional[str] = None,
                              version: Optional[str] = None) -> Optional[Tuple[Optional[Union[nn.Module,
                                                                                              object]],
                                                                               Optional[Dict[int,
                                                                                             str]]]]:
        if not self.model_registry or not torch or not nn:
            logger.error(
                "ModelRegistry or PyTorch not available. Cannot load model.")
            return None
        model_key = self._get_model_key(model_name, version)
        if model_key in self.loaded_models:
            logger.debug("Using cached model: {model_key}")
            model, _ = self.loaded_models[model_key]
            label_map = self.label_maps.get(model_key)
            return model, label_map
        logger.info("Attempting to load model: {model_key}")
        loaded_data = None
        try:
            loaded_data = self.model_registry.load_model(
                model_name=model_name or self.default_model_name,
                version=version or self.default_model_version,
                device=self.device
            )
        except FileNotFoundError:
            logger.error("Model file not found in registry for {model_key}")
            return None
        except Exception as e:
            logger.error(
                "Error loading model %s from registry: %s", model_key, e,
                exc_info=True)
            return None
        if loaded_data:
            model, metadata = loaded_data
            self.loaded_models[model_key] = (model, metadata)
            label_map = None
            label_map_from_metadata = metadata.get(
                "training_params", {}).get("label_map")
            if isinstance(label_map_from_metadata, dict):
                try:
                    label_map = {int(k): str(v)
                                 for k, v in label_map_from_metadata.items()}
                    logger.info(
                        "Loaded label map from metadata for {model_key}")
                except (ValueError, TypeError):
                    logger.warning(
                        "Could not parse label map from metadata for {model_key}.")
                    label_map = None
            if label_map is None and nn and model:
                # Determine num_classes from model structure (as before)
                num_classes = -1
                # ... (code for determining num_classes from model.fc or model.classifier as in previous version)
                if hasattr(
                        model,
                        'fc') and isinstance(
                        model.fc,
                        nn.modules.linear.Linear):
                    num_classes = model.fc.out_features
                elif hasattr(model, 'classifier'):
                    if isinstance(model.classifier, nn.modules.linear.Linear):
                        num_classes = model.classifier.out_features
                    elif isinstance(model.classifier, nn.Sequential):
                        for layer in reversed(model.classifier):
                            if isinstance(layer, nn.modules.linear.Linear):
                                num_classes = layer.out_features
                                break
                if num_classes > 0:
                    label_map = {i: f"Class_{i}" for i in range(num_classes)}
                    logger.warning(
                        "Created dummy label map for {model_key} with {num_classes} classes.")
                else:
                    logger.error(
                        "Could not determine label map for model {model_key}")
            if label_map:
                self.label_maps[model_key] = label_map
            logger.info(
                "Successfully loaded model {model_key}. Label map {'found' if label_map else 'not found/created'}.")
            return model, label_map
        return None

    def diagnose_from_image(self,
                            image_path: str,
                            model_name: Optional[str] = None,
                            version: Optional[str] = None) -> Dict[str,
                                                                   Any]:
        if not self.preprocessor or not Image:
            logger.error(
                "Preprocessor or Pillow not available for image diagnosis.")
            return {"error": "Image processing components not available."}
        model_data = self._load_model_if_needed(model_name, version)
        if not model_data or not model_data[0]:
            return {"error": "Model could not be loaded."}
        model, label_map = model_data
        if not label_map:
            logger.warning(
                "Label map not available for model {self._get_model_key(model_name, version)}. Predictions will be class indices.")
        try:
            img = Image.open(image_path)
            img_tensor = self.preprocessor.preprocess_image_for_inference(
                img, target_size=(224, 224))  # Example size
            img_tensor = img_tensor.unsqueeze(0).to(
                self.device)  # Add batch dim and send to device

            with torch.no_grad():
                model.eval()
                outputs = model(img_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)

            predicted_class_idx = predicted_idx.item()
            predicted_class_name = label_map.get(
                predicted_class_idx,
                "Unknown_Class_{predicted_class_idx}") if label_map else "Class_{predicted_class_idx}"

            result = {
                "prediction_index": predicted_class_idx,
                "predicted_class": predicted_class_name,
                "confidence": confidence.item(),
                "model_used": self._get_model_key(model_name, version)
            }
            # Augment with knowledge base info
            kb_info = self.get_knowledge_base_entry(predicted_class_name)
            if kb_info:
                result["knowledge_base_info"] = kb_info
            else:
                result["knowledge_base_info"] = "No information found in knowledge base for this diagnosis."
            return result
        except Exception as e:
            logger.error("Error during image diagnosis: {e}", exc_info=True)
            return {"error": str(e)}

    def get_knowledge_base_entry(
            self, disease_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves an entry from the knowledge base by disease name."""
        if not self.knowledge_base:
            logger.warning("Knowledge base is not loaded or is empty.")
            return None
        for entry in self.knowledge_base:
            if entry.get("disease_name", "").lower() == disease_name.lower():
                return entry
        logger.debug("No KB entry found for disease: {disease_name}")
        return None

    def search_knowledge_base(
            self, query: str, search_fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Searches the knowledge base for entries matching the query in specified fields."""
        if not self.knowledge_base:
            return []
        results = []
        query_lower = query.lower()
        fields_to_search = search_fields or [
            "disease_name", "symptoms", "causes", "affected_crops"]

        for entry in self.knowledge_base:
            for field in fields_to_search:
                field_value = entry.get(field)
                if field_value:
                    # Handle if field_value is a list (e.g., affected_crops
                    # from YAML)
                    if isinstance(field_value, list):
                        if any(query_lower in str(item).lower()
                               for item in field_value):
                            results.append(entry)
                            break  # Found in this entry, move to next entry
                    elif isinstance(field_value, str):
                        if query_lower in field_value.lower():
                            results.append(entry)
                            break  # Found in this entry
        logger.info(
            "KB search for '{query}' in fields {fields_to_search} found {len(results)} results.")
        return results

    # --- Placeholder for External Tool Integration ---
    def consult_external_diagnostic_tool(
            self, tool_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """(Placeholder) Consults an external diagnostic tool or API.
        In a real implementation, this would involve HTTP requests, SDK calls, etc.
        """
        logger.info(
            "Consulting external tool: {tool_name} with data: {data.get('image_path', 'N/A')}")
        # Example: Simulate calling a hypothetical PlantNet API or similar
        if tool_name == "plantnet_mock":
            # Simulate a response structure
            return {
                "tool_name": tool_name,
                "status": "success",
                "results": [
                    {"species": "Solanum lycopersicum", "score": 0.85, "common_names": ["Tomato"]},
                    {"species": "Capsicum annuum", "score": 0.10, "common_names": ["Pepper"]}
                ],
                "message": "Mock response from PlantNet-like service."
            }
        elif tool_name == "disease_lookup_api_mock":
            disease_query = data.get("disease_name", "unknown")
            return {
                "tool_name": tool_name,
                "status": "success",
                "data": {
                    "disease_name": disease_query,
                    "external_info": f"Mock detailed info for {disease_query} from external API.",
                    "control_methods": [
                        "Method A",
                        "Method B"]}}
        else:
            logger.warning(
                "External tool '{tool_name}' not implemented or recognized.")
            return {
                "tool_name": tool_name,
                "status": "error",
                "message": "Tool not implemented"}

    def comprehensive_diagnosis(self,
                                image_path: Optional[str] = None,
                                textual_symptoms: Optional[str] = None,
                                external_tools_to_consult: Optional[List[str]] = None) -> Dict[str,
                                                                                               Any]:
        """Provides a comprehensive diagnosis using internal models, KB, and optionally external tools."""
        final_report = {
            "inputs": {},
            "internal_diagnosis": {},
            "knowledge_base_search": {},
            "external_consultations": [],
            "summary": ""}

        if image_path:
            final_report["inputs"]["image_path"] = image_path
            internal_image_diag = self.diagnose_from_image(image_path)
            final_report["internal_diagnosis"]["image_based"] = internal_image_diag
            if not internal_image_diag.get(
                    "error") and internal_image_diag.get("predicted_class"):
                # Use the predicted class for KB search if available
                kb_search_results = self.search_knowledge_base(
                    internal_image_diag["predicted_class"])
                final_report["knowledge_base_search"]["based_on_image_prediction"] = kb_search_results

        if textual_symptoms:
            final_report["inputs"]["textual_symptoms"] = textual_symptoms
            kb_symptom_search = self.search_knowledge_base(
                textual_symptoms, search_fields=["symptoms", "disease_name"])
            final_report["knowledge_base_search"]["based_on_textual_symptoms"] = kb_symptom_search

        if external_tools_to_consult:
            for tool_name in external_tools_to_consult:
                # Prepare data for the tool, could be image_path or other info
                tool_data = {"image_path": image_path} if image_path else {}
                if textual_symptoms and "disease_lookup" in tool_name:  # Example specific data for a tool
                    # Or a parsed disease name
                    tool_data["disease_name"] = textual_symptoms

                consult_result = self.consult_external_diagnostic_tool(
                    tool_name, tool_data)
                final_report["external_consultations"].append(consult_result)

        # Basic summary logic (can be made more sophisticated)
        summary_points = []
        if final_report["internal_diagnosis"].get(
                "image_based", {}).get("predicted_class"):
            summary_points.append(
                "Image diagnosis: {final_report['internal_diagnosis']['image_based']['predicted_class']}")
        if final_report["knowledge_base_search"].get(
                "based_on_textual_symptoms"):
            summary_points.append(
                "Found {len(final_report['knowledge_base_search']['based_on_textual_symptoms'])} KB entries for symptoms.")
        final_report["summary"] = "; ".join(
            summary_points) if summary_points else "No conclusive findings or actions performed."

        logger.info("Comprehensive diagnosis report generated.")
        return final_report


logger.info(
    "InternalDiagnosisService (service.py) loaded with enhanced KB and external tool integration.")
