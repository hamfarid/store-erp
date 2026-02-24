import sys
print('PY', sys.executable)
try:
    import chromadb
    print('CHROMADB_OK', getattr(chromadb, '__version__', '?'))
except Exception as e:
    print('CHROMADB_ERROR', repr(e))

try:
    from sentence_transformers import SentenceTransformer
    print('ST_OK', SentenceTransformer)
except Exception as e:
    print('ST_ERROR', repr(e))

