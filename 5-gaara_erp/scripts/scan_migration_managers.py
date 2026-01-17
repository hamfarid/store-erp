import os
import re


def main():
    opt_pat = re.compile(r"options\s*=\s*\{[\s\S]*?\}")
    mgr_pat = re.compile(r"managers\s*:\s*(\[[\s\S]*?\])")
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
                    # look for 'managers' occurrences
                    for m in re.finditer(r"managers\s*=|managers\s*:\s*", text):
                        line_no = text.count('\n', 0, m.start()) + 1
                        hits.append((path.replace('\\', '/'), line_no))
    if not hits:
        print('NO_MANAGERS_FOUND')
    else:
        for path, line in hits:
            print(f"{path}:{line}: contains 'managers' definition")


if __name__ == '__main__':
    main()
