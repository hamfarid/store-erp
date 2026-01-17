import os, re


def main():
    pattern = re.compile(r"\(\s*['\"]([^'\"]+)['\"]\s*,\s*models\.(\w+Field)\s*,")
    bad = []
    for root, _, files in os.walk('.'):
        if root.endswith(os.path.sep + 'migrations') or (os.path.sep + 'migrations' + os.path.sep) in root:
            for fn in files:
                if fn.endswith('.py'):
                    path = os.path.join(root, fn)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            text = f.read()
                    except Exception:
                        continue
                    for m in pattern.finditer(text):
                        # crude filter: ignore if the preceding few chars include '(' which could indicate function call? We already check comma after class
                        line_no = text.count('\n', 0, m.start()) + 1
                        bad.append((path.replace('\\','/'), line_no, m.group(1), m.group(2)))
    if not bad:
        print('NO_BAD_FIELDS')
    else:
        for path, line, field_name, field_type in bad:
            print(f"{path}:{line}: field '{field_name}' uses {field_type} class without () in migration")


if __name__ == '__main__':
    main()

