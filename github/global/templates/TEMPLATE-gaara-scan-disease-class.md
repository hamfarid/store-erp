# Template: Disease Class Definition (Gaara Scan)

> **Use For**: Adding new plant diseases to Gaara Scan AI

## Database Entry (disease_classes table)
```sql
INSERT INTO disease_classes (
    name, name_ar, description, treatment,
    favorable_temp_min, favorable_temp_max,
    favorable_humidity_min, favorable_humidity_max,
    min_images_for_training
) VALUES (
    '{disease_name_en}',
    '{disease_name_ar}',
    '{description}',
    '{treatment_description}',
    {temp_min}, {temp_max},
    {humidity_min}, {humidity_max},
    100  -- minimum images before training
);
```

## Crawler Queries (3 per disease)
```python
queries = [
    "{disease_name} plant disease leaf symptoms",
    "{disease_name} crop disease close up photo",
    "{disease_name_ar} النبات مرض أعراض",
]
```

## Checklist
- [ ] Disease entry in disease_classes table (EN + AR names)
- [ ] Treatment description documented
- [ ] Favorable environmental conditions (temp + humidity ranges)
- [ ] Crawler queries defined (3 minimum)
- [ ] Min 100 validated images collected
- [ ] YOLO model retrained with new class
- [ ] CNN model retrained with new class
- [ ] IoT alert rules configured for favorable conditions
