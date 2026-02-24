import sys
print('PY', sys.executable)
try:
    import flask
    print('FLASK', flask.__version__)
except Exception as e:
    print('FLASK_IMPORT_ERROR', repr(e))

try:
    sys.path.append('backend')
    from app import create_app
    app = create_app()
    print('APP_OK')
except Exception as e:
    print('APP_ERROR', repr(e))

