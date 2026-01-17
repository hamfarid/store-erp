import traceback
import sys

try:
    import gaara_erp.agricultural_modules.farms.integration as m
    with open('.import_check.txt', 'w', encoding='utf-8') as f:
        f.write('OK ' + str(m.__file__))
except Exception:
    with open('.import_check.txt', 'w', encoding='utf-8') as f:
        f.write('ERR\n')
        traceback.print_exc(file=f)

