import os, re


def main():
    patterns = [
        re.compile(r"\(\s*['\"]([^'\"]+)['\"]\s*,\s*models\.(\w+Field)\s*(?:,|\))"),
        re.compile(r"\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\w+Field)\s*(?:,|\))"),
    ]
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
                    for pat in patterns:
                        for m in pat.finditer(text):
                            line_no = text.count('\n', 0, m.start()) + 1
                            field_type = m.group(2)
                            # Heuristic: if immediately following token is '(', it's instantiated; skip
                            after = text[m.end(): m.end()+1]
                            if after == '(':
                                continue
                            bad.append((path.replace('\\','/'), line_no, m.group(1), field_type))
    if not bad:
        print('NO_BAD_FIELDS')
    else:
        for path, line, field_name, field_type in bad:
            print(f"{path}:{line}: field '{field_name}' uses {field_type} class without () in migration")


if __name__ == '__main__':
    main()

