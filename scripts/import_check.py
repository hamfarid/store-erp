import sys
try:
    import flask, jwt, sqlalchemy
    print('OK', flask.__version__, getattr(jwt, '__spec__', None).name if getattr(jwt, '__spec__', None) else 'jwt', sqlalchemy.__version__, sys.executable)
except Exception as e:
    print('ERR', repr(e))
    raise

