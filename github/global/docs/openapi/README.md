# OpenAPI (Swagger) Bootstrap

This repository uses flask-smorest + apispec + marshmallow to generate OpenAPI 3.0 documentation and serve Swagger UI.

Quick start
- UI: GET /api/docs
- Spec JSON: GET /api/openapi.json

How it works
- main.py initializes Api(app) when flask-smorest is available
- A demo blueprint is provided at src/routes/openapi_demo.py and is registered into Api
- The demo endpoint is /api/docs-demo/ping

Add a documented endpoint
1) Create or update a smorest Blueprint
2) Prefer class-based views with MethodView
3) Define request/response schemas with marshmallow
4) Register the blueprint into Api(app) (see main.py)

Example

```python
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

blp = Blueprint('items', __name__, description='Item APIs')

class ItemSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

@blp.route('/items')
class ItemsView(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return [{'id': 1, 'name': 'foo'}]
```

Notes
- In dev environments lacking flask-smorest, OpenAPI tests are skipped
- Keep decorators on methods (get/post/put/delete) to ensure paths/schemas are generated

