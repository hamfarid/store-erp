#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مراقب ملفات السجل
Log Monitor - Real-time log analysis and error detection
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class LogMonitor:
    def __init__(self, logs_dir="logs"):
        self.logs_dir = Path(logs_dir)
        self.analysis_report = {
            "timestamp": datetime.now().isoformat(),
            "log_files": {},
            "errors_found": [],
            "warnings_found": [],
            "statistics": {},
            "recommendations": []
        }

    def scan_logs(self):
        """فحص جميع ملفات السجل"""
        print("🔍 بدء فحص ملفات السجل...")

        if not self.logs_dir.exists():
            print("❌ مجلد logs غير موجود!")
            return

        log_files = list(self.logs_dir.glob("*.log"))
        print(f"📁 تم العثور على {len(log_files)} ملف سجل")

        for log_file in log_files:
            print(f"📄 فحص {log_file.name}...")
            self.analyze_log_file(log_file)

        self.generate_statistics()
        self.generate_recommendations()

    def analyze_log_file(self, log_file):
        """تحليل ملف سجل واحد"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            file_analysis = {
                "file_name": log_file.name,
                "total_lines": len(lines),
                "errors": 0,
                "warnings": 0,
                "info": 0,
                "last_entry": None,
                "first_entry": None
            }

            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue

                # تحديد نوع السجل
                if "ERROR" in line.upper() or "خطأ" in line:
                    file_analysis["errors"] += 1
                    self.analysis_report["errors_found"].append({
                        "file": log_file.name,
                        "line": i,
                        "content": line[:200]
                    })
                elif "WARNING" in line.upper() or "تحذير" in line:
                    file_analysis["warnings"] += 1
                    self.analysis_report["warnings_found"].append({
                        "file": log_file.name,
                        "line": i,
                        "content": line[:200]
                    })
                elif "INFO" in line.upper():
                    file_analysis["info"] += 1

                # تحديد أول وآخر إدخال
                if file_analysis["first_entry"] is None:
                    file_analysis["first_entry"] = line[:100]
                file_analysis["last_entry"] = line[:100]

            self.analysis_report["log_files"][log_file.name] = file_analysis

        except Exception as e:
            print(f"❌ خطأ في فحص {log_file.name}: {e}")

    def generate_statistics(self):
        """إنشاء إحصائيات شاملة"""
        stats = {
            "total_files": len(self.analysis_report["log_files"]),
            "total_errors": len(self.analysis_report["errors_found"]),
            "total_warnings": len(self.analysis_report["warnings_found"]),
            "files_with_errors": 0,
            "files_with_warnings": 0,
            "most_active_log": None,
            "error_rate": 0
        }

        max_lines = 0
        total_lines = 0

        for file_name, file_data in self.analysis_report["log_files"].items():
            total_lines += file_data["total_lines"]

            if file_data["errors"] > 0:
                stats["files_with_errors"] += 1

            if file_data["warnings"] > 0:
                stats["files_with_warnings"] += 1

            if file_data["total_lines"] > max_lines:
                max_lines = file_data["total_lines"]
                stats["most_active_log"] = file_name

        if total_lines > 0:
            stats["error_rate"] = (stats["total_errors"] / total_lines) * 100

        stats["total_log_entries"] = total_lines
        self.analysis_report["statistics"] = stats

    def generate_recommendations(self):
        """إنشاء توصيات للتحسين"""
        recommendations = []
        stats = self.analysis_report["statistics"]

        # توصيات بناءً على الأخطاء
        if stats["total_errors"] > 0:
            recommendations.append({
                "type": "error",
                "priority": "high",
                "message": f"تم العثور على {stats['total_errors']} خطأ في ملفات السجل",
                "action": "مراجعة الأخطاء وإصلاح المشاكل الأساسية"
            })

        # توصيات بناءً على التحذيرات
        if stats["total_warnings"] > 10:
            recommendations.append({
                "type": "warning",
                "priority": "medium",
                "message": f"عدد كبير من التحذيرات: {stats['total_warnings']}",
                "action": "مراجعة التحذيرات وتحسين الكود"
            })

        # توصيات بناءً على معدل الأخطاء
        if stats["error_rate"] > 5:
            recommendations.append({
                "type": "performance",
                "priority": "high",
                "message": f"معدل أخطاء مرتفع: {stats['error_rate']:.2f}%",
                "action": "تحسين معالجة الأخطاء في التطبيق"
            })

        # توصيات عامة
        if stats["total_files"] == 0:
            recommendations.append({
                "type": "setup",
                "priority": "medium",
                "message": "لا توجد ملفات سجل",
                "action": "التأكد من تفعيل نظام التسجيل"
            })

        self.analysis_report["recommendations"] = recommendations

    def save_report(self):
        """حفظ تقرير التحليل"""
        report_path = Path("log_analysis_report.json")

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_report, f, ensure_ascii=False, indent=2)

        print(f"📊 تم حفظ تقرير تحليل السجل في: {report_path}")

    def print_summary(self):
        """طباعة ملخص التحليل"""
        stats = self.analysis_report["statistics"]

        print("\n" + "="*60)
        print("📊 ملخص تحليل ملفات السجل")
        print("="*60)
        print(f"📁 إجمالي ملفات السجل: {stats['total_files']}")
        print(f"📝 إجمالي إدخالات السجل: {stats['total_log_entries']}")
        print(f"❌ إجمالي الأخطاء: {stats['total_errors']}")
        print(f"⚠️  إجمالي التحذيرات: {stats['total_warnings']}")
        print(f"📈 معدل الأخطاء: {stats['error_rate']:.2f}%")

        if stats["most_active_log"]:
            print(f"🔥 أكثر ملف نشاطاً: {stats['most_active_log']}")

        # طباعة الأخطاء الحديثة
        if self.analysis_report["errors_found"]:
            print(f"\n❌ آخر {min(5, len(self.analysis_report['errors_found']))} أخطاء:")
            for error in self.analysis_report["errors_found"][-5:]:
                print(f"   📄 {error['file']}:{error['line']} - {error['content'][:80]}...")

        # طباعة التوصيات
        if self.analysis_report["recommendations"]:
            print("\n💡 التوصيات:")
            for rec in self.analysis_report["recommendations"]:
                priority_icon = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
                print(f"   {priority_icon} {rec['message']}")
                print(f"      👉 {rec['action']}")


def main():
    monitor = LogMonitor()

    print("🔍 مراقب ملفات السجل")
    print("="*40)

    monitor.scan_logs()
    monitor.save_report()
    monitor.print_summary()

    print("\n✅ تم الانتهاء من تحليل ملفات السجل!")


if __name__ == "__main__":
    main()
