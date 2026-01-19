import unittest
import logging
import sys
import os
from datetime import datetime, timedelta


from src.modules.ai_management.ai_connectors.base_connector import BaseConnector
from src.modules.ai_management.usage_analyzer import UsageAnalyzer
from src.modules.ai_management.load_balancer import LoadBalancer
from src.modules.ai_management.multi_agent_router import MultiAgentRouter

# File:
# /home/ubuntu/ai_web_organized/src/modules/ai_management/test_integration.py
"""
اختبار تكاملي شامل لنظام إدارة وكلاء الذكاء الاصطناعي المتعدد
يوفر هذا الملف اختبارات تكاملية للتحقق من عمل جميع مكونات النظام معًا
"""


# إضافة المسار الجذر للمشروع إلى مسار البحث
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../../..')))


# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MockDBService:
    """خدمة قاعدة بيانات وهمية للاختبار"""

    def __init__(self):
        self.agents = [
            {
                'id': 'agent1',
                'name': 'وكيل الذكاء الاصطناعي 1',
                'type': 'openai',
                'enabled': True,
                'priority': 10,
                'capabilities': 'text,image_processing',
                'cost_per_token': 0.001
            },
            {
                'id': 'agent2',
                'name': 'وكيل الذكاء الاصطناعي 2',
                'type': 'azure',
                'enabled': True,
                'priority': 5,
                'capabilities': 'text',
                'cost_per_token': 0.0005
            },
            {
                'id': 'agent3',
                'name': 'وكيل الذكاء الاصطناعي 3',
                'type': 'local',
                'enabled': False,
                'priority': 1,
                'capabilities': 'text',
                'cost_per_token': 0.0001
            }
        ]
        self.usage_logs = []
        self.failover_logs = []
        self.agent_stats = {}
        self.user_preferences = {
            1: {
                'preferred_agent_id': 'agent1',
                'excluded_agents': '',
                'allowed_agents': ''
            },
            2: {
                'preferred_agent_id': '',
                'excluded_agents': 'agent1',
                'allowed_agents': ''
            }
        }
        self.users = {
            1: {'id': 1, 'first_name': 'أحمد', 'last_name': 'محمد', 'roles': ['admin']},
            2: {'id': 2, 'first_name': 'سارة', 'last_name': 'أحمد', 'roles': ['user']}
        }

    def get_enabled_agents(self):
        return [agent for agent in self.agents if agent['enabled']]

    def get_agent(self, agent_id):
        return next(
            (agent for agent in self.agents if agent['id'] == agent_id),
            None)

    def log_ai_interaction(self, interaction_data):
        interaction_data['id'] = len(self.usage_logs) + 1
        self.usage_logs.append(interaction_data)
        return interaction_data['id']

    def log_failover(self, **kwargs):
        self.failover_logs.append(kwargs)
        return len(self.failover_logs)

    def update_agent_stats(self, **kwargs):
        agent_id = kwargs.get('agent_id')
        if agent_id not in self.agent_stats:
            self.agent_stats[agent_id] = {
                'total_requests': 0,
                'successful_requests': 0,
                'total_tokens': 0}

        self.agent_stats[agent_id]['total_requests'] += 1
        if kwargs.get('success', False):
            self.agent_stats[agent_id]['successful_requests'] += 1
        self.agent_stats[agent_id]['total_tokens'] += kwargs.get('tokens', 0)

    def update_agent_error_stats(self, **kwargs):
        agent_id = kwargs.get('agent_id')
        if agent_id not in self.agent_stats:
            self.agent_stats[agent_id] = {'total_requests': 0, 'errors': 0}

        self.agent_stats[agent_id]['errors'] = self.agent_stats[agent_id].get(
            'errors', 0) + 1

    def get_user_preferences(self, user_id):
        return self.user_preferences.get(user_id, {})

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_user_roles(self, user_id):
        user = self.get_user(user_id)
        return user.get('roles', []) if user else []

    def get_ai_usage_logs(self, **kwargs):
        return self.usage_logs

    def update_interaction_analysis(self, log_id, analysis_result):
        for log in self.usage_logs:
            if log['id'] == log_id:
                log['analysis'] = analysis_result
                return True
        return False

    def log_activity(self, activity_data):
        # تسجيل النشاط في سجل الأنشطة العام (وهمي للاختبار)
        return True


class MockConnector(BaseConnector):
    """موصل وهمي للاختبار"""

    def __init__(self, agent_id, config):
        super().__init__(agent_id, config)
        self.should_fail = config.get('should_fail', False)

    def validate_request(self, request):
        return True

    def process_request(self, request):
        if self.should_fail is not None:
            raise ConnectionError("فشل مقصود للاختبار")

        return {
            'output': {
                'text': f"استجابة من الوكيل {self.agent_id} للطلب: {request.get('input', {}).get('text', '')}"},
            'tokens': {
                'input': len(
                    request.get(
                        'input',
                        {}).get(
                        'text',
                        '').split()),
                'output': 20},
            'processing_time': 0.5}

    def test_connection(self):
        if self.should_fail is not None:
            return {'success': False, 'message': "فشل الاتصال"}
        return {'success': True, 'message': "تم الاتصال بنجاح"}


class MockCentralAIService:
    """خدمة ذكاء اصطناعي مركزية وهمية للاختبار"""

    def analyze_interaction(self, analysis_data):
        input_text = analysis_data.get('input_text', '')
        output_text = analysis_data.get('output_text', '')

        # تحليل وهمي للامتثال
        is_compliant = 'محظور' not in input_text and 'محظور' not in output_text
        compliance_score = 100 if is_compliant else 50

        # تصنيف وهمي للسؤال
        category = 'استفسار عام'
        if 'زراعة' in input_text:
            category = 'زراعة'
        elif 'صحة' in input_text:
            category = 'صحة'
        elif 'تقنية' in input_text:
            category = 'تقنية'

        return {
            'is_compliant': is_compliant,
            'compliance_score': compliance_score,
            'issues': [] if is_compliant else ['محتوى محظور'],
            'category': category
        }


class TestMultiAgentRouter(unittest.TestCase):
    """اختبارات موجه الوكلاء المتعدد"""

    def setUp(self):
        self.db_service = MockDBService()
        self.central_ai_service = MockCentralAIService()
        self.load_balancer = LoadBalancer(self.db_service, strategy="priority")
        self.router = MultiAgentRouter(
            self.db_service,
            self.central_ai_service)

        # تسجيل الموصلات الوهمية
        self.router.register_connector(  # pylint: disable=no-member
            'openai',
            lambda agent_id, config: MockConnector(agent_id, config)  # pylint: disable=no-member
        )
        self.router.register_connector(  # pylint: disable=no-member
            'azure',
            lambda agent_id, config: MockConnector(agent_id, config)  # pylint: disable=no-member
        )
        self.router.register_connector(  # pylint: disable=no-member
            'local',
            lambda agent_id, config: MockConnector(agent_id, config)  # pylint: disable=no-member
        )

    def test_route_request_success(self):
        """اختبار توجيه الطلب بنجاح"""
        request = {
            'input': {
                'text': 'مرحبًا، هذا طلب اختبار'
            },
            'type': 'text'
        }

        response = self.router.route_request(request, user_id=1)

        self.assertIn('output', response)
        self.assertIn('text', response['output'])
        # يجب أن يستخدم الوكيل المفضل للمستخدم 1
        self.assertIn('agent1', response['output']['text'])
        self.assertEqual(len(self.db_service.usage_logs), 1)

    def test_route_request_with_user_preferences(self):
        """اختبار توجيه الطلب مع تفضيلات المستخدم"""
        request = {
            'input': {
                'text': 'مرحبًا، هذا طلب اختبار'
            },
            'type': 'text'
        }

        # المستخدم 2 لديه استبعاد للوكيل 1
        response = self.router.route_request(request, user_id=2)

        self.assertIn('output', response)
        self.assertIn('text', response['output'])
        # يجب أن يستخدم الوكيل 2 لأن الوكيل 1 مستبعد
        self.assertIn('agent2', response['output']['text'])
        self.assertEqual(len(self.db_service.usage_logs), 2)

    def test_route_request_with_specific_agent(self):
        """اختبار توجيه الطلب إلى وكيل محدد"""
        request = {
            'input': {
                'text': 'مرحبًا، هذا طلب اختبار'
            },
            'type': 'text',
            'agent_id': 'agent2'  # تحديد الوكيل مباشرة
        }

        response = self.router.process_request(request, agent_id='agent2')  # pylint: disable=no-member  # pylint: disable=no-member

        self.assertIn('output', response)
        self.assertIn('text', response['output'])
        self.assertIn('agent2', response['output']['text'])
        self.assertEqual(len(self.db_service.usage_logs), 3)

    def test_failover(self):
        """اختبار التحويل التلقائي في حالة فشل الوكيل"""
        # تعديل الوكيل 1 ليفشل
        agent1 = self.db_service.get_agent('agent1')
        agent1['should_fail'] = True

        request = {
            'input': {
                'text': 'مرحبًا، هذا طلب اختبار للتحويل التلقائي'
            },
            'type': 'text'
        }

        response = self.router.route_request(request, user_id=1)

        self.assertIn('output', response)
        self.assertIn('text', response['output'])
        # يجب أن يتحول تلقائيًا إلى الوكيل 2
        self.assertIn('agent2', response['output']['text'])
        self.assertEqual(len(self.db_service.failover_logs), 1)
        self.assertEqual(len(self.db_service.usage_logs), 4)

    def test_disabled_agent(self):
        """اختبار عدم استخدام وكيل معطل"""
        # محاولة استخدام الوكيل 3 المعطل
        request = {
            'input': {
                'text': 'مرحبًا، هذا طلب اختبار لوكيل معطل'
            },
            'type': 'text',
            'agent_id': 'agent3'
        }

        # يجب أن يفشل لأن الوكيل معطل
        with self.assertRaises(Exception):
            self.router.process_request(request, agent_id='agent3')  # pylint: disable=no-member  # pylint: disable=no-member


class TestLoadBalancer(unittest.TestCase):
    """اختبارات موازن الحمل"""

    def setUp(self):
        self.db_service = MockDBService()

    def test_priority_strategy(self):
        """اختبار استراتيجية الأولوية"""
        load_balancer = LoadBalancer(self.db_service, strategy="priority")

        request = {'type': 'text'}
        agent_id, _ = load_balancer.select_agent(request)

        self.assertEqual(agent_id, 'agent1')  # الوكيل 1 له أعلى أولوية

    def test_round_robin_strategy(self):
        """اختبار استراتيجية التناوب الدائري"""
        load_balancer = LoadBalancer(self.db_service, strategy="round_robin")

        request = {'type': 'text'}

        # الاستدعاء الأول
        agent_id1, _ = load_balancer.select_agent(request)
        # الاستدعاء الثاني
        agent_id2, _ = load_balancer.select_agent(request)
        # الاستدعاء الثالث (يجب أن يعود إلى الأول)
        agent_id3, _ = load_balancer.select_agent(request)

        self.assertNotEqual(agent_id1, agent_id2)
        self.assertEqual(agent_id1, agent_id3)

    def test_filter_by_request_type(self):
        """اختبار تصفية الوكلاء حسب نوع الطلب"""
        load_balancer = LoadBalancer(self.db_service, strategy="priority")

        # طلب معالجة صورة
        request = {'type': 'image'}
        agent_id, _ = load_balancer.select_agent(request)

        self.assertEqual(agent_id, 'agent1')  # فقط الوكيل 1 يدعم معالجة الصور

    def test_filter_by_user_preferences(self):
        """اختبار تصفية الوكلاء حسب تفضيلات المستخدم"""
        load_balancer = LoadBalancer(self.db_service, strategy="priority")

        request = {'type': 'text'}

        # المستخدم 1 يفضل الوكيل 1
        agent_id1, _ = load_balancer.select_agent(request, user_id=1)

        # المستخدم 2 يستبعد الوكيل 1
        agent_id2, _ = load_balancer.select_agent(request, user_id=2)

        self.assertEqual(agent_id1, 'agent1')
        self.assertEqual(agent_id2, 'agent2')

    def test_failover(self):
        """اختبار التحويل التلقائي"""
        load_balancer = LoadBalancer(self.db_service, strategy="priority")

        request = {'type': 'text'}

        # التحويل التلقائي من الوكيل 1 إلى الوكيل التالي
        agent_id, _ = load_balancer.handle_failover(
            'agent1', request, Exception("فشل اختبار"), user_id=1)

        self.assertEqual(agent_id, 'agent2')
        self.assertEqual(len(self.db_service.failover_logs), 1)


class TestUsageAnalyzer(unittest.TestCase):
    """اختبارات محلل الاستخدام"""

    def setUp(self):
        self.db_service = MockDBService()
        self.central_ai_service = MockCentralAIService()
        self.usage_analyzer = UsageAnalyzer(
            self.db_service, self.central_ai_service)

        # إضافة بعض سجلات الاستخدام للاختبار
        self._add_sample_usage_logs()

    def _add_sample_usage_logs(self):
        """إضافة سجلات استخدام نموذجية للاختبار"""
        # سجل استخدام ناجح للمستخدم 1 مع الوكيل 1
        self.usage_analyzer.log_interaction({
            'request_id': 'req1',
            'agent_id': 'agent1',
            'user_id': 1,
            'input_text': 'ما هي أفضل الممارسات في زراعة القمح؟',
            'output_text': 'تتضمن أفضل الممارسات في زراعة القمح: اختيار التربة المناسبة، الري المنتظم، استخدام الأسمدة المناسبة...',
            'input_tokens': 10,
            'output_tokens': 30,
            'total_tokens': 40,
            'processing_time': 0.8,
            'success': True,
            'timestamp': datetime.now() - timedelta(days=2)
        })

        # سجل استخدام ناجح للمستخدم 2 مع الوكيل 2
        self.usage_analyzer.log_interaction({
            'request_id': 'req2',
            'agent_id': 'agent2',
            'user_id': 2,
            'input_text': 'كيف يمكنني تحسين إنتاجية محصول الطماطم؟',
            'output_text': 'لتحسين إنتاجية محصول الطماطم، يمكنك اتباع الخطوات التالية: استخدام بذور عالية الجودة، الري المناسب...',
            'input_tokens': 8,
            'output_tokens': 25,
            'total_tokens': 33,
            'processing_time': 0.6,
            'success': True,
            'timestamp': datetime.now() - timedelta(days=1)
        })

        # سجل استخدام فاشل للمستخدم 1 مع الوكيل 1
        self.usage_analyzer.log_interaction({
            'request_id': 'req3',
            'agent_id': 'agent1',
            'user_id': 1,
            'input_text': 'كيف يمكنني الحصول على محتوى محظور؟',
            'output_text': '',
            'input_tokens': 7,
            'output_tokens': 0,
            'total_tokens': 7,
            'processing_time': 0.3,
            'success': False,
            'error_message': 'محتوى غير مناسب',
            'timestamp': datetime.now()
        })

    def test_log_interaction(self):
        """اختبار تسجيل التفاعل"""
        interaction_data = {
            'request_id': 'req4',
            'agent_id': 'agent2',
            'user_id': 2,
            'input_text': 'ما هي أفضل أنواع الأسمدة للخضروات؟',
            'output_text': 'تختلف أنواع الأسمدة المناسبة للخضروات حسب نوع المحصول والتربة...',
            'input_tokens': 9,
            'output_tokens': 20,
            'processing_time': 0.7,
            'success': True}

        log_id = self.usage_analyzer.log_interaction(interaction_data)

        self.assertEqual(log_id, 4)  # يجب أن يكون هذا هو السجل الرابع
        self.assertEqual(len(self.db_service.usage_logs), 4)

    def test_generate_usage_report(self):
        """اختبار توليد تقرير الاستخدام"""
        report = self.usage_analyzer.generate_usage_report()

        self.assertIn('total_interactions', report)
        self.assertEqual(report['total_interactions'], 3)
        self.assertIn('successful_interactions', report)
        self.assertEqual(report['successful_interactions'], 2)
        self.assertIn('agent_stats', report)
        # يجب أن يكون هناك إحصائيات لوكيلين
        self.assertEqual(len(report['agent_stats']), 2)

    def test_generate_compliance_report(self):
        """اختبار توليد تقرير الامتثال"""
        report = self.usage_analyzer.generate_compliance_report()

        self.assertIn('total_interactions', report)
        self.assertEqual(report['total_interactions'], 3)
        self.assertIn('analyzed_interactions', report)
        self.assertIn('compliance_rate', report)

    def test_analyze_user_behavior(self):
        """اختبار تحليل سلوك المستخدم"""
        analysis = self.usage_analyzer.analyze_user_behavior(user_id=1)

        self.assertIn('user_id', analysis)
        self.assertEqual(analysis['user_id'], 1)
        self.assertIn('total_interactions', analysis)
        self.assertEqual(
            analysis['total_interactions'],
            2)  # المستخدم 1 لديه تفاعلان
        self.assertIn('recommendations', analysis)


def run_tests():
    """تشغيل جميع الاختبارات"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestMultiAgentRouter))
    suite.addTests(loader.loadTestsFromTestCase(TestLoadBalancer))
    suite.addTests(loader.loadTestsFromTestCase(TestUsageAnalyzer))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    logger.info(
        "بدء الاختبارات التكاملية لنظام إدارة وكلاء الذكاء الاصطناعي المتعدد")
    result = run_tests()

    if result.wasSuccessful():
        logger.info("تم اجتياز جميع الاختبارات بنجاح")
        sys.exit(0)
    else:
        logger.error("فشلت %s اختبارات", len(result.failures) + len(result.errors))
        sys.exit(1)
