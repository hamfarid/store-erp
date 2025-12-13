# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Startup Logger
Tracks all imports, exports, component loading, and startup progress
"""

import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import importlib.util
import json


class StartupLogger:
    """Logs all startup activities"""

    def __init__(self, logger):
        self.logger = logger
        self.start_time = time.time()
        self.imports = []
        self.blueprints = []
        self.models = []
        self.errors = []
        self.warnings = []

    def log_import(self, module_name, success=True, error=None):
        """Log module import"""
        import_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "module": module_name,
            "success": success,
            "error": str(error) if error else None,
            "elapsed_seconds": round(time.time() - self.start_time, 3),
        }

        self.imports.append(import_data)

        if success:
            self.logger.log_startup(
                event="import_success",
                module=module_name,
                elapsed=import_data["elapsed_seconds"],
            )
        else:
            self.logger.log_startup(
                event="import_failed",
                module=module_name,
                error=str(error),
                elapsed=import_data["elapsed_seconds"],
            )
            self.errors.append(import_data)

    def log_blueprint(self, blueprint_name, success=True, error=None):
        """Log blueprint registration"""
        blueprint_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "blueprint": blueprint_name,
            "success": success,
            "error": str(error) if error else None,
            "elapsed_seconds": round(time.time() - self.start_time, 3),
        }

        self.blueprints.append(blueprint_data)

        if success:
            self.logger.log_startup(
                event="blueprint_registered",
                blueprint=blueprint_name,
                elapsed=blueprint_data["elapsed_seconds"],
            )
        else:
            self.logger.log_startup(
                event="blueprint_failed",
                blueprint=blueprint_name,
                error=str(error),
                elapsed=blueprint_data["elapsed_seconds"],
            )
            self.errors.append(blueprint_data)

    def log_model(self, model_name, success=True, error=None):
        """Log model loading"""
        model_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model_name,
            "success": success,
            "error": str(error) if error else None,
            "elapsed_seconds": round(time.time() - self.start_time, 3),
        }

        self.models.append(model_data)

        if success:
            self.logger.log_startup(
                event="model_loaded",
                model=model_name,
                elapsed=model_data["elapsed_seconds"],
            )
        else:
            self.logger.log_startup(
                event="model_failed",
                model=model_name,
                error=str(error),
                elapsed=model_data["elapsed_seconds"],
            )
            self.errors.append(model_data)

    def log_warning(self, message, **kwargs):
        """Log warning"""
        warning_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "elapsed_seconds": round(time.time() - self.start_time, 3),
            **kwargs,
        }

        self.warnings.append(warning_data)
        self.logger.log_startup(event="warning", message=message, **kwargs)

    def log_error(self, message, **kwargs):
        """Log error"""
        error_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "elapsed_seconds": round(time.time() - self.start_time, 3),
            **kwargs,
        }

        self.errors.append(error_data)
        self.logger.log_startup(event="error", message=message, **kwargs)

    def log_config(self, key, value):
        """Log configuration"""
        self.logger.log_startup(
            event="config_loaded",
            key=key,
            value=str(value),
            elapsed=round(time.time() - self.start_time, 3),
        )

    def log_database_init(self, success=True, error=None):
        """Log database initialization"""
        if success:
            self.logger.log_startup(
                event="database_initialized",
                elapsed=round(time.time() - self.start_time, 3),
            )
        else:
            self.logger.log_startup(
                event="database_init_failed",
                error=str(error),
                elapsed=round(time.time() - self.start_time, 3),
            )
            self.errors.append(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "component": "database",
                    "error": str(error),
                }
            )

    def log_server_start(self, host, port, debug=False):
        """Log server start"""
        total_time = round(time.time() - self.start_time, 3)

        self.logger.log_startup(
            event="server_started",
            host=host,
            port=port,
            debug=debug,
            total_startup_time=total_time,
            imports_count=len(self.imports),
            blueprints_count=len([b for b in self.blueprints if b["success"]]),
            models_count=len([m for m in self.models if m["success"]]),
            errors_count=len(self.errors),
            warnings_count=len(self.warnings),
        )

        # Write summary to file
        self._write_startup_summary(host, port, debug, total_time)

    def _write_startup_summary(self, host, port, debug, total_time):
        """Write startup summary to file"""
        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "server": {"host": host, "port": port, "debug": debug},
            "startup_time_seconds": total_time,
            "imports": {
                "total": len(self.imports),
                "successful": len([i for i in self.imports if i["success"]]),
                "failed": len([i for i in self.imports if not i["success"]]),
                "details": self.imports,
            },
            "blueprints": {
                "total": len(self.blueprints),
                "successful": len([b for b in self.blueprints if b["success"]]),
                "failed": len([b for b in self.blueprints if not b["success"]]),
                "details": self.blueprints,
            },
            "models": {
                "total": len(self.models),
                "successful": len([m for m in self.models if m["success"]]),
                "failed": len([m for m in self.models if not m["success"]]),
                "details": self.models,
            },
            "errors": self.errors,
            "warnings": self.warnings,
        }

        # Write to file
        log_dir = Path(__file__).parent.parent.parent / "logs" / "startup"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        summary_file = log_dir / f"startup_summary_{timestamp}.json"

        try:
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)

            self.logger.log_startup(event="summary_written", file=str(summary_file))
        except Exception as e:
            self.logger.log_error(error=f"Failed to write startup summary: {str(e)}")

    def get_summary(self):
        """Get startup summary"""
        return {
            "total_time": round(time.time() - self.start_time, 3),
            "imports": {
                "total": len(self.imports),
                "successful": len([i for i in self.imports if i["success"]]),
                "failed": len([i for i in self.imports if not i["success"]]),
            },
            "blueprints": {
                "total": len(self.blueprints),
                "successful": len([b for b in self.blueprints if b["success"]]),
                "failed": len([b for b in self.blueprints if not b["success"]]),
            },
            "models": {
                "total": len(self.models),
                "successful": len([m for m in self.models if m["success"]]),
                "failed": len([m for m in self.models if not m["success"]]),
            },
            "errors": len(self.errors),
            "warnings": len(self.warnings),
        }
