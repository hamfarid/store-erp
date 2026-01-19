import logging
from datetime import datetime, timedelta
from collections import Counter
import json
from typing import Dict, List, Any, Optional

import pandas as pd
import numpy as np


# File:
# /home/ubuntu/ai_web_organized/src/modules/ai_management/usage_analyzer.py
"""
آلية تسجيل وتحليل استخدام وكلاء الذكاء الاصطناعي
يوفر هذا الملف وظائف لتسجيل وتحليل استخدام الوكلاء وتوليد تقارير ذكية
"""


# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class UsageAnalyzer:
    """فئة تحليل استخدام وكلاء الذكاء الاصطناعي"""

    def __init__(self, db_service, central_ai_service=None):
        """
        تهيئة محلل الاستخدام

        المعلمات:
            db_service: خدمة قاعدة البيانات للوصول إلى سجلات الاستخدام
            central_ai_service: خدمة الذكاء الاصطناعي المركزية للتحليل المتقدم (اختياري)
        """
        self.db_service = db_service
        self.central_ai_service = central_ai_service
        logger.info("تم تهيئة محلل استخدام وكلاء الذكاء الاصطناعي")

    def _calculate_interaction_metrics(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        حساب مقاييس التفاعل

        المعلمات:
            interaction_data (dict): بيانات التفاعل

        العائد:
            dict: بيانات التفاعل مع المقاييس المحسوبة
        """
        # إضافة الطابع الزمني إذا لم يكن موجودًا
        if 'timestamp' not in interaction_data:
            interaction_data['timestamp'] = datetime.now()

        # حساب إجمالي الرموز والتكلفة
        input_tokens = interaction_data.get('input_tokens', 0)
        output_tokens = interaction_data.get('output_tokens', 0)
        total_tokens = input_tokens + output_tokens

        # الحصول على معلومات الوكيل لحساب التكلفة
        agent_id = interaction_data.get('agent_id')
        agent_info = self.db_service.get_agent(agent_id) if agent_id is not None else None
        cost_per_token = agent_info.get('cost_per_token', 0) if agent_info is not None else 0
        cost = total_tokens * cost_per_token

        # إضافة المعلومات المحسوبة
        interaction_data['total_tokens'] = total_tokens
        interaction_data['cost'] = cost

        return interaction_data

    def _log_minimal_interaction(self, interaction_data: Dict[str, Any], error: Exception) -> int:
        """
        تسجيل الحد الأدنى من معلومات التفاعل في حالة الخطأ

        المعلمات:
            interaction_data (dict): بيانات التفاعل
            error (Exception): الخطأ الذي حدث

        العائد:
            int: معرف السجل المضاف
        """
        try:
            minimal_data = {
                'agent_id': interaction_data.get('agent_id'),
                'user_id': interaction_data.get('user_id'),
                'request_id': interaction_data.get('request_id'),
                'success': False,
                'error_message': f"خطأ في تسجيل التفاعل: {str(error)}",
                'timestamp': datetime.now()
            }
            return self.db_service.log_ai_interaction(minimal_data)
        except Exception:
            logger.critical("فشل في تسجيل الحد الأدنى من معلومات التفاعل")
            return -1

    def log_interaction(self, interaction_data: Dict[str, Any]) -> int:
        """
        تسجيل تفاعل مع وكيل ذكاء اصطناعي

        المعلمات:
            interaction_data (dict): بيانات التفاعل
                - request_id: معرف الطلب
                - agent_id: معرف الوكيل
                - user_id: معرف المستخدم
                - input_text: نص المدخلات
                - output_text: نص المخرجات
                - input_tokens: عدد رموز المدخلات
                - output_tokens: عدد رموز المخرجات
                - processing_time: وقت المعالجة
                - success: هل كانت العملية ناجحة
                - error_message: رسالة الخطأ (إذا كان هناك خطأ)
                - is_failover: هل تم التحويل التلقائي
                - original_agent_id: معرف الوكيل الأصلي (في حالة التحويل التلقائي)

        العائد:
            int: معرف السجل المضاف
        """
        try:
            # حساب مقاييس التفاعل
            interaction_data = self._calculate_interaction_metrics(interaction_data)

            # تسجيل التفاعل في قاعدة البيانات
            log_id = self.db_service.log_ai_interaction(interaction_data)

            # تسجيل في سجل الأنشطة العام
            self._log_to_activity_log(interaction_data)

            # تحليل التفاعل إذا كانت خدمة الذكاء المركزية متاحة
            if self.central_ai_service is not None and interaction_data.get('success', False):
                self._analyze_interaction_async(log_id, interaction_data)

            logger.info("تم تسجيل التفاعل برقم %s للوكيل {interaction_data.get('agent_id')}", log_id)
            return log_id
        except Exception as e:
            logger.error("خطأ أثناء تسجيل التفاعل: %s", str(e))
            return self._log_minimal_interaction(interaction_data, e)

    def generate_usage_report(self,
                              start_date: Optional[datetime] = None,
                              end_date: Optional[datetime] = None,
                              user_id: Optional[int] = None,
                              agent_id: Optional[str] = None,
                              department_id: Optional[int] = None,
                              include_content: bool = False) -> Dict[str, Any]:
        """
        توليد تقرير استخدام وكلاء الذكاء الاصطناعي

        المعلمات:
            start_date (datetime, optional): تاريخ بداية التقرير
            end_date (datetime, optional): تاريخ نهاية التقرير
            user_id (int, optional): تصفية حسب معرف المستخدم
            agent_id (str, optional): تصفية حسب معرف الوكيل
            department_id (int, optional): تصفية حسب معرف القسم
            include_content (bool): تضمين محتوى المدخلات والمخرجات

        العائد:
            dict: تقرير الاستخدام
        """
        try:
            # تعيين التواريخ الافتراضية إذا لم يتم تحديدها
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                # تقرير الشهر الماضي افتراضيًا
                start_date = end_date - timedelta(days=30)

            # الحصول على سجلات الاستخدام من قاعدة البيانات
            logs = self.db_service.get_ai_usage_logs(
                start_date=start_date,
                end_date=end_date,
                user_id=user_id,
                agent_id=agent_id,
                department_id=department_id
            )

            if not logs:
                return {
                    'start_date': start_date,
                    'end_date': end_date,
                    'total_interactions': 0,
                    'message': 'لا توجد بيانات للفترة المحددة'
                }

            # تحويل السجلات إلى DataFrame للتحليل
            df = pd.DataFrame(logs)

            # إحصائيات أساسية
            total_interactions = len(df)
            successful_interactions = df['success'].sum()
            failed_interactions = total_interactions - successful_interactions
            success_rate = (successful_interactions / total_interactions) * \
                100 if total_interactions > 0 else 0

            total_tokens = df['total_tokens'].sum()
            total_cost = df['cost'].sum()
            avg_tokens_per_interaction = df['total_tokens'].mean()
            avg_response_time = df['processing_time'].mean()

            # تحليل حسب الوكيل
            agent_stats = df.groupby('agent_id').agg({
                'id': 'count',
                'success': 'sum',
                'total_tokens': 'sum',
                'cost': 'sum',
                'processing_time': 'mean'
            }).reset_index()

            agent_stats.columns = [
                'agent_id',
                'interactions',
                'successful',
                'total_tokens',
                'total_cost',
                'avg_response_time']
            agent_stats['success_rate'] = (
                agent_stats['successful'] / agent_stats['interactions']) * 100

            # تحليل حسب المستخدم
            user_stats = df.groupby('user_id').agg({
                'id': 'count',
                'total_tokens': 'sum',
                'cost': 'sum'
            }).reset_index()

            user_stats.columns = [
                'user_id',
                'interactions',
                'total_tokens',
                'total_cost']

            # تحليل حسب اليوم
            df['date'] = pd.to_datetime(df['created_at']).dt.date
            daily_stats = df.groupby('date').agg({
                'id': 'count',
                'total_tokens': 'sum',
                'cost': 'sum'
            }).reset_index()

            daily_stats.columns = [
                'date',
                'interactions',
                'total_tokens',
                'total_cost']

            # تحليل أوقات الذروة
            df['hour'] = pd.to_datetime(df['created_at']).dt.hour
            hourly_stats = df.groupby('hour').agg({
                'id': 'count'
            }).reset_index()

            hourly_stats.columns = ['hour', 'interactions']
            peak_hour = hourly_stats.loc[hourly_stats['interactions'].idxmax(
            )]['hour']

            # تحليل التحويل التلقائي
            failover_count = df['is_failover'].sum()
            failover_rate = (failover_count / total_interactions) * \
                100 if total_interactions > 0 else 0

            # تحليل أنواع الأسئلة (إذا كانت خدمة الذكاء المركزية متاحة)
            question_categories = {}
            if self.central_ai_service is not None:
                # الحصول على تصنيفات الأسئلة من تحليلات الذكاء المركزي
                question_categories = self._get_question_categories(df)

            # إنشاء التقرير
            report = {
                'start_date': start_date,
                'end_date': end_date,
                'total_interactions': total_interactions,
                'successful_interactions': successful_interactions,
                'failed_interactions': failed_interactions,
                'success_rate': success_rate,
                'total_tokens': total_tokens,
                'total_cost': total_cost,
                'avg_tokens_per_interaction': avg_tokens_per_interaction,
                'avg_response_time': avg_response_time,
                'peak_hour': peak_hour,
                'failover_count': failover_count,
                'failover_rate': failover_rate,
                'agent_stats': agent_stats.to_dict('records'),
                'user_stats': user_stats.to_dict('records'),
                'daily_stats': daily_stats.to_dict('records'),
                'hourly_stats': hourly_stats.to_dict('records')
            }

            if question_categories:
                report['question_categories'] = question_categories

            # إضافة محتوى المدخلات والمخرجات إذا تم طلبه
            if include_content:
                content_samples = df.sample(min(10, len(df)))[
                    ['input_text', 'output_text', 'created_at', 'user_id', 'agent_id']]
                report['content_samples'] = content_samples.to_dict('records')

            logger.info("تم توليد تقرير الاستخدام: %s تفاعل", total_interactions)
            return report
        except Exception as e:
            logger.error("خطأ أثناء توليد تقرير الاستخدام: %s", str(e))
            return {
                'error': f"خطأ أثناء توليد التقرير: {str(e)}",
                'start_date': start_date,
                'end_date': end_date
            }

    def generate_compliance_report(self,
                                   start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None,
                                   user_id: Optional[int] = None,
                                   department_id: Optional[int] = None) -> Dict[str, Any]:
        """
        توليد تقرير الامتثال لاستخدام وكلاء الذكاء الاصطناعي

        المعلمات:
            start_date (datetime, optional): تاريخ بداية التقرير
            end_date (datetime, optional): تاريخ نهاية التقرير
            user_id (int, optional): تصفية حسب معرف المستخدم
            department_id (int, optional): تصفية حسب معرف القسم

        العائد:
            dict: تقرير الامتثال
        """
        try:
            # تعيين التواريخ الافتراضية إذا لم يتم تحديدها
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                # تقرير الشهر الماضي افتراضيًا
                start_date = end_date - timedelta(days=30)

            # الحصول على سجلات الاستخدام من قاعدة البيانات
            logs = self.db_service.get_ai_usage_logs(
                start_date=start_date,
                end_date=end_date,
                user_id=user_id,
                department_id=department_id,
                include_analysis=True
            )

            if not logs:
                return {
                    'start_date': start_date,
                    'end_date': end_date,
                    'total_interactions': 0,
                    'message': 'لا توجد بيانات للفترة المحددة'
                }

            # تحويل السجلات إلى DataFrame للتحليل
            df = pd.DataFrame(logs)

            # تحليل الامتثال لكل تفاعل
            compliance_data = []
            for _, row in df.iterrows():
                if row.get('analysis'):
                    try:
                        if isinstance(row['analysis'], str):
                            analysis = json.loads(row['analysis'])
                        else:
                            analysis = row['analysis']

                        compliance_data.append({
                            'log_id': row['id'],
                            'user_id': row['user_id'],
                            'timestamp': row['timestamp'],
                            'compliance_score': analysis.get('compliance_score', 100),
                            'issues': analysis.get('issues', []),
                            'is_compliant': analysis.get('is_compliant', True)
                        })
                    except Exception as e:
                        logger.warning("خطأ في تحليل بيانات الامتثال للسجل %s: %s", row['id'], str(e))

            if not compliance_data:
                return {
                    'start_date': start_date,
                    'end_date': end_date,
                    'total_interactions': len(df),
                    'message': 'لا توجد بيانات امتثال للفترة المحددة'
                }

            # تحويل بيانات الامتثال إلى DataFrame
            compliance_df = pd.DataFrame(compliance_data)

            # إحصائيات الامتثال
            total_interactions = len(compliance_df)
            compliant_count = compliance_df['is_compliant'].sum()
            non_compliant_count = total_interactions - compliant_count
            compliance_rate = (compliant_count / total_interactions) * 100 if total_interactions > 0 else 0

            avg_compliance_score = compliance_df['compliance_score'].mean()
            min_compliance_score = compliance_df['compliance_score'].min()
            max_compliance_score = compliance_df['compliance_score'].max()

            # تحليل المشكلات
            all_issues = []
            for issues in compliance_df['issues']:
                if isinstance(issues, list):
                    all_issues.extend(issues)
            issue_counts = Counter(all_issues)

            # إنشاء التقرير
            report = {
                'start_date': start_date,
                'end_date': end_date,
                'total_interactions': total_interactions,
                'compliant_count': compliant_count,
                'non_compliant_count': non_compliant_count,
                'compliance_rate': compliance_rate,
                'avg_compliance_score': avg_compliance_score,
                'min_compliance_score': min_compliance_score,
                'max_compliance_score': max_compliance_score,
                'issue_counts': dict(issue_counts)
            }

            # إضافة أمثلة على المخالفات
            if non_compliant_count > 0:
                non_compliant_examples = compliance_df[compliance_df['is_compliant'] is False].head(5)
                non_compliant_logs = []

                for _, row in non_compliant_examples.iterrows():
                    log_data = df[df['id'] == row['log_id']].iloc[0]
                    non_compliant_logs.append({
                        'log_id': row['log_id'],
                        'user_id': row['user_id'],
                        'timestamp': row['timestamp'],
                        'input_text': log_data['input_text'],
                        'output_text': log_data['output_text'],
                        'issues': row['issues'],
                        'compliance_score': row['compliance_score']
                    })

                report['non_compliant_examples'] = non_compliant_logs

            logger.info("تم توليد تقرير الامتثال: %s تفاعل محلل", len(compliance_df))
            return report
        except Exception as e:
            logger.error("خطأ أثناء توليد تقرير الامتثال: %s", str(e))
            return {
                'error': f"خطأ أثناء توليد تقرير الامتثال: {str(e)}",
                'start_date': start_date,
                'end_date': end_date
            }

    def analyze_user_behavior(
            self, user_id: int, time_period: int = 30) -> Dict[str, Any]:
        """
        تحليل سلوك المستخدم في استخدام وكلاء الذكاء الاصطناعي

        المعلمات:
            user_id (int): معرف المستخدم
            time_period (int): الفترة الزمنية بالأيام للتحليل

        العائد:
            dict: تحليل سلوك المستخدم
        """
        try:
            # تحديد نطاق التاريخ
            end_date = datetime.now()
            start_date = end_date - timedelta(days=time_period)

            # الحصول على سجلات استخدام المستخدم
            logs = self.db_service.get_ai_usage_logs(
                start_date=start_date,
                end_date=end_date,
                user_id=user_id,
                include_analysis=True
            )

            if not logs:
                return {
                    'user_id': user_id,
                    'time_period': time_period,
                    'message': 'لا توجد بيانات استخدام للفترة المحددة'
                }

            # تحويل السجلات إلى DataFrame للتحليل
            df = pd.DataFrame(logs)

            # الحصول على معلومات المستخدم
            user_info = self.db_service.get_user(user_id)

            # إحصائيات أساسية
            total_interactions = len(df)
            total_tokens = df['total_tokens'].sum()
            total_cost = df['cost'].sum()
            avg_tokens_per_interaction = df['total_tokens'].mean()

            # تحليل أنماط الاستخدام
            df['date'] = pd.to_datetime(df['created_at']).dt.date
            df['hour'] = pd.to_datetime(df['created_at']).dt.hour
            df['day_of_week'] = pd.to_datetime(df['created_at']).dt.dayofweek

            # أنماط الاستخدام اليومي
            daily_usage = df.groupby('date').size().reset_index(name='count')

            # أنماط الاستخدام حسب ساعات اليوم
            hourly_usage = df.groupby('hour').size().reset_index(name='count')
            peak_hour = hourly_usage.loc[hourly_usage['count'].idxmax(
            )]['hour']

            # أنماط الاستخدام حسب أيام الأسبوع
            day_of_week_usage = df.groupby(
                'day_of_week').size().reset_index(name='count')
            day_names = [
                'الاثنين',
                'الثلاثاء',
                'الأربعاء',
                'الخميس',
                'الجمعة',
                'السبت',
                'الأحد']
            day_of_week_usage['day_name'] = day_of_week_usage['day_of_week'].apply(
                lambda x: day_names[x])

            # تحليل الوكلاء المستخدمة
            agent_usage = df.groupby(
                'agent_id').size().reset_index(name='count')
            favorite_agent = agent_usage.loc[agent_usage['count'].idxmax(
            )]['agent_id'] if not agent_usage.empty else None

            # تحليل أنواع الأسئلة
            question_categories = {}
            if self.central_ai_service is not None:
                question_categories = self._get_question_categories(df)

            # تحليل طول المدخلات والمخرجات
            df['input_length'] = df['input_text'].apply(
                lambda x: len(
                    x.split()) if isinstance(
                    x, str) else 0)
            df['output_length'] = df['output_text'].apply(
                lambda x: len(
                    x.split()) if isinstance(
                    x, str) else 0)

            avg_input_length = df['input_length'].mean()
            avg_output_length = df['output_length'].mean()

            # تحليل الامتثال
            compliance_data = {}
            if 'analysis' in df.columns:
                compliance_scores = []
                for analysis in df['analysis']:
                    if analysis:
                        try:
                            if isinstance(analysis, str):
                                analysis = json.loads(analysis)
                            compliance_scores.append(
                                analysis.get('compliance_score', 100))
                        except BaseException:
                            compliance_scores.append(100)

                if compliance_scores:
                    compliance_data = {
                        'avg_compliance_score': np.mean(compliance_scores),
                        'min_compliance_score': min(compliance_scores),
                        'max_compliance_score': max(compliance_scores)
                    }

            # إنشاء التقرير
            report = {
                'user_id': user_id,
                'user_name': f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}" if user_info else f"المستخدم {user_id}",
                'time_period': time_period,
                'start_date': start_date,
                'end_date': end_date,
                'total_interactions': total_interactions,
                'total_tokens': total_tokens,
                'total_cost': total_cost,
                'avg_tokens_per_interaction': avg_tokens_per_interaction,
                'avg_input_length': avg_input_length,
                'avg_output_length': avg_output_length,
                'peak_hour': peak_hour,
                'favorite_agent': favorite_agent,
                'daily_usage': daily_usage.to_dict('records'),
                'hourly_usage': hourly_usage.to_dict('records'),
                'day_of_week_usage': day_of_week_usage.to_dict('records'),
                'agent_usage': agent_usage.to_dict('records')}

            if question_categories:
                report['question_categories'] = question_categories

            if compliance_data:
                report.update(compliance_data)

            # توصيات للمستخدم
            recommendations = self._generate_user_recommendations(df, report)
            if recommendations:
                report['recommendations'] = recommendations

            logger.info("تم توليد تحليل سلوك المستخدم %s: %s تفاعل", user_id, total_interactions)
            return report
        except Exception as e:
            logger.error("خطأ أثناء تحليل سلوك المستخدم %s: %s", user_id, str(e))
            return {
                'error': f"خطأ أثناء تحليل سلوك المستخدم: {str(e)}",
                'user_id': user_id,
                'time_period': time_period
            }

    def _log_to_activity_log(self, interaction_data: Dict[str, Any]) -> None:
        """
        تسجيل التفاعل في سجل الأنشطة العام

        المعلمات:
            interaction_data (dict): بيانات التفاعل
        """
        try:
            # إنشاء بيانات النشاط
            activity_data = {
                'user_id': interaction_data.get('user_id'),
                'activity_type': 'ai_interaction',
                'activity_details': {
                    'agent_id': interaction_data.get('agent_id'),
                    'request_id': interaction_data.get('request_id'),
                    'success': interaction_data.get('success', True),
                    'tokens': interaction_data.get('total_tokens', 0)
                },
                'timestamp': interaction_data.get('timestamp', datetime.now())
            }

            # تسجيل النشاط في سجل الأنشطة العام
            self.db_service.log_activity(activity_data)
        except Exception as e:
            logger.error("خطأ أثناء تسجيل التفاعل في سجل الأنشطة: %s", str(e))

    def _analyze_interaction_async(
            self, log_id: int, interaction_data: Dict[str, Any]) -> None:
        """
        تحليل التفاعل بشكل غير متزامن

        المعلمات:
            log_id (int): معرف السجل
            interaction_data (dict): بيانات التفاعل
        """
        try:
            # التحقق من توفر خدمة الذكاء المركزية
            if not self.central_ai_service:
                return

            # تحليل التفاعل
            analysis_result = self._analyze_interaction_compliance(
                interaction_data.get('input_text', ''),
                interaction_data.get('output_text', ''),
                interaction_data.get('user_id')
            )

            # تحديث السجل بنتائج التحليل
            if analysis_result:
                self.db_service.update_interaction_analysis(
                    log_id, analysis_result)
        except Exception as e:
            logger.error("خطأ أثناء تحليل التفاعل: %s", str(e))

    def _analyze_interaction_compliance(self,
                                        input_text: str,
                                        output_text: str,
                                        user_id: Optional[int] = None) -> Dict[str,
                                                                               Any]:
        """
        تحليل امتثال التفاعل

        المعلمات:
            input_text (str): نص المدخلات
            output_text (str): نص المخرجات
            user_id (int, optional): معرف المستخدم

        العائد:
            dict: نتائج التحليل
        """
        try:
            # التحقق من توفر خدمة الذكاء المركزية
            if not self.central_ai_service:
                return {}

            # الحصول على معلومات المستخدم وصلاحياته
            user_info = self.db_service.get_user(user_id) if user_id else None
            user_roles = self.db_service.get_user_roles(
                user_id) if user_id else []

            # إعداد بيانات التحليل
            analysis_data = {
                'input_text': input_text,
                'output_text': output_text,
                'user_info': user_info,
                'user_roles': user_roles
            }

            # استدعاء خدمة الذكاء المركزية لتحليل التفاعل
            analysis_result = self.central_ai_service.analyze_interaction(
                analysis_data)

            return analysis_result
        except Exception as e:
            logger.error("خطأ أثناء تحليل امتثال التفاعل: %s", str(e))
            return {}

    def _get_question_categories(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        الحصول على تصنيفات الأسئلة من تحليلات الذكاء المركزي

        المعلمات:
            df (DataFrame): إطار البيانات للتحليل

        العائد:
            dict: توزيع تصنيفات الأسئلة
        """
        try:
            # التحقق من توفر خدمة الذكاء المركزية
            if not self.central_ai_service:
                return {}

            # استخراج تصنيفات الأسئلة من نتائج التحليل
            categories = []

            for _, row in df.iterrows():
                analysis = row.get('analysis')

                if analysis:
                    try:
                        if isinstance(analysis, str):
                            analysis = json.loads(analysis)

                        category = analysis.get('category')
                        if category:
                            categories.append(category)
                    except BaseException:
                        pass

            # حساب توزيع التصنيفات
            category_counts = Counter(categories)

            return dict(category_counts)
        except Exception as e:
            logger.error("خطأ أثناء الحصول على تصنيفات الأسئلة: %s", str(e))
            return {}

    def _generate_user_recommendations(
            self, df: pd.DataFrame, report: Dict[str, Any]) -> List[str]:
        """
        توليد توصيات للمستخدم بناءً على تحليل السلوك

        المعلمات:
            df (DataFrame): إطار البيانات للتحليل
            report (dict): تقرير تحليل السلوك

        العائد:
            list: قائمة التوصيات
        """
        try:
            recommendations = []

            # توصيات بناءً على طول المدخلات
            avg_input_length = report.get('avg_input_length', 0)
            if avg_input_length < 5:
                recommendations.append(
                    "حاول تقديم أسئلة أكثر تفصيلاً للحصول على إجابات أفضل")
            elif avg_input_length > 100:
                recommendations.append(
                    "يمكن تقسيم الأسئلة الطويلة جداً إلى أسئلة أصغر للحصول على إجابات أكثر تركيزاً")

            # توصيات بناءً على معدل الاستخدام
            daily_usage = df.groupby('date').size()
            if len(daily_usage) > 0:
                max_daily = daily_usage.max()
                if max_daily > 50:
                    recommendations.append(
                        "لاحظنا استخداماً مكثفاً في بعض الأيام، يمكن توزيع الاستفسارات على مدار اليوم لتحسين الأداء")

            # توصيات بناءً على الامتثال
            compliance_score = report.get('avg_compliance_score', 100)
            if compliance_score < 80:
                recommendations.append(
                    "يرجى مراجعة إرشادات استخدام الذكاء الاصطناعي للتأكد من الامتثال لسياسات الشركة")

            # توصيات بناءً على تنوع الوكلاء
            agent_usage = report.get('agent_usage', [])
            if len(agent_usage) == 1:
                recommendations.append(
                    "جرب استخدام وكلاء ذكاء اصطناعي متنوعة للحصول على نتائج أفضل لأنواع مختلفة من الاستفسارات")

            return recommendations
        except Exception as e:
            logger.error("خطأ أثناء توليد توصيات المستخدم: %s", str(e))
            return []
