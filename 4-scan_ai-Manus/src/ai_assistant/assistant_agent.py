#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Assistant Agent for Agricultural AI System.
Provides question answering, file management, and interactive assistance.
"""

import os
import sys
import json
import logging
import datetime
import uuid
import base64
import requests
from typing import Dict, List, Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ai_assistant')


class AIAssistantAgent:
    """
    AI Assistant Agent for the Agricultural AI System.
    Provides question answering, file management, and interactive assistance.
    Features a pharaoh-themed appearance that evolves with learning.
    """
    
    def __init__(self, config_path: str, database_manager=None, audit_manager=None, 
                 auth_manager=None, knowledge_base=None):
        """
        Initialize the AI Assistant Agent.
        
        Args:
            config_path: Path to configuration file
            database_manager: Database manager instance
            audit_manager: Audit manager instance
            auth_manager: Authentication manager instance
            knowledge_base: Knowledge base instance
        """
        self.config_path = config_path
        self.database_manager = database_manager
        self.audit_manager = audit_manager
        self.auth_manager = auth_manager
        self.knowledge_base = knowledge_base
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize data directories
        self._init_directories()
        
        # Initialize assistant state
        self.assistant_state = self._load_assistant_state()
        
        logger.info("AI Assistant Agent initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Get AI assistant specific config
            if 'ai_assistant' not in config:
                config['ai_assistant'] = {
                    'data_dir': os.path.join(os.path.dirname(self.config_path), '../data/ai_assistant'),
                    'files_dir': os.path.join(os.path.dirname(self.config_path), '../data/ai_assistant/files'),
                    'conversations_dir': os.path.join(os.path.dirname(self.config_path), '../data/ai_assistant/conversations'),
                    'assets_dir': os.path.join(os.path.dirname(self.config_path), '../data/ai_assistant/assets'),
                    'free_tier': {
                        'enabled': True,
                        'max_questions_per_day': 10,
                        'max_file_size_mb': 5,
                        'features': ['basic_questions', 'crop_identification']
                    },
                    'paid_tier': {
                        'enabled': True,
                        'features': ['advanced_questions', 'crop_identification', 'disease_diagnosis', 
                                    'treatment_recommendations', 'variety_comparison', 'file_management']
                    },
                    'pharaoh_evolution': {
                        'levels': [
                            {
                                'level': 1,
                                'name': 'Novice Pharaoh',
                                'description': 'A young pharaoh just beginning to learn about agriculture',
                                'min_interactions': 0,
                                'avatar': 'pharaoh_level1.png'
                            },
                            {
                                'level': 2,
                                'name': 'Apprentice Pharaoh',
                                'description': 'A pharaoh with growing knowledge of crops and farming',
                                'min_interactions': 50,
                                'avatar': 'pharaoh_level2.png'
                            },
                            {
                                'level': 3,
                                'name': 'Adept Pharaoh',
                                'description': 'A pharaoh with substantial agricultural wisdom',
                                'min_interactions': 200,
                                'avatar': 'pharaoh_level3.png'
                            },
                            {
                                'level': 4,
                                'name': 'Master Pharaoh',
                                'description': 'A pharaoh with extensive knowledge of all agricultural matters',
                                'min_interactions': 500,
                                'avatar': 'pharaoh_level4.png'
                            },
                            {
                                'level': 5,
                                'name': 'Sage Pharaoh',
                                'description': 'A legendary pharaoh with unparalleled agricultural wisdom',
                                'min_interactions': 1000,
                                'avatar': 'pharaoh_level5.png'
                            }
                        ]
                    },
                    'api_keys': {
                        'openai': '${OPENAI_API_KEY}',
                        'google': '${GOOGLE_API_KEY}'
                    }
                }
                
                # Save updated config
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
            
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Return default configuration
            return {
                'ai_assistant': {
                    'data_dir': os.path.join(os.path.dirname(self.config_path), '../data/ai_assistant'),
                    'files_dir': os.path.join(os.path.dirname(self.config_path), '../data/ai_assistant/files'),
                    'conversations_dir': os.path.join(os.path.dirname(self.config_path), '../data/ai_assistant/conversations'),
                    'assets_dir': os.path.join(os.path.dirname(self.config_path), '../data/ai_assistant/assets'),
                    'free_tier': {
                        'enabled': True,
                        'max_questions_per_day': 10,
                        'max_file_size_mb': 5,
                        'features': ['basic_questions', 'crop_identification']
                    },
                    'paid_tier': {
                        'enabled': True,
                        'features': ['advanced_questions', 'crop_identification', 'disease_diagnosis', 
                                    'treatment_recommendations', 'variety_comparison', 'file_management']
                    },
                    'pharaoh_evolution': {
                        'levels': [
                            {
                                'level': 1,
                                'name': 'Novice Pharaoh',
                                'description': 'A young pharaoh just beginning to learn about agriculture',
                                'min_interactions': 0,
                                'avatar': 'pharaoh_level1.png'
                            },
                            {
                                'level': 2,
                                'name': 'Apprentice Pharaoh',
                                'description': 'A pharaoh with growing knowledge of crops and farming',
                                'min_interactions': 50,
                                'avatar': 'pharaoh_level2.png'
                            },
                            {
                                'level': 3,
                                'name': 'Adept Pharaoh',
                                'description': 'A pharaoh with substantial agricultural wisdom',
                                'min_interactions': 200,
                                'avatar': 'pharaoh_level3.png'
                            },
                            {
                                'level': 4,
                                'name': 'Master Pharaoh',
                                'description': 'A pharaoh with extensive knowledge of all agricultural matters',
                                'min_interactions': 500,
                                'avatar': 'pharaoh_level4.png'
                            },
                            {
                                'level': 5,
                                'name': 'Sage Pharaoh',
                                'description': 'A legendary pharaoh with unparalleled agricultural wisdom',
                                'min_interactions': 1000,
                                'avatar': 'pharaoh_level5.png'
                            }
                        ]
                    },
                    'api_keys': {
                        'openai': '${OPENAI_API_KEY}',
                        'google': '${GOOGLE_API_KEY}'
                    }
                }
            }
    
    def _init_directories(self):
        """Initialize required directories."""
        os.makedirs(self.config['ai_assistant']['data_dir'], exist_ok=True)
        os.makedirs(self.config['ai_assistant']['files_dir'], exist_ok=True)
        os.makedirs(self.config['ai_assistant']['conversations_dir'], exist_ok=True)
        os.makedirs(self.config['ai_assistant']['assets_dir'], exist_ok=True)
        
        # Create user-specific directories
        if self.database_manager:
            try:
                # Get all users
                result = self.database_manager.query_data(
                    table='users',
                    condition=""
                )
                
                if result.get('success', False) and result.get('data'):
                    for user in result['data']:
                        user_id = user.get('id')
                        if user_id:
                            os.makedirs(os.path.join(self.config['ai_assistant']['files_dir'], user_id), exist_ok=True)
                            os.makedirs(os.path.join(self.config['ai_assistant']['conversations_dir'], user_id), exist_ok=True)
            except Exception as e:
                logger.error(f"Error creating user directories: {e}")
    
    def _load_assistant_state(self) -> Dict[str, Any]:
        """Load assistant state from file."""
        state_file = os.path.join(self.config['ai_assistant']['data_dir'], 'assistant_state.json')
        
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading assistant state: {e}")
        
        # Initialize default state
        default_state = {
            'total_interactions': 0,
            'questions_answered': 0,
            'files_processed': 0,
            'current_level': 1,
            'last_updated': datetime.datetime.now().isoformat(),
            'user_interactions': {}
        }
        
        # Save default state
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(default_state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving default assistant state: {e}")
        
        return default_state
    
    def _save_assistant_state(self):
        """Save assistant state to file."""
        state_file = os.path.join(self.config['ai_assistant']['data_dir'], 'assistant_state.json')
        
        try:
            # Update timestamp
            self.assistant_state['last_updated'] = datetime.datetime.now().isoformat()
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(self.assistant_state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving assistant state: {e}")
    
    def _update_interaction_count(self, user_id: str):
        """
        Update interaction count for a user and check for level up.
        
        Args:
            user_id: ID of the user
        """
        # Update total interactions
        self.assistant_state['total_interactions'] += 1
        
        # Update user interactions
        if user_id not in self.assistant_state['user_interactions']:
            self.assistant_state['user_interactions'][user_id] = {
                'interactions': 0,
                'questions_asked': 0,
                'files_uploaded': 0,
                'files_downloaded': 0,
                'last_interaction': datetime.datetime.now().isoformat()
            }
        
        self.assistant_state['user_interactions'][user_id]['interactions'] += 1
        self.assistant_state['user_interactions'][user_id]['last_interaction'] = datetime.datetime.now().isoformat()
        
        # Check for level up
        current_level = self.assistant_state['current_level']
        total_interactions = self.assistant_state['total_interactions']
        
        # Get pharaoh evolution levels
        levels = self.config['ai_assistant']['pharaoh_evolution']['levels']
        
        # Find the appropriate level based on interactions
        new_level = current_level
        for level in levels:
            if total_interactions >= level['min_interactions']:
                new_level = level['level']
        
        # Level up if needed
        if new_level > current_level:
            self.assistant_state['current_level'] = new_level
            logger.info(f"Assistant leveled up to {new_level}")
        
        # Save state
        self._save_assistant_state()
    
    def get_current_level_info(self) -> Dict[str, Any]:
        """
        Get information about the current pharaoh level.
        
        Returns:
            Dictionary with level information
        """
        current_level = self.assistant_state['current_level']
        
        # Get pharaoh evolution levels
        levels = self.config['ai_assistant']['pharaoh_evolution']['levels']
        
        # Find the current level info
        for level in levels:
            if level['level'] == current_level:
                return level
        
        # Return default level if not found
        return levels[0]
    
    def check_user_access(self, user_info: Dict[str, Any], feature: str) -> Dict[str, Any]:
        """
        Check if a user has access to a specific feature.
        
        Args:
            user_info: Information about the user
            feature: Feature to check access for
            
        Returns:
            Dictionary with access information
        """
        try:
            # Admin users have access to all features
            if user_info.get('role') == 'admin':
                return {
                    'success': True,
                    'has_access': True,
                    'tier': 'admin'
                }
            
            # Check if user has paid access
            has_paid_access = False
            if self.database_manager:
                result = self.database_manager.query_data(
                    table='user_subscriptions',
                    condition=f"user_id = '{user_info.get('id')}' AND status = 'active'"
                )
                
                if result.get('success', False) and result.get('data'):
                    has_paid_access = True
            
            # Determine tier
            tier = 'paid' if has_paid_access else 'free'
            
            # Check if feature is available in tier
            tier_config = self.config['ai_assistant']['paid_tier'] if has_paid_access else self.config['ai_assistant']['free_tier']
            
            if feature in tier_config.get('features', []):
                # For free tier, check daily question limit
                if not has_paid_access and feature == 'basic_questions':
                    # Get today's date
                    today = datetime.datetime.now().date().isoformat()
                    
                    # Get user interactions
                    user_id = user_info.get('id')
                    if user_id in self.assistant_state['user_interactions']:
                        user_data = self.assistant_state['user_interactions'][user_id]
                        
                        # Check if we have today's question count
                        if 'daily_questions' not in user_data:
                            user_data['daily_questions'] = {}
                        
                        if today not in user_data['daily_questions']:
                            user_data['daily_questions'][today] = 0
                        
                        # Check if user has reached daily limit
                        max_questions = self.config['ai_assistant']['free_tier'].get('max_questions_per_day', 10)
                        if user_data['daily_questions'][today] >= max_questions:
                            return {
                                'success': True,
                                'has_access': False,
                                'tier': tier,
                                'reason': f"Daily question limit reached ({max_questions})"
                            }
                
                return {
                    'success': True,
                    'has_access': True,
                    'tier': tier
                }
            else:
                return {
                    'success': True,
                    'has_access': False,
                    'tier': tier,
                    'reason': f"Feature '{feature}' not available in {tier} tier"
                }
            
        except Exception as e:
            logger.error(f"Error checking user access: {e}")
            return {
                'success': False,
                'error': f"Error checking user access: {str(e)}"
            }
    
    def ask_question(self, user_info: Dict[str, Any], question: str, 
                    context_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Ask a question to the AI assistant.
        
        Args:
            user_info: Information about the user
            question: Question text
            context_files: Optional list of file paths to provide as context
            
        Returns:
            Dictionary with answer information
        """
        try:
            # Check user access
            access_result = self.check_user_access(user_info, 'basic_questions')
            
            if not access_result.get('success', False):
                return access_result
            
            if not access_result.get('has_access', False):
                return {
                    'success': False,
                    'error': access_result.get('reason', 'Access denied')
                }
            
            # Update interaction count
            self._update_interaction_count(user_info.get('id'))
            
            # For free tier, increment daily question count
            tier = access_result.get('tier')
            if tier == 'free':
                today = datetime.datetime.now().date().isoformat()
                user_id = user_info.get('id')
                self.assistant_state['user_interactions'][user_id]['daily_questions'][today] += 1
                self._save_assistant_state()
            
            # Generate conversation ID
            conversation_id = str(uuid.uuid4())
            
            # Prepare context
            context = ""
            if context_files:
                for file_path in context_files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            context += f"\nContent from file {os.path.basename(file_path)}:\n{content}\n"
                    except Exception as e:
                        logger.error(f"Error reading context file {file_path}: {e}")
            
            # Get current level info
            level_info = self.get_current_level_info()
            
            # Prepare prompt
            prompt = f"""
            You are {level_info['name']}, an AI assistant specializing in agricultural knowledge.
            {level_info['description']}
            
            Please answer the following question about agriculture:
            
            {question}
            
            {context}
            """
            
            # In a real implementation, this would call an LLM API
            # For this example, we'll simulate a response
            answer = self._simulate_ai_response(question, context, level_info)
            
            # Save conversation
            conversation_data = {
                'id': conversation_id,
                'user_id': user_info.get('id'),
                'question': question,
                'answer': answer,
                'context_files': context_files,
                'timestamp': datetime.datetime.now().isoformat(),
                'assistant_level': level_info['level']
            }
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.insert_data(
                    table='ai_conversations',
                    data=conversation_data
                )
            
            # Save to file system
            user_conversations_dir = os.path.join(
                self.config['ai_assistant']['conversations_dir'],
                user_info.get('id')
            )
            os.makedirs(user_conversations_dir, exist_ok=True)
            
            conversation_file = os.path.join(
                user_conversations_dir,
                f"{conversation_id}.json"
            )
            
            with open(conversation_file, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2)
            
            # Update statistics
            self.assistant_state['questions_answered'] += 1
            self._save_assistant_state()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AI_ASSISTANT",
                    action="ask_question",
                    component="ai_assistant",
                    user_info=user_info,
                    details={"conversation_id": conversation_id},
                    status="success"
                )
            
            return {
                'success': True,
                'conversation_id': conversation_id,
                'answer': answer,
                'assistant_level': level_info['level'],
                'assistant_name': level_info['name'],
                'assistant_avatar': level_info['avatar']
            }
            
        except Exception as e:
            logger.error(f"Error asking question: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AI_ASSISTANT",
                    action="ask_question",
                    component="ai_assistant",
                    user_info=user_info,
                    details={"error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error asking question: {str(e)}"
            }
    
    def _simulate_ai_response(self, question: str, context: str, level_info: Dict[str, Any]) -> str:
        """
        Simulate an AI response for demonstration purposes.
        In a real implementation, this would call an LLM API.
        
        Args:
            question: Question text
            context: Context information
            level_info: Information about the current assistant level
            
        Returns:
            Simulated answer text
        """
        # Simple keyword-based responses for demonstration
        question_lower = question.lower()
        
        if 'disease' in question_lower or 'pest' in question_lower:
            return f"""As {level_info['name']}, I can tell you that plant diseases and pests are a significant challenge in agriculture. 

Common plant diseases include:
1. Powdery mildew - appears as white powdery spots on leaves
2. Rust - appears as orange or brown spots on leaves
3. Blight - causes rapid browning and death of plant tissues
4. Root rot - affects the roots and can cause wilting and death

For accurate diagnosis, it's important to:
- Examine the affected parts closely
- Note the pattern of spread
- Consider environmental conditions
- Check for signs of insects

For treatment, consider:
- Cultural practices like proper spacing and sanitation
- Biological controls
- Chemical treatments as a last resort

Would you like more specific information about a particular disease or pest?"""
            
        elif 'fertilizer' in question_lower or 'nutrient' in question_lower:
            return f"""As {level_info['name']}, I understand the importance of proper plant nutrition. 

Plants require several essential nutrients:
- Macronutrients: Nitrogen (N), Phosphorus (P), Potassium (K), Calcium (Ca), Magnesium (Mg), Sulfur (S)
- Micronutrients: Iron (Fe), Manganese (Mn), Zinc (Zn), Copper (Cu), Boron (B), Molybdenum (Mo), Chlorine (Cl)

Each nutrient plays a specific role:
- Nitrogen: Leaf growth and green color
- Phosphorus: Root and flower development
- Potassium: Overall plant health and disease resistance

Nutrient deficiencies show specific symptoms:
- Nitrogen deficiency: Yellowing of older leaves
- Phosphorus deficiency: Purple coloration of leaves
- Potassium deficiency: Brown scorching along leaf margins

For sustainable fertilization:
- Test your soil before applying fertilizers
- Use organic options when possible
- Apply at the right time and in the right amount
- Consider slow-release formulations

Would you like more specific information about a particular nutrient or fertilization practice?"""
            
        elif 'irrigation' in question_lower or 'water' in question_lower:
            return f"""As {level_info['name']}, I can share that water management is crucial for successful agriculture.

Effective irrigation methods include:
1. Drip irrigation - highly efficient, delivers water directly to plant roots
2. Sprinkler systems - good for larger areas, but less water-efficient
3. Flood irrigation - traditional method, uses more water
4. Subsurface irrigation - reduces evaporation and weed growth

For optimal irrigation:
- Water deeply but infrequently to encourage deep root growth
- Water early in the morning to reduce evaporation
- Monitor soil moisture using sensors or manual checks
- Adjust watering based on weather conditions and plant growth stage

Water conservation techniques:
- Mulching to reduce evaporation
- Rainwater harvesting
- Drought-resistant crop varieties
- Precision irrigation technologies

Would you like more specific information about a particular irrigation method or water conservation technique?"""
            
        elif 'crop rotation' in question_lower or 'planting schedule' in question_lower:
            return f"""As {level_info['name']}, I can tell you that crop rotation is an ancient and effective agricultural practice.

Benefits of crop rotation:
1. Disrupts pest and disease cycles
2. Improves soil structure and fertility
3. Reduces soil erosion
4. Manages nutrient requirements
5. Increases biodiversity

Basic principles for effective rotation:
- Alternate between different plant families
- Rotate between deep and shallow-rooted crops
- Include nitrogen-fixing legumes in the rotation
- Consider nutrient demands of different crops

Example rotation sequence:
Year 1: Legumes (beans, peas)
Year 2: Leaf crops (lettuce, cabbage)
Year 3: Fruit crops (tomatoes, peppers)
Year 4: Root crops (carrots, onions)

For planning rotations:
- Keep detailed records of what was planted where
- Consider companion planting within rotations
- Adjust based on your specific climate and soil conditions

Would you like more specific information about rotating particular crops or designing a rotation plan?"""
            
        else:
            return f"""As {level_info['name']}, I'm here to help with your agricultural questions.

Your question about "{question}" touches on an important agricultural topic. 

In agriculture, success depends on understanding the complex interactions between plants, soil, climate, and management practices. Each farm or garden is unique, with its own set of challenges and opportunities.

For the best results:
- Observe your plants regularly
- Keep records of what works and what doesn't
- Learn from local agricultural experts
- Adapt practices to your specific conditions
- Embrace sustainable methods that work with nature

If you could provide more specific details about your situation, I'd be happy to offer more targeted advice. Feel free to ask follow-up questions or provide more context about your agricultural needs."""
    
    def upload_file(self, user_info: Dict[str, Any], file_path: str, 
                   file_name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to the AI assistant.
        
        Args:
            user_info: Information about the user
            file_path: Path to the file to upload
            file_name: Optional custom name for the file
            description: Optional description of the file
            
        Returns:
            Dictionary with upload result
        """
        try:
            # Check user access
            access_result = self.check_user_access(user_info, 'file_management')
            
            if not access_result.get('success', False):
                return access_result
            
            if not access_result.get('has_access', False):
                return {
                    'success': False,
                    'error': access_result.get('reason', 'Access denied')
                }
            
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': f"File not found: {file_path}"
                }
            
            # Check file size for free tier
            tier = access_result.get('tier')
            if tier == 'free':
                max_size_mb = self.config['ai_assistant']['free_tier'].get('max_file_size_mb', 5)
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                
                if file_size_mb > max_size_mb:
                    return {
                        'success': False,
                        'error': f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed for free tier ({max_size_mb} MB)"
                    }
            
            # Generate file ID
            file_id = str(uuid.uuid4())
            
            # Get original file name if not provided
            if not file_name:
                file_name = os.path.basename(file_path)
            
            # Get file extension
            _, ext = os.path.splitext(file_path)
            
            # Create user files directory
            user_files_dir = os.path.join(
                self.config['ai_assistant']['files_dir'],
                user_info.get('id')
            )
            os.makedirs(user_files_dir, exist_ok=True)
            
            # Destination path
            dest_path = os.path.join(user_files_dir, f"{file_id}{ext}")
            
            # Copy file
            import shutil
            shutil.copy2(file_path, dest_path)
            
            # Create file metadata
            file_data = {
                'id': file_id,
                'user_id': user_info.get('id'),
                'original_name': file_name,
                'path': dest_path,
                'extension': ext,
                'size_bytes': os.path.getsize(dest_path),
                'description': description or '',
                'uploaded_at': datetime.datetime.now().isoformat(),
                'is_public': False
            }
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.insert_data(
                    table='ai_assistant_files',
                    data=file_data
                )
            
            # Save metadata to file
            metadata_file = os.path.join(user_files_dir, f"{file_id}.json")
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(file_data, f, indent=2)
            
            # Update interaction count
            self._update_interaction_count(user_info.get('id'))
            
            # Update statistics
            self.assistant_state['files_processed'] += 1
            if user_info.get('id') in self.assistant_state['user_interactions']:
                self.assistant_state['user_interactions'][user_info.get('id')]['files_uploaded'] += 1
            self._save_assistant_state()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AI_ASSISTANT",
                    action="upload_file",
                    component="ai_assistant",
                    user_info=user_info,
                    details={"file_id": file_id, "original_name": file_name},
                    status="success"
                )
            
            return {
                'success': True,
                'file_id': file_id,
                'message': f"File '{file_name}' uploaded successfully"
            }
            
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AI_ASSISTANT",
                    action="upload_file",
                    component="ai_assistant",
                    user_info=user_info,
                    details={"error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error uploading file: {str(e)}"
            }
    
    def download_file(self, user_info: Dict[str, Any], file_id: str) -> Dict[str, Any]:
        """
        Download a file from the AI assistant.
        
        Args:
            user_info: Information about the user
            file_id: ID of the file to download
            
        Returns:
            Dictionary with download result
        """
        try:
            # Check user access
            access_result = self.check_user_access(user_info, 'file_management')
            
            if not access_result.get('success', False):
                return access_result
            
            if not access_result.get('has_access', False):
                return {
                    'success': False,
                    'error': access_result.get('reason', 'Access denied')
                }
            
            # Get file metadata
            user_files_dir = os.path.join(
                self.config['ai_assistant']['files_dir'],
                user_info.get('id')
            )
            
            metadata_file = os.path.join(user_files_dir, f"{file_id}.json")
            
            if not os.path.exists(metadata_file):
                # Check if it's a public file from another user
                if self.database_manager:
                    result = self.database_manager.query_data(
                        table='ai_assistant_files',
                        condition=f"id = '{file_id}' AND is_public = TRUE"
                    )
                    
                    if result.get('success', False) and result.get('data'):
                        file_data = result['data'][0]
                        file_path = file_data['path']
                        
                        if os.path.exists(file_path):
                            # Update interaction count
                            self._update_interaction_count(user_info.get('id'))
                            
                            # Update statistics
                            if user_info.get('id') in self.assistant_state['user_interactions']:
                                self.assistant_state['user_interactions'][user_info.get('id')]['files_downloaded'] += 1
                            self._save_assistant_state()
                            
                            # Log the action
                            if self.audit_manager:
                                self.audit_manager.log_action(
                                    action_type="AI_ASSISTANT",
                                    action="download_file",
                                    component="ai_assistant",
                                    user_info=user_info,
                                    details={"file_id": file_id, "original_name": file_data['original_name']},
                                    status="success"
                                )
                            
                            return {
                                'success': True,
                                'file_path': file_path,
                                'file_name': file_data['original_name'],
                                'message': f"File '{file_data['original_name']}' downloaded successfully"
                            }
                
                return {
                    'success': False,
                    'error': f"File with ID '{file_id}' not found"
                }
            
            with open(metadata_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            
            # Check if file exists
            file_path = file_data['path']
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': f"File not found: {file_path}"
                }
            
            # Update interaction count
            self._update_interaction_count(user_info.get('id'))
            
            # Update statistics
            if user_info.get('id') in self.assistant_state['user_interactions']:
                self.assistant_state['user_interactions'][user_info.get('id')]['files_downloaded'] += 1
            self._save_assistant_state()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AI_ASSISTANT",
                    action="download_file",
                    component="ai_assistant",
                    user_info=user_info,
                    details={"file_id": file_id, "original_name": file_data['original_name']},
                    status="success"
                )
            
            return {
                'success': True,
                'file_path': file_path,
                'file_name': file_data['original_name'],
                'message': f"File '{file_data['original_name']}' downloaded successfully"
            }
            
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AI_ASSISTANT",
                    action="download_file",
                    component="ai_assistant",
                    user_info=user_info,
                    details={"file_id": file_id, "error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error downloading file: {str(e)}"
            }
    
    def list_files(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        List files uploaded by a user.
        
        Args:
            user_info: Information about the user
            
        Returns:
            Dictionary with list of files
        """
        try:
            # Check user access
            access_result = self.check_user_access(user_info, 'file_management')
            
            if not access_result.get('success', False):
                return access_result
            
            if not access_result.get('has_access', False):
                return {
                    'success': False,
                    'error': access_result.get('reason', 'Access denied')
                }
            
            # Get user files directory
            user_files_dir = os.path.join(
                self.config['ai_assistant']['files_dir'],
                user_info.get('id')
            )
            
            if not os.path.exists(user_files_dir):
                return {
                    'success': True,
                    'files': []
                }
            
            # Get metadata files
            metadata_files = [f for f in os.listdir(user_files_dir) if f.endswith('.json')]
            
            files = []
            for metadata_file in metadata_files:
                file_path = os.path.join(user_files_dir, metadata_file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                # Check if actual file exists
                if os.path.exists(file_data['path']):
                    files.append({
                        'id': file_data['id'],
                        'name': file_data['original_name'],
                        'size_bytes': file_data['size_bytes'],
                        'uploaded_at': file_data['uploaded_at'],
                        'description': file_data['description'],
                        'is_public': file_data['is_public']
                    })
            
            return {
                'success': True,
                'files': files
            }
            
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return {
                'success': False,
                'error': f"Error listing files: {str(e)}"
            }
    
    def get_conversation_history(self, user_info: Dict[str, Any], 
                               limit: Optional[int] = 10) -> Dict[str, Any]:
        """
        Get conversation history for a user.
        
        Args:
            user_info: Information about the user
            limit: Optional maximum number of conversations to return
            
        Returns:
            Dictionary with conversation history
        """
        try:
            # Get user conversations directory
            user_conversations_dir = os.path.join(
                self.config['ai_assistant']['conversations_dir'],
                user_info.get('id')
            )
            
            if not os.path.exists(user_conversations_dir):
                return {
                    'success': True,
                    'conversations': []
                }
            
            # Get conversation files
            conversation_files = [f for f in os.listdir(user_conversations_dir) if f.endswith('.json')]
            
            # Sort by modification time (newest first)
            conversation_files.sort(key=lambda x: os.path.getmtime(os.path.join(user_conversations_dir, x)), reverse=True)
            
            # Apply limit
            if limit:
                conversation_files = conversation_files[:limit]
            
            conversations = []
            for conversation_file in conversation_files:
                file_path = os.path.join(user_conversations_dir, conversation_file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    conversation_data = json.load(f)
                
                conversations.append({
                    'id': conversation_data['id'],
                    'question': conversation_data['question'],
                    'answer': conversation_data['answer'],
                    'timestamp': conversation_data['timestamp'],
                    'assistant_level': conversation_data['assistant_level']
                })
            
            return {
                'success': True,
                'conversations': conversations
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return {
                'success': False,
                'error': f"Error getting conversation history: {str(e)}"
            }
    
    def get_assistant_stats(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get statistics about the AI assistant.
        
        Args:
            user_info: Information about the user
            
        Returns:
            Dictionary with assistant statistics
        """
        try:
            # Check if user is admin
            if user_info.get('role') != 'admin':
                # Return limited stats for non-admin users
                user_id = user_info.get('id')
                user_stats = {}
                
                if user_id in self.assistant_state['user_interactions']:
                    user_stats = self.assistant_state['user_interactions'][user_id]
                
                # Get current level info
                level_info = self.get_current_level_info()
                
                return {
                    'success': True,
                    'current_level': level_info,
                    'user_interactions': user_stats.get('interactions', 0),
                    'user_questions_asked': user_stats.get('questions_asked', 0),
                    'user_files_uploaded': user_stats.get('files_uploaded', 0),
                    'user_files_downloaded': user_stats.get('files_downloaded', 0)
                }
            
            # Full stats for admin users
            return {
                'success': True,
                'total_interactions': self.assistant_state['total_interactions'],
                'questions_answered': self.assistant_state['questions_answered'],
                'files_processed': self.assistant_state['files_processed'],
                'current_level': self.get_current_level_info(),
                'user_count': len(self.assistant_state['user_interactions']),
                'last_updated': self.assistant_state['last_updated']
            }
            
        except Exception as e:
            logger.error(f"Error getting assistant stats: {e}")
            return {
                'success': False,
                'error': f"Error getting assistant stats: {str(e)}"
            }
    
    def get_assistant_avatar(self) -> Dict[str, Any]:
        """
        Get the current avatar for the AI assistant.
        
        Returns:
            Dictionary with avatar information
        """
        try:
            # Get current level info
            level_info = self.get_current_level_info()
            
            # Get avatar path
            avatar_file = level_info['avatar']
            avatar_path = os.path.join(self.config['ai_assistant']['assets_dir'], avatar_file)
            
            # Check if avatar exists
            if not os.path.exists(avatar_path):
                return {
                    'success': False,
                    'error': f"Avatar file not found: {avatar_path}"
                }
            
            return {
                'success': True,
                'avatar_path': avatar_path,
                'level': level_info['level'],
                'name': level_info['name']
            }
            
        except Exception as e:
            logger.error(f"Error getting assistant avatar: {e}")
            return {
                'success': False,
                'error': f"Error getting assistant avatar: {str(e)}"
            }
