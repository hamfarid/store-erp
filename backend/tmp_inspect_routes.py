from app import app

TARGETS = {"/api/auth/login", "/api/products", "/api/invoices"}

for rule in app.url_map.iter_rules():
    if rule.rule in TARGETS:
        vf = app.view_functions[rule.endpoint]
        print(
            rule.rule,
            rule.endpoint,
            sorted(rule.methods),
            getattr(vf, "__module__", None),
            getattr(vf, "__name__", None),
        )
