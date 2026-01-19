"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/code_quality/code_validator.py
الوصف: أداة للتحقق من جودة الكود وتنظيفه
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import json
import logging
import os
import re
import subprocess
from datetime import datetime
from typing import Any, Dict

# Constants
FILE_DOC_REQUIRED = 'يجب إضافة توثيق الملف'

# إعداد المسجل
logger = logging.getLogger(__name__)


class CodeValidator:
    """
    أداة للتحقق من جودة الكود وتنظيفه
    """

    def __init__(self, project_root: str):
        """
        تهيئة مدقق الكود

        Args:
            project_root: المسار الجذر للمشروع
        """
        self.project_root = project_root
        self.python_files = []
        self.js_files = []
        self.vue_files = []
        self.issues = []

    def scan_project(self) -> None:
        """
        مسح المشروع للعثور على ملفات الكود
        """
        logger.info(f"بدء مسح المشروع في {self.project_root}")

        for root, _, files in os.walk(self.project_root):
            # تجاهل المجلدات المخفية والمجلدات الخاصة
            if '/.' in root or '/__pycache__' in root or '/node_modules' in root or '/venv' in root:
                continue

            for file in files:
                file_path = os.path.join(root, file)

                if file.endswith('.py'):
                    self.python_files.append(file_path)
                elif file.endswith('.js') and not file.endswith('.min.js'):
                    self.js_files.append(file_path)
                elif file.endswith('.vue'):
                    self.vue_files.append(file_path)

        logger.info(
            f"تم العثور على {len(self.python_files)} ملف Python، {len(self.js_files)} ملف JavaScript، {len(self.vue_files)} ملف Vue")

    def validate_python_files(self) -> None:
        """
        التحقق من جودة ملفات Python
        """
        logger.info("بدء التحقق من جودة ملفات Python")

        for file_path in self.python_files:
            # التحقق من وجود توثيق الملف
            self._check_file_documentation(file_path, 'python')

            # التحقق من وجود توثيق الدوال والفئات
            self._check_function_documentation(file_path)

            # تشغيل flake8 للتحقق من الأخطاء
            self._run_flake8(file_path)

            # تشغيل pylint للتحقق من جودة الكود
            self._run_pylint(file_path)

    def validate_js_files(self) -> None:
        """
        التحقق من جودة ملفات JavaScript
        """
        logger.info("بدء التحقق من جودة ملفات JavaScript")

        for file_path in self.js_files:
            # التحقق من وجود توثيق الملف
            self._check_file_documentation(file_path, 'javascript')

            # التحقق من وجود توثيق الدوال
            self._check_js_function_documentation(file_path)

            # تشغيل ESLint للتحقق من الأخطاء
            self._run_eslint(file_path)

    def validate_vue_files(self) -> None:
        """
        التحقق من جودة ملفات Vue
        """
        logger.info("بدء التحقق من جودة ملفات Vue")

        for file_path in self.vue_files:
            # التحقق من وجود توثيق الملف
            self._check_file_documentation(file_path, 'vue')

            # التحقق من وجود توثيق المكونات
            self._check_vue_component_documentation(file_path)

            # تشغيل ESLint للتحقق من الأخطاء
            self._run_eslint(file_path)

    def _check_file_documentation(
            self,
            file_path: str,
            file_type: str) -> None:
        """
        التحقق من وجود توثيق الملف

        Args:
            file_path: مسار الملف
            file_type: نوع الملف (python, javascript, vue)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        relative_path = os.path.relpath(file_path, self.project_root)

        if file_type == 'python':
            # البحث عن توثيق الملف في بداية الملف
            if not re.search(
                    r'"""[\s\S]*?مسار الملف[\s\S]*?"""',
                    content) and not re.search(
                    r'"""[\s\S]*?File path[\s\S]*?"""',
                    content):
                self.issues.append({
                    'file': relative_path,
                    'type': 'missing_file_documentation',
                    'line': 1,
                    'message': FILE_DOC_REQUIRED
                })
        elif file_type == 'javascript':
            # البحث عن توثيق الملف في بداية الملف
            if not re.search(
                    r'/\*\*[\s\S]*?مسار الملف[\s\S]*?\*/',
                    content) and not re.search(
                    r'/\*\*[\s\S]*?File path[\s\S]*?\*/',
                    content):
                self.issues.append({
                    'file': relative_path,
                    'type': 'missing_file_documentation',
                    'line': 1,
                    'message': FILE_DOC_REQUIRED
                })
        elif file_type == 'vue':
            # البحث عن توثيق الملف في بداية الملف
            if not re.search(
                    r'<!--[\s\S]*?مسار الملف[\s\S]*?-->',
                    content) and not re.search(
                    r'<!--[\s\S]*?File path[\s\S]*?-->',
                    content):
                self.issues.append({
                    'file': relative_path,
                    'type': 'missing_file_documentation',
                    'line': 1,
                    'message': FILE_DOC_REQUIRED
                })

    def _check_function_documentation(self, file_path: str) -> None:
        """
        التحقق من وجود توثيق الدوال والفئات في ملفات Python

        Args:
            file_path: مسار الملف
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()

        relative_path = os.path.relpath(file_path, self.project_root)

        # البحث عن تعريفات الدوال والفئات
        function_pattern = re.compile(r'^\s*def\s+(\w+)\s*\(')
        class_pattern = re.compile(r'^\s*class\s+(\w+)')

        for i, line in enumerate(content):
            # البحث عن تعريفات الدوال
            function_match = function_pattern.match(line)
            if function_match:
                function_name = function_match.group(1)

                # تجاهل الدوال الخاصة
                if function_name.startswith(
                        '_') and not function_name.startswith('__'):
                    continue

                # التحقق من وجود توثيق الدالة
                if i > 0 and '"""' not in content[i -
                                                  1] and '"""' not in content[i + 1]:
                    self.issues.append({
                        'file': relative_path,
                        'type': 'missing_function_documentation',
                        'line': i + 1,
                        'message': f'يجب إضافة توثيق للدالة {function_name}'
                    })

            # البحث عن تعريفات الفئات
            class_match = class_pattern.match(line)
            if class_match:
                class_name = class_match.group(1)

                # التحقق من وجود توثيق الفئة
                if i > 0 and '"""' not in content[i -
                                                  1] and '"""' not in content[i + 1]:
                    self.issues.append({
                        'file': relative_path,
                        'type': 'missing_class_documentation',
                        'line': i + 1,
                        'message': f'يجب إضافة توثيق للفئة {class_name}'
                    })

    def _check_js_function_documentation(self, file_path: str) -> None:
        """
        التحقق من وجود توثيق الدوال في ملفات JavaScript

        Args:
            file_path: مسار الملف
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()

        relative_path = os.path.relpath(file_path, self.project_root)

        # البحث عن تعريفات الدوال
        function_patterns = [
            re.compile(r'^\s*function\s+(\w+)\s*\('),
            re.compile(r'^\s*const\s+(\w+)\s*=\s*function'),
            re.compile(r'^\s*const\s+(\w+)\s*=\s*\('),
            re.compile(r'^\s*(\w+)\s*:\s*function')
        ]

        for i, line in enumerate(content):
            for pattern in function_patterns:
                match = pattern.match(line)
                if match:
                    function_name = match.group(1)

                    # تجاهل الدوال الخاصة
                    if function_name.startswith('_'):
                        continue

                    # التحقق من وجود توثيق الدالة
                    if i > 0 and '/**' not in content[i -
                                                      1] and '*/' not in content[i - 1]:
                        self.issues.append({
                            'file': relative_path,
                            'type': 'missing_function_documentation',
                            'line': i + 1,
                            'message': f'يجب إضافة توثيق للدالة {function_name}'
                        })

    def _check_vue_component_documentation(self, file_path: str) -> None:
        """
        التحقق من وجود توثيق المكونات في ملفات Vue

        Args:
            file_path: مسار الملف
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        relative_path = os.path.relpath(file_path, self.project_root)

        # البحث عن تعريف المكون
        component_match = re.search(
            r'export\s+default\s*{[\s\S]*?name\s*:\s*[\'"](\w+)[\'"]', content)
        if component_match:
            component_name = component_match.group(1)

            # البحث عن توثيق المكون
            if not re.search(
                    r'/\*\*[\s\S]*?@component[\s\S]*?\*/',
                    content) and not re.search(
                    r'<!--[\s\S]*?@component[\s\S]*?-->',
                    content):
                self.issues.append({
                    'file': relative_path,
                    'type': 'missing_component_documentation',
                    'line': 1,
                    'message': f'يجب إضافة توثيق للمكون {component_name}'
                })

        # البحث عن تعريفات الدوال في قسم الـ script
        script_match = re.search(r'<script>[\s\S]*?</script>', content)
        if script_match:
            script_content = script_match.group(0)

            # البحث عن تعريفات الدوال
            function_matches = re.finditer(
                r'(\w+)\s*\([^)]*\)\s*{', script_content)
            for match in function_matches:
                function_name = match.group(1)

                # تجاهل الدوال الخاصة
                if function_name.startswith('_') or function_name in [
                    'data',
                    'created',
                    'mounted',
                    'beforeDestroy',
                    'destroyed',
                    'beforeUpdate',
                        'updated']:
                    continue

                # التحقق من وجود توثيق الدالة
                if not re.search(
                    r'/\*\*[\s\S]*?' +
                    function_name +
                    r'[\s\S]*?\*/',
                        script_content):
                    self.issues.append({
                        'file': relative_path,
                        'type': 'missing_method_documentation',
                        'line': 0,  # لا يمكن تحديد رقم السطر بدقة
                        'message': f'يجب إضافة توثيق للدالة {function_name} في المكون'
                    })

    def _run_flake8(self, file_path: str) -> None:
        """
        تشغيل flake8 للتحقق من الأخطاء في ملفات Python

        Args:
            file_path: مسار الملف
        """
        try:
            result = subprocess.run(
                ['flake8', file_path], capture_output=True, text=True)

            if result.returncode != 0:
                relative_path = os.path.relpath(file_path, self.project_root)

                for line in result.stdout.splitlines():
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        line_num = int(parts[1])
                        error_code = parts[3].strip().split(' ')[0]
                        error_message = parts[3].strip()

                        self.issues.append({
                            'file': relative_path,
                            'type': 'flake8_error',
                            'line': line_num,
                            'code': error_code,
                            'message': error_message
                        })
        except Exception as e:
            logger.error(f"خطأ في تشغيل flake8: {str(e)}")

    def _run_pylint(self, file_path: str) -> None:
        """
        تشغيل pylint للتحقق من جودة الكود في ملفات Python

        Args:
            file_path: مسار الملف
        """
        try:
            result = subprocess.run(
                ['pylint', '--output-format=json', file_path], capture_output=True, text=True)

            if result.stdout:
                try:
                    pylint_issues = json.loads(result.stdout)
                    relative_path = os.path.relpath(
                        file_path, self.project_root)

                    for issue in pylint_issues:
                        # تجاهل التحذيرات الطفيفة
                        if issue['type'] in ['convention', 'refactor']:
                            continue

                        self.issues.append({
                            'file': relative_path,
                            'type': 'pylint_' + issue['type'],
                            'line': issue['line'],
                            'code': issue['symbol'],
                            'message': issue['message']
                        })
                except json.JSONDecodeError:
                    logger.warning(
                        f"تعذر تحليل مخرجات pylint لملف {file_path}")
        except Exception as e:
            logger.error(f"خطأ في تشغيل pylint: {str(e)}")

    def _run_eslint(self, file_path: str) -> None:
        """
        تشغيل ESLint للتحقق من الأخطاء في ملفات JavaScript و Vue

        Args:
            file_path: مسار الملف
        """
        try:
            result = subprocess.run(
                ['eslint', '--format=json', file_path], capture_output=True, text=True)

            if result.stdout:
                try:
                    eslint_issues = json.loads(result.stdout)
                    relative_path = os.path.relpath(
                        file_path, self.project_root)

                    for file_result in eslint_issues:
                        for message in file_result.get('messages', []):
                            # تجاهل التحذيرات الطفيفة
                            if message['severity'] < 2:
                                continue

                            self.issues.append({
                                'file': relative_path,
                                'type': 'eslint_error',
                                'line': message['line'],
                                'code': message['ruleId'],
                                'message': message['message']
                            })
                except json.JSONDecodeError:
                    logger.warning(
                        f"تعذر تحليل مخرجات eslint لملف {file_path}")
        except Exception as e:
            logger.error(f"خطأ في تشغيل eslint: {str(e)}")

    def fix_issues(self) -> None:
        """
        إصلاح المشكلات المكتشفة
        """
        logger.info("بدء إصلاح المشكلات المكتشفة")

        # إصلاح مشكلات Python
        self._fix_python_issues()

        # إصلاح مشكلات JavaScript
        self._fix_js_issues()

        # إصلاح مشكلات Vue
        self._fix_vue_issues()

    def _fix_python_issues(self) -> None:
        """
        إصلاح مشكلات ملفات Python
        """
        # تشغيل autopep8 لإصلاح مشكلات التنسيق
        for file_path in self.python_files:
            try:
                subprocess.run(['autopep8',
                                '--in-place',
                                '--aggressive',
                                '--aggressive',
                                file_path],
                               check=True)
                logger.info(f"تم إصلاح مشكلات التنسيق في {file_path}")
            except Exception as e:
                logger.error(f"خطأ في تشغيل autopep8: {str(e)}")

        # إضافة توثيق الملفات المفقودة
        for issue in self.issues:
            if issue['type'] == 'missing_file_documentation' and issue['file'].endswith(
                    '.py'):
                file_path = os.path.join(self.project_root, issue['file'])
                self._add_file_documentation(file_path, 'python')

    def _fix_js_issues(self) -> None:
        """
        إصلاح مشكلات ملفات JavaScript
        """
        # تشغيل prettier لإصلاح مشكلات التنسيق
        for file_path in self.js_files:
            try:
                subprocess.run(['prettier', '--write', file_path], check=True)
                logger.info(f"تم إصلاح مشكلات التنسيق في {file_path}")
            except Exception as e:
                logger.error(f"خطأ في تشغيل prettier: {str(e)}")

        # إضافة توثيق الملفات المفقودة
        for issue in self.issues:
            if issue['type'] == 'missing_file_documentation' and issue['file'].endswith(
                    '.js'):
                file_path = os.path.join(self.project_root, issue['file'])
                self._add_file_documentation(file_path, 'javascript')

    def _fix_vue_issues(self) -> None:
        """
        إصلاح مشكلات ملفات Vue
        """
        # تشغيل prettier لإصلاح مشكلات التنسيق
        for file_path in self.vue_files:
            try:
                subprocess.run(['prettier', '--write', file_path], check=True)
                logger.info(f"تم إصلاح مشكلات التنسيق في {file_path}")
            except Exception as e:
                logger.error(f"خطأ في تشغيل prettier: {str(e)}")

        # إضافة توثيق الملفات المفقودة
        for issue in self.issues:
            if issue['type'] == 'missing_file_documentation' and issue['file'].endswith(
                    '.vue'):
                file_path = os.path.join(self.project_root, issue['file'])
                self._add_file_documentation(file_path, 'vue')

    def _add_file_documentation(self, file_path: str, file_type: str) -> None:
        """
        إضافة توثيق الملف

        Args:
            file_path: مسار الملف
            file_type: نوع الملف (python, javascript, vue)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            relative_path = os.path.relpath(file_path, self.project_root)
            # file_name = os.path.basename(file_path)  # Not used

            if file_type == 'python':
                doc_template = f'"""\nمسار الملف: {relative_path}\nالوصف: \nالمؤلف: فريق Gaara ERP\nتاريخ الإنشاء: {datetime.now().strftime("%Y-%m-%d")}\n"""\n\n'
                new_content = doc_template + content
            elif file_type == 'javascript':
                doc_template = f'/**\n * مسار الملف: {relative_path}\n * الوصف: \n * المؤلف: فريق Gaara ERP\n * تاريخ الإنشاء: {datetime.now().strftime("%Y-%m-%d")}\n */\n\n'
                new_content = doc_template + content
            elif file_type == 'vue':
                doc_template = f'<!-- \nمسار الملف: {relative_path}\nالوصف: \nالمؤلف: فريق Gaara ERP\nتاريخ الإنشاء: {datetime.now().strftime("%Y-%m-%d")}\n-->\n\n'
                new_content = doc_template + content
            else:
                return

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            logger.info(f"تم إضافة توثيق الملف إلى {file_path}")
        except Exception as e:
            logger.error(f"خطأ في إضافة توثيق الملف {file_path}: {str(e)}")

    def generate_report(self) -> Dict[str, Any]:
        """
        إنشاء تقرير بنتائج التحقق

        Returns:
            Dict[str, Any]: تقرير بنتائج التحقق
        """
        # تصنيف المشكلات حسب النوع
        issues_by_type = {}
        for issue in self.issues:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)

        # تصنيف المشكلات حسب الملف
        issues_by_file = {}
        for issue in self.issues:
            file_path = issue['file']
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)

        # إنشاء التقرير
        report = {
            'summary': {
                'total_files': len(self.python_files) + len(self.js_files) + len(self.vue_files),
                'python_files': len(self.python_files),
                'js_files': len(self.js_files),
                'vue_files': len(self.vue_files),
                'total_issues': len(self.issues),
                'issues_by_type': {issue_type: len(issues) for issue_type, issues in issues_by_type.items()}
            },
            'issues_by_type': issues_by_type,
            'issues_by_file': issues_by_file
        }

        return report

    def save_report(self, output_path: str) -> None:
        """
        حفظ تقرير التحقق إلى ملف

        Args:
            output_path: مسار ملف الإخراج
        """
        report = self.generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"تم حفظ تقرير التحقق إلى {output_path}")


def main(
        project_root: str,
        output_path: str = None,
        fix_issues: bool = False) -> None:
    """
    الدالة الرئيسية

    Args:
        project_root: المسار الجذر للمشروع
        output_path: مسار ملف الإخراج (اختياري)
        fix_issues: ما إذا كان يجب إصلاح المشكلات المكتشفة (اختياري)
    """
    # إعداد المسجل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # إنشاء مدقق الكود
    validator = CodeValidator(project_root)

    # مسح المشروع
    validator.scan_project()

    # التحقق من جودة الكود
    validator.validate_python_files()
    validator.validate_js_files()
    validator.validate_vue_files()

    # إصلاح المشكلات إذا تم طلب ذلك
    if fix_issues:
        validator.fix_issues()

    # إنشاء تقرير
    report = validator.generate_report()

    # طباعة ملخص التقرير
    print(f"إجمالي الملفات: {report['summary']['total_files']}")
    print(f"ملفات Python: {report['summary']['python_files']}")
    print(f"ملفات JavaScript: {report['summary']['js_files']}")
    print(f"ملفات Vue: {report['summary']['vue_files']}")
    print(f"إجمالي المشكلات: {report['summary']['total_issues']}")
    print("المشكلات حسب النوع:")
    for issue_type, count in report['summary']['issues_by_type'].items():
        print(f"  {issue_type}: {count}")

    # حفظ التقرير إذا تم تحديد مسار الإخراج
    if output_path:
        validator.save_report(output_path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='أداة للتحقق من جودة الكود وتنظيفه')
    parser.add_argument('project_root', help='المسار الجذر للمشروع')
    parser.add_argument('--output', help='مسار ملف الإخراج')
    parser.add_argument(
        '--fix',
        action='store_true',
        help='إصلاح المشكلات المكتشفة')

    args = parser.parse_args()

    main(args.project_root, args.output, args.fix)
