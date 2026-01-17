import os
import re


def main():
    patterns = [
        re.compile(
            r"\(\s*['\"]([^'\"]+)['\"]\s*,\s*models\.Manager\s*(?:,|\))"),
        re.compile(r"\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\w+Manager)\s*(?:,|\))"),
    ]
    hits = []
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
                            # ensure not followed by '(' immediately after this token (instantiation)
                            after = text[m.end(): m.end()+1]
                            if after == '(':
                                continue
                            line_no = text.count('\n', 0, m.start()) + 1
                            hits.append(
                                (path.replace('\\', '/'), line_no, m.group(1)))
    if not hits:
        print('NO_BAD_MANAGERS')
    else:
        for path, line, name in hits:
            print(f"{path}:{line}: manager '{name}' declared without () in migration")


if __name__ == '__main__':
    main()
