# File: /home/ubuntu/clean_project/src/api/generative_ai.py

"""
API للذكاء الاصطناعي التوليدي
يوفر نقاط نهاية لجميع وظائف الذكاء الاصطناعي التوليدي
"""

from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
import logging
import json
from datetime import datetime
import base64
import io
from PIL import Image
import traceback

# استيراد الخدمات
try:
    from ..modules.ai_management.generative_ai_service import GenerativeAIService
    from ..core.auth import require_auth, get_current_user
    from ..core.error_handling import APIError, handle_api_error
except ImportError as e:
    logging.warning(f"Import error in generative_ai.py: {e}")
    # Fallback imports for development
    GenerativeAIService = None

# إنشاء Blueprint
generative_ai_bp = Blueprint('generative_ai', __name__, url_prefix='/api/generative-ai')

# تهيئة الخدمة
generative_service = None

def init_generative_service():
    """تهيئة خدمة الذكاء الاصطناعي التوليدي"""
    global generative_service
    if GenerativeAIService and not generative_service:
        try:
            generative_service = GenerativeAIService()
            logging.info("Generative AI service initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize generative AI service: {e}")
            generative_service = None

@generative_ai_bp.before_request
def before_request():
    """تهيئة الخدمة قبل كل طلب"""
    init_generative_service()

# ==================== LLM APIs ====================

@generative_ai_bp.route('/llm/chat', methods=['POST'])
@cross_origin()
@require_auth
def llm_chat():
    """
    محادثة مع النماذج اللغوية الكبيرة
    """
    try:
        data = request.get_json()
        if not data:
            raise APIError("No data provided", 400)
        
        message = data.get('message', '').strip()
        model = data.get('model', 'gpt-4')
        context = data.get('context', [])
        user_id = get_current_user()['id']
        
        if not message:
            raise APIError("Message is required", 400)
        
        if not generative_service:
            # Fallback response for development
            return jsonify({
                'success': True,
                'response': f"تم استلام رسالتك: {message}. سيتم الرد عليها قريباً باستخدام نموذج {model}.",
                'model_used': model,
                'timestamp': datetime.now().isoformat(),
                'tokens_used': len(message.split()) * 2
            })
        
        # استخدام الخدمة الحقيقية
        response = generative_service.chat_with_llm(
            message=message,
            model=model,
            context=context,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'response': response['response'],
            'model_used': response['model'],
            'timestamp': response['timestamp'],
            'tokens_used': response.get('tokens_used', 0),
            'confidence': response.get('confidence', 0.95)
        })
        
    except APIError:
        raise
    except Exception as e:
        logging.error(f"Error in LLM chat: {e}")
        logging.error(traceback.format_exc())
        raise APIError(f"Internal server error: {str(e)}", 500)

@generative_ai_bp.route('/llm/models', methods=['GET'])
@cross_origin()
@require_auth
def get_llm_models():
    """
    الحصول على قائمة النماذج اللغوية المتاحة
    """
    try:
        if not generative_service:
            # Fallback response
            return jsonify({
                'success': True,
                'models': [
                    {
                        'id': 'gpt-4',
                        'name': 'GPT-4',
                        'description': 'نموذج متقدم للمحادثة والتحليل',
                        'type': 'cloud',
                        'status': 'available',
                        'capabilities': ['chat', 'analysis', 'code']
                    },
                    {
                        'id': 'local-llm',
                        'name': 'نموذج محلي',
                        'description': 'نموذج محلي مجاني',
                        'type': 'local',
                        'status': 'available',
                        'capabilities': ['chat', 'basic_analysis']
                    },
                    {
                        'id': 'codex',
                        'name': 'Codex',
                        'description': 'نموذج متخصص في البرمجة',
                        'type': 'cloud',
                        'status': 'available',
                        'capabilities': ['code', 'automation']
                    }
                ]
            })
        
        models = generative_service.get_available_models()
        return jsonify({
            'success': True,
            'models': models
        })
        
    except Exception as e:
        logging.error(f"Error getting LLM models: {e}")
        raise APIError(f"Failed to get models: {str(e)}", 500)

@generative_ai_bp.route('/llm/switch-model', methods=['POST'])
@cross_origin()
@require_auth
def switch_llm_model():
    """
    تبديل النموذج اللغوي
    """
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        user_id = get_current_user()['id']
        
        if not model_id:
            raise APIError("Model ID is required", 400)
        
        if not generative_service:
            return jsonify({
                'success': True,
                'message': f'تم تبديل النموذج إلى {model_id}',
                'model': model_id
            })
        
        result = generative_service.switch_model(model_id, user_id)
        
        return jsonify({
            'success': True,
            'message': result['message'],
            'model': result['model']
        })
        
    except APIError:
        raise
    except Exception as e:
        logging.error(f"Error switching LLM model: {e}")
        raise APIError(f"Failed to switch model: {str(e)}", 500)

# ==================== Image Generation APIs ====================

@generative_ai_bp.route('/image/generate', methods=['POST'])
@cross_origin()
@require_auth
def generate_image():
    """
    توليد الصور باستخدام الذكاء الاصطناعي
    """
    try:
        data = request.get_json()
        if not data:
            raise APIError("No data provided", 400)
        
        prompt = data.get('prompt', '').strip()
        model = data.get('model', 'dalle-3')
        style = data.get('style', 'realistic')
        quality = data.get('quality', 'hd')
        size = data.get('size', '1024x1024')
        user_id = get_current_user()['id']
        
        if not prompt:
            raise APIError("Prompt is required", 400)
        
        if not generative_service:
            # Fallback response
            return jsonify({
                'success': True,
                'image_id': f'img_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'image_url': '/api/placeholder/512/512',
                'prompt': prompt,
                'model': model,
                'style': style,
                'quality': quality,
                'timestamp': datetime.now().isoformat(),
                'status': 'generated'
            })
        
        result = generative_service.generate_image(
            prompt=prompt,
            model=model,
            style=style,
            quality=quality,
            size=size,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'image_id': result['image_id'],
            'image_url': result['image_url'],
            'prompt': result['prompt'],
            'model': result['model'],
            'style': result['style'],
            'quality': result['quality'],
            'timestamp': result['timestamp'],
            'status': result['status']
        })
        
    except APIError:
        raise
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        logging.error(traceback.format_exc())
        raise APIError(f"Failed to generate image: {str(e)}", 500)

@generative_ai_bp.route('/image/enhance', methods=['POST'])
@cross_origin()
@require_auth
def enhance_image():
    """
    تحسين الصور باستخدام تقنيات Diffusion
    """
    try:
        data = request.get_json()
        if not data:
            raise APIError("No data provided", 400)
        
        image_data = data.get('image_data')
        enhancement_type = data.get('enhancement_type', 'quality')
        strength = data.get('strength', 0.7)
        user_id = get_current_user()['id']
        
        if not image_data:
            raise APIError("Image data is required", 400)
        
        if not generative_service:
            return jsonify({
                'success': True,
                'enhanced_image_url': '/api/placeholder/512/512',
                'enhancement_type': enhancement_type,
                'strength': strength,
                'timestamp': datetime.now().isoformat()
            })
        
        result = generative_service.enhance_image(
            image_data=image_data,
            enhancement_type=enhancement_type,
            strength=strength,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'enhanced_image_url': result['enhanced_image_url'],
            'enhancement_type': result['enhancement_type'],
            'strength': result['strength'],
            'timestamp': result['timestamp']
        })
        
    except APIError:
        raise
    except Exception as e:
        logging.error(f"Error enhancing image: {e}")
        raise APIError(f"Failed to enhance image: {str(e)}", 500)

@generative_ai_bp.route('/image/variations', methods=['POST'])
@cross_origin()
@require_auth
def create_image_variations():
    """
    إنشاء تنويعات للصور
    """
    try:
        data = request.get_json()
        if not data:
            raise APIError("No data provided", 400)
        
        image_data = data.get('image_data')
        num_variations = data.get('num_variations', 3)
        variation_strength = data.get('variation_strength', 0.5)
        user_id = get_current_user()['id']
        
        if not image_data:
            raise APIError("Image data is required", 400)
        
        if not generative_service:
            variations = []
            for i in range(num_variations):
                variations.append({
                    'variation_id': f'var_{i+1}_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                    'image_url': f'/api/placeholder/512/512?v={i+1}',
                    'variation_index': i + 1
                })
            
            return jsonify({
                'success': True,
                'variations': variations,
                'num_variations': num_variations,
                'timestamp': datetime.now().isoformat()
            })
        
        result = generative_service.create_image_variations(
            image_data=image_data,
            num_variations=num_variations,
            variation_strength=variation_strength,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'variations': result['variations'],
            'num_variations': result['num_variations'],
            'timestamp': result['timestamp']
        })
        
    except APIError:
        raise
    except Exception as e:
        logging.error(f"Error creating image variations: {e}")
        raise APIError(f"Failed to create variations: {str(e)}", 500)

# ==================== Memory APIs ====================

@generative_ai_bp.route('/memory/store', methods=['POST'])
@cross_origin()
@require_auth
def store_memory():
    """
    تخزين ذاكرة جديدة
    """
    try:
        data = request.get_json()
        if not data:
            raise APIError("No data provided", 400)
        
        content = data.get('content')
        memory_type = data.get('type', 'short_term')
        context = data.get('context', {})
        user_id = get_current_user()['id']
        
        if not content:
            raise APIError("Content is required", 400)
        
        if not generative_service:
            return jsonify({
                'success': True,
                'memory_id': f'mem_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'message': 'تم تخزين الذاكرة بنجاح',
                'timestamp': datetime.now().isoformat()
            })
        
        result = generative_service.store_memory(
            content=content,
            memory_type=memory_type,
            context=context,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'memory_id': result['memory_id'],
            'message': result['message'],
            'timestamp': result['timestamp']
        })
        
    except APIError:
        raise
    except Exception as e:
        logging.error(f"Error storing memory: {e}")
        raise APIError(f"Failed to store memory: {str(e)}", 500)

@generative_ai_bp.route('/memory/retrieve', methods=['POST'])
@cross_origin()
@require_auth
def retrieve_memory():
    """
    استرجاع الذاكرة
    """
    try:
        data = request.get_json()
        query = data.get('query', '') if data else ''
        memory_type = data.get('type', 'all') if data else 'all'
        limit = data.get('limit', 10) if data else 10
        user_id = get_current_user()['id']
        
        if not generative_service:
            return jsonify({
                'success': True,
                'memories': [
                    {
                        'memory_id': 'mem_001',
                        'content': 'ذاكرة تجريبية للاختبار',
                        'type': 'short_term',
                        'relevance': 0.95,
                        'timestamp': datetime.now().isoformat()
                    }
                ],
                'total_count': 1
            })
        
        result = generative_service.retrieve_memory(
            query=query,
            memory_type=memory_type,
            limit=limit,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'memories': result['memories'],
            'total_count': result['total_count']
        })
        
    except APIError:
        raise
    except Exception as e:
        logging.error(f"Error retrieving memory: {e}")
        raise APIError(f"Failed to retrieve memory: {str(e)}", 500)

# ==================== Analytics APIs ====================

@generative_ai_bp.route('/analytics/usage', methods=['GET'])
@cross_origin()
@require_auth
def get_usage_analytics():
    """
    الحصول على إحصائيات الاستخدام
    """
    try:
        user_id = get_current_user()['id']
        period = request.args.get('period', 'week')
        
        if not generative_service:
            return jsonify({
                'success': True,
                'analytics': {
                    'total_requests': 150,
                    'llm_requests': 100,
                    'image_generations': 30,
                    'memory_operations': 20,
                    'tokens_used': 15000,
                    'images_generated': 30,
                    'period': period,
                    'timestamp': datetime.now().isoformat()
                }
            })
        
        analytics = generative_service.get_usage_analytics(user_id, period)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        logging.error(f"Error getting usage analytics: {e}")
        raise APIError(f"Failed to get analytics: {str(e)}", 500)

@generative_ai_bp.route('/analytics/performance', methods=['GET'])
@cross_origin()
@require_auth
def get_performance_metrics():
    """
    الحصول على مقاييس الأداء
    """
    try:
        if not generative_service:
            return jsonify({
                'success': True,
                'performance': {
                    'average_response_time': 2.5,
                    'success_rate': 98.5,
                    'model_accuracy': 94.2,
                    'system_load': 65.3,
                    'active_models': 3,
                    'timestamp': datetime.now().isoformat()
                }
            })
        
        performance = generative_service.get_performance_metrics()
        
        return jsonify({
            'success': True,
            'performance': performance
        })
        
    except Exception as e:
        logging.error(f"Error getting performance metrics: {e}")
        raise APIError(f"Failed to get performance metrics: {str(e)}", 500)

# ==================== Error Handlers ====================

@generative_ai_bp.errorhandler(APIError)
def handle_api_error_in_generative(error):
    """معالج أخطاء API"""
    return handle_api_error(error)

@generative_ai_bp.errorhandler(Exception)
def handle_general_error_in_generative(error):
    """معالج الأخطاء العامة"""
    logging.error(f"Unhandled error in generative AI API: {error}")
    logging.error(traceback.format_exc())
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'حدث خطأ داخلي في الخادم'
    }), 500

# ==================== Health Check ====================

@generative_ai_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """فحص صحة API الذكاء الاصطناعي التوليدي"""
    try:
        status = {
            'service': 'Generative AI API',
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        if generative_service:
            service_status = generative_service.health_check()
            status.update(service_status)
        else:
            status['status'] = 'limited'
            status['message'] = 'Service running in fallback mode'
        
        return jsonify(status)
        
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({
            'service': 'Generative AI API',
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# تصدير Blueprint
__all__ = ['generative_ai_bp']

