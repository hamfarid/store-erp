#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فاحص الأزرار الشامل
Button Scanner - Comprehensive Button Analysis
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime


class ButtonScanner:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.scan_report = {
            "timestamp": datetime.now().isoformat(),
            "buttons_found": [],
            "components_scanned": [],
            "button_types": {},
            "event_handlers": [],
            "summary": {}
        }

        # أنماط البحث عن الأزرار
        self.button_patterns = [
            # React/JSX buttons
            r'<button[^>]*onClick\s*=\s*{([^}]+)}[^>]*>([^<]*)</button>',
            r'<button[^>]*onClick\s*=\s*{([^}]+)}[^>]*>',
            r'onClick\s*=\s*{([^}]+)}',
            r'onSubmit\s*=\s*{([^}]+)}',
            r'onPress\s*=\s*{([^}]+)}',
            r'onTap\s*=\s*{([^}]+)}',

            # HTML buttons
            r'<button[^>]*onclick\s*=\s*["\']([^"\']+)["\'][^>]*>([^<]*)</button>',
            r'<input[^>]*type\s*=\s*["\']button["\'][^>]*onclick\s*=\s*["\']([^"\']+)["\']',
            r'<input[^>]*type\s*=\s*["\']submit["\'][^>]*>',

            # Event handlers
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',
            r'function\s+(\w+)\s*\([^)]*\)\s*{',
            r'const\s+(\w+)\s*=\s*async\s*\([^)]*\)\s*=>\s*{',
            r'async\s+function\s+(\w+)\s*\([^)]*\)\s*{',

            # مكونات أزرار مخصصة
            r'<(\w*Button\w*)[^>]*>',
            r'<(\w*Btn\w*)[^>]*>',
        ]

    def scan_file(self, file_path):
        """فحص ملف واحد للبحث عن الأزرار"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            file_buttons = []
            relative_path = str(file_path.relative_to(self.project_root))

            for pattern in self.button_patterns:
                matches = re.finditer(pattern,
                    content,
                    re.MULTILINE | re.DOTALL)
                for match in matches:
                    button_info = {
                        "file": relative_path,
                        "line": content[:match.start()].count('\n') + 1,
                        "pattern": pattern,
                        "match": match.group(0)[:200],  # أول 200 حرف
                        "handler": match.group(1) if match.groups() else None,
                        "text": match.group(2) if len(match.groups()) > 1 else None
                    }
                    file_buttons.append(button_info)

            return file_buttons

        except Exception as e:
            print(f"خطأ في فحص الملف {file_path}: {e}")
            return []

    def scan_project(self):
        """فحص المشروع بالكامل"""
        print("🔍 بدء فحص الأزرار في المشروع...")

        # الملفات المراد فحصها
        file_extensions = ['.jsx', '.js', '.tsx', '.ts', '.html', '.vue']

        scanned_files = 0
        total_buttons = 0

        for root, dirs, files in os.walk(self.project_root):
            # تجاهل مجلدات معينة
            dirs[:] = [d for d in dirs if d not in ['node_modules',
                'unneeded',
                '.git',
                'dist',
                'build']]

            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    file_path = Path(root) / file
                    relative_path = str(file_path.relative_to(self.project_root))

                    self.scan_report["components_scanned"].append(relative_path)
                    scanned_files += 1

                    buttons = self.scan_file(file_path)
                    if buttons:
                        self.scan_report["buttons_found"].extend(buttons)
                        total_buttons += len(buttons)
                        print(f"📁 {relative_path}: {len(buttons)} أزرار")

        print(f"\n✅ تم فحص {scanned_files} ملف")
        print(f"🔘 تم العثور على {total_buttons} زر")

    def analyze_buttons(self):
        """تحليل الأزرار المكتشفة"""
        print("\n📊 تحليل الأزرار...")

        # تصنيف الأزرار حسب النوع
        button_types = {}
        event_handlers = set()

        for button in self.scan_report["buttons_found"]:
            # تصنيف حسب نوع الملف
            file_ext = Path(button["file"]).suffix
            if file_ext not in button_types:
                button_types[file_ext] = 0
            button_types[file_ext] += 1

            # جمع معالجات الأحداث
            if button["handler"]:
                event_handlers.add(button["handler"])

        self.scan_report["button_types"] = button_types
        self.scan_report["event_handlers"] = list(event_handlers)

        # إحصائيات
        self.scan_report["summary"] = {
            "total_files_scanned": len(self.scan_report["components_scanned"]),
            "total_buttons_found": len(self.scan_report["buttons_found"]),
            "unique_handlers": len(event_handlers),
            "button_types_count": len(button_types)
        }

    def find_common_patterns(self):
        """البحث عن الأنماط الشائعة"""
        print("\n🔍 البحث عن الأنماط الشائعة...")

        common_handlers = {}
        common_texts = {}

        for button in self.scan_report["buttons_found"]:
            # معالجات شائعة
            if button["handler"]:
                handler = button["handler"].strip()
                if handler in common_handlers:
                    common_handlers[handler] += 1
                else:
                    common_handlers[handler] = 1

            # نصوص شائعة
            if button["text"]:
                text = button["text"].strip()
                if text in common_texts:
                    common_texts[text] += 1
                else:
                    common_texts[text] = 1

        # أكثر 10 معالجات شيوعاً
        top_handlers = sorted(common_handlers.items(),
            key=lambda x: x[1],
            reverse=True)[:10]
        top_texts = sorted(common_texts.items(),
            key=lambda x: x[1],
            reverse=True)[:10]

        self.scan_report["common_patterns"] = {
            "top_handlers": top_handlers,
            "top_texts": top_texts
        }

        print("🔥 أكثر المعالجات شيوعاً:")
        for handler, count in top_handlers:
            print(f"   {handler}: {count} مرة")

    def generate_report(self):
        """إنشاء تقرير شامل"""
        report_path = self.project_root / "button_scan_report.json"

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.scan_report, f, ensure_ascii=False, indent=2)

        print(f"\n📊 تم حفظ تقرير فحص الأزرار في: {report_path}")

        # طباعة ملخص
        print("\n" + "="*50)
        print("📊 ملخص فحص الأزرار")
        print("="*50)
        print(f"📁 ملفات تم فحصها: {self.scan_report['summary']['total_files_scanned']}")
        print(f"🔘 أزرار تم العثور عليها: {self.scan_report['summary']['total_buttons_found']}")
        print(f"⚡ معالجات فريدة: {self.scan_report['summary']['unique_handlers']}")
        print(f"📊 أنواع أزرار: {self.scan_report['summary']['button_types_count']}")

        print("\n📈 توزيع الأزرار حسب نوع الملف:")
        for file_type, count in self.scan_report["button_types"].items():
            print(f"   {file_type}: {count} زر")

    def create_button_inventory(self):
        """إنشاء جرد شامل للأزرار"""
        inventory = {}

        for button in self.scan_report["buttons_found"]:
            file_path = button["file"]
            if file_path not in inventory:
                inventory[file_path] = []

            inventory[file_path].append({
                "line": button["line"],
                "handler": button["handler"],
                "text": button["text"],
                "type": self._classify_button(button)
            })

        # حفظ الجرد
        inventory_path = self.project_root / "button_inventory.json"
        with open(inventory_path, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, ensure_ascii=False, indent=2)

        print(f"📋 تم حفظ جرد الأزرار في: {inventory_path}")

    def _classify_button(self, button):
        """تصنيف نوع الزر"""
        match = button["match"].lower()
        handler = button["handler"] or ""

        if "submit" in match or "onsubmit" in handler.lower():
            return "submit"
        elif "delete" in handler.lower() or "remove" in handler.lower():
            return "delete"
        elif "save" in handler.lower() or "create" in handler.lower():
            return "save"
        elif "edit" in handler.lower() or "update" in handler.lower():
            return "edit"
        elif "cancel" in handler.lower() or "close" in handler.lower():
            return "cancel"
        elif "export" in handler.lower():
            return "export"
        elif "import" in handler.lower():
            return "import"
        elif "navigate" in handler.lower() or "goto" in handler.lower():
            return "navigation"
        else:
            return "general"


def main():
    project_root = Path(__file__).parent
    scanner = ButtonScanner(project_root)

    print("🔍 فاحص الأزرار الشامل")
    print("="*40)

    # فحص المشروع
    scanner.scan_project()

    # تحليل النتائج
    scanner.analyze_buttons()

    # البحث عن الأنماط
    scanner.find_common_patterns()

    # إنشاء التقارير
    scanner.generate_report()
    scanner.create_button_inventory()

    print("\n🎉 تم الانتهاء من فحص الأزرار!")


if __name__ == "__main__":
    main()
