# __init__.py Patterns - أمثلة عملية

هذا المجلد يحتوي على أمثلة عملية لأنماط مختلفة من ملفات `__init__.py`.

## الأمثلة المتوفرة

### 1. Central Registry Pattern
**المجلد:** `01_central_registry/`

**الاستخدام:**
```python
from examples.init_py_patterns.01_central_registry import (
    Status,
    UserRole,
    APIResponse,
    TimestampMixin
)

# Use the definitions
user_status = Status.ACTIVE
user_role = UserRole.ADMIN
```

**متى تستخدمه:**
- عندما تريد مكان مركزي لجميع التعريفات
- في packages الـ config
- لتبسيط الـ imports

**الإيجابيات:**
- ✅ واجهة واضحة ونظيفة
- ✅ سهل الاستخدام
- ✅ منظم جيداً

---

### 2. Lazy Loading Pattern
**المجلد:** `02_lazy_loading/`

**الاستخدام:**
```python
from examples.init_py_patterns.02_lazy_loading import get_analyzer

# Module is imported only when you call this
analyzer = get_analyzer()
results = analyzer.analyze('/path/to/code')
```

**أو باستخدام __getattr__:**
```python
from examples.init_py_patterns.02_lazy_loading import CodeAnalyzer

# Module is imported on first access
analyzer = CodeAnalyzer()
```

**متى تستخدمه:**
- عندما يكون لديك modules ثقيلة
- في CLI tools
- عندما تريد تحسين startup time

**الإيجابيات:**
- ✅ يحسن الأداء بشكل كبير
- ✅ يقلل memory footprint
- ✅ مناسب للـ large applications

**قياس الأداء:**
```bash
# Without lazy loading
$ time python -c "import heavy_package"
real    0m0.500s

# With lazy loading
$ time python -c "import heavy_package"
real    0m0.050s
```

---

### 3. Plugin System Pattern
**المجلد:** `03_plugin_system/`

**الاستخدام:**
```python
from examples.init_py_patterns.03_plugin_system import (
    discover_plugins,
    get_plugin,
    list_plugins
)

# Discover all plugins
discover_plugins()

# List available plugins
plugins = list_plugins()
print(f"Available plugins: {plugins}")

# Get specific plugin
ExamplePlugin = get_plugin('example')
plugin = ExamplePlugin()
plugin.initialize()
result = plugin.execute(arg1="value1")
```

**متى تستخدمه:**
- عندما تريد extensible architecture
- للـ plugin systems
- عندما تريد auto-discovery

**الإيجابيات:**
- ✅ مرن وقابل للتوسع
- ✅ auto-discovery تلقائي
- ✅ سهل إضافة plugins جديدة

**كيفية إنشاء plugin جديد:**
```python
# my_plugin.py
class MyPlugin:
    name = "my_plugin"
    version = "1.0.0"
    
    def initialize(self):
        pass
    
    def execute(self, *args, **kwargs):
        return "My plugin result"

def register_plugin():
    return MyPlugin
```

---

## اختبار الأمثلة

### Test Pattern 1: Central Registry
```bash
cd /path/to/global
python3 -c "
from examples.init_py_patterns.01_central_registry import Status, UserRole
print(f'Status.ACTIVE = {Status.ACTIVE}')
print(f'UserRole.ADMIN = {UserRole.ADMIN}')
"
```

### Test Pattern 2: Lazy Loading
```bash
python3 -c "
from examples.init_py_patterns.02_lazy_loading import get_analyzer
analyzer = get_analyzer()
print(f'Analyzer: {analyzer}')
"
```

### Test Pattern 3: Plugin System
```bash
python3 -c "
from examples.init_py_patterns.03_plugin_system import discover_plugins, list_plugins
discover_plugins()
print(f'Plugins: {list_plugins()}')
"
```

---

## مقارنة الأنماط

| النمط | الأداء | التعقيد | الاستخدام الأمثل |
|-------|--------|---------|------------------|
| **Central Registry** | ⭐⭐⭐ | ⭐ | Config packages |
| **Lazy Loading** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | CLI tools, heavy modules |
| **Plugin System** | ⭐⭐⭐ | ⭐⭐⭐⭐ | Extensible apps |

---

## أفضل الممارسات

### 1. اختر النمط المناسب
- **Small packages** → Central Registry
- **Performance-critical** → Lazy Loading
- **Extensible apps** → Plugin System

### 2. وثق الاستخدام
- أضف docstrings واضحة
- أضف أمثلة في الـ docstring
- اشرح متى يُستخدم النمط

### 3. اختبر الأداء
```python
import time

start = time.time()
import your_package
end = time.time()

print(f"Import time: {(end - start) * 1000:.2f}ms")
```

### 4. استخدم Type Hints
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .heavy_module import HeavyClass
```

---

## المراجع

- [PEP 420 - Implicit Namespace Packages](https://peps.python.org/pep-0420/)
- [Python Import System](https://docs.python.org/3/reference/import.html)
- [Lazy Imports in Python](https://docs.python.org/3/whatsnew/3.7.html#pep-562-customization-of-access-to-module-attributes)

---

## الخلاصة

هذه الأمثلة توضح **3 أنماط أساسية** لملفات `__init__.py`:

1. ✅ **Central Registry** - للتنظيم والوضوح
2. ✅ **Lazy Loading** - للأداء
3. ✅ **Plugin System** - للمرونة

اختر النمط المناسب حسب احتياجات مشروعك!

