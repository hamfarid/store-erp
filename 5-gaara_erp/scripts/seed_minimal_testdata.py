from __future__ import annotations

# Idempotent minimal test data seeder using apps.get_model to avoid import path issues.
# Usage: APP_MODE=test DJANGO_SETTINGS_MODULE=gaara_erp.settings \
#        .venv/Scripts/python gaara_erp/manage.py shell -c "exec(open('scripts/seed_minimal_testdata.py','rb').read())"

from django.apps import apps
from django.db import transaction
from django.utils import timezone


def _field_names(model):
    return {f.name for f in model._meta.get_fields() if getattr(f, "concrete", False) and not getattr(f, "many_to_many", False)}


def _safe_create_or_get(model_label: str, lookup: dict, defaults: dict | None = None):
    Model = apps.get_model(*model_label.split("."))  # e.g., "companies.Company" -> ("companies","Company")
    fields = _field_names(Model)
    lookup_f = {k: v for k, v in (lookup or {}).items() if k in fields}
    defaults_f = {k: v for k, v in (defaults or {}).items() if k in fields}
    obj, _ = Model.objects.get_or_create(**lookup_f, defaults=defaults_f)
    return obj


@transaction.atomic
def run():
    # Core org/companies
    region = _safe_create_or_get(
        "companies.Region",
        lookup={"code": "MEA"},
        defaults={"name": "Middle East & Africa"},
    )
    country = _safe_create_or_get(
        "companies.Country",
        lookup={"code": "AE"},
        defaults={"name": "United Arab Emirates", "region": region},
    )
    company = _safe_create_or_get(
        "companies.Company",
        lookup={"name": "Gaara Test Co"},
        defaults={"code": "GAARA", "country": country},
    )
    branch = _safe_create_or_get(
        "companies.Branch",
        lookup={"company": company, "name": "HQ"},
        defaults={"code": "HQ"},
    )
    _safe_create_or_get(
        "companies.Department",
        lookup={"company": company, "name": "IT"},
        defaults={"code": "IT", "branch": branch},
    )

    # Farms basics
    Farm = apps.get_model("farms", "Farm")
    Section = apps.get_model("farms", "Section") if apps.is_installed("farms") else None
    Plot = apps.get_model("farms", "Plot") if apps.is_installed("farms") else None
    Crop = apps.get_model("farms", "Crop") if apps.is_installed("farms") else None
    CropVariety = apps.get_model("farms", "CropVariety") if apps.is_installed("farms") else None
    Planting = apps.get_model("farms", "Planting") if apps.is_installed("farms") else None

    farm = _safe_create_or_get(
        "farms.Farm",
        lookup={"code": "TFARM"},
        defaults={
            "name": "Test Farm",
            "location": "Test Location",
            "gps_coordinates": "25.2048,55.2708",
            "total_area": 100,
            "cultivated_area": 25,
            "farm_type": "mixed",
            "description": "Seeded by script",
            "establishment_date": timezone.now().date(),
            "is_active": True,
        },
    )
    if Section:
        section = _safe_create_or_get(
            "farms.Section", lookup={"farm": farm, "code": "SEC-A"}, defaults={"name": "Section A"}
        )
    else:
        section = None
    if Plot:
        plot = _safe_create_or_get(
            "farms.Plot", lookup={"farm": farm, "name": "Plot 1"}, defaults={"section": section, "area": 1.5}
        )
    else:
        plot = None
    if Crop:
        crop = _safe_create_or_get("farms.Crop", lookup={"name": "Wheat"}, defaults={"crop_type": "grain"})
    else:
        crop = None
    if CropVariety and crop:
        variety = _safe_create_or_get(
            "farms.CropVariety", lookup={"crop": crop, "code": "DW"}, defaults={"name": "Durum Wheat"}
        )
    else:
        variety = None
    if Planting and plot and variety:
        _safe_create_or_get(
            "farms.Planting",
            lookup={"plot": plot, "crop_variety": variety, "planting_date": timezone.now().date()},
            defaults={},
        )

    # AI basic integration (optional)
    if apps.is_installed("ai"):
        try:
            integration = _safe_create_or_get(
                "ai.AIIntegration",
                lookup={"name": "Default Vector DB"},
                defaults={"status": "active"},
            )
            _safe_create_or_get(
                "ai.AIModel",
                lookup={"name": "ai-mini"},
                defaults={"provider": "local", "status": "active", "integration": integration},
            )
        except Exception:
            # tolerate absence of these models/fields
            pass

    print("Seeded minimal test data.")


if __name__ == "__main__":
    run()

