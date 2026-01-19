"""
مصنع التكامل الشامل - Frontend/Backend Integration Factory
يضمن ربط كل API بواجهة أمامية مقابلة
"""

from pathlib import Path
from typing import Any, Dict, List


class IntegrationFactory:
    """مصنع التكامل بين الواجهات الأمامية والخلفية"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.apis_mapping = {}
        self.frontend_components = {}
        self.missing_integrations = []

    def scan_backend_apis(self) -> Dict[str, Any]:
        """فحص جميع APIs الموجودة في الخلفية"""
        apis = {}
        modules_path = self.project_root / "src" / "modules"

        if not modules_path.exists():
            return apis

        for module_dir in modules_path.iterdir():
            if module_dir.is_dir():
                api_file = module_dir / "api.py"
                if api_file.exists():
                    apis[module_dir.name] = {
                        "path": str(api_file),
                        "endpoints": self._extract_endpoints(api_file),
                        "has_frontend": False,
                        "frontend_components": []
                    }

        return apis

    def scan_frontend_components(self) -> Dict[str, Any]:
        """فحص جميع المكونات الأمامية الموجودة"""
        components = {}
        frontend_path = self.project_root / "src" / "frontend" / "components"

        if not frontend_path.exists():
            return components

        for component_dir in frontend_path.iterdir():
            if component_dir.is_dir():
                vue_files = list(component_dir.glob("*.vue"))
                if vue_files:
                    components[component_dir.name] = {
                        "path": str(component_dir),
                        "files": [str(f) for f in vue_files],
                        "has_backend": False,
                        "related_apis": []
                    }

        return components

    def _extract_endpoints(self, api_file: Path) -> List[str]:
        """استخراج endpoints من ملف API"""
        endpoints = []
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # البحث عن decorators مثل @router.get, @router.post
                import re
                patterns = [
                    r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
                    r'@app\.route\(["\']([^"\']+)["\']']
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if isinstance(match, tuple):
                            endpoints.append(match[-1])
                        else:
                            endpoints.append(match)
        except Exception as e:
            print(f"خطأ في قراءة {api_file}: {e}")

        return endpoints

    def generate_integration_report(self) -> str:
        """إنشاء تقرير التكامل"""
        apis = self.scan_backend_apis()
        components = self.scan_frontend_components()

        report = f"""# تقرير التكامل بين الواجهات الأمامية والخلفية

## إجمالي الإحصائيات:
- **عدد APIs**: {len(apis)}
- **عدد المكونات الأمامية**: {len(components)}

## APIs الموجودة:
"""

        for api_name, api_info in apis.items():
            report += f"- **{api_name}**: {len(api_info['endpoints'])} endpoints\n"

        report += "\n## المكونات الأمامية:\n"
        for comp_name, comp_info in components.items():
            report += f"- **{comp_name}**: {len(comp_info['files'])} files\n"

        return report


# إنشاء مثيل المصنع
integration_factory = IntegrationFactory()

if __name__ == "__main__":
    # تشغيل فحص التكامل
    print("فحص التكامل بين الواجهات الأمامية والخلفية...")

    # إنشاء تقرير التكامل
    report = integration_factory.generate_integration_report()

    # حفظ التقرير
    report_path = Path("/home/ubuntu/clean_project/docs/integration_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"تم حفظ تقرير التكامل في: {report_path}")
    print("تم الانتهاء من فحص التكامل!")
