"""
FILE: backend/src/api/v1/chatbot.py | PURPOSE: AI Chatbot API for plant care
OWNER: Backend Team | LAST-AUDITED: 2026-01-31

AI Chatbot API - Conversational AI for Plant Care Advice

Provides intelligent responses for plant disease diagnosis, treatment
recommendations, and agricultural best practices.

Version: 1.0.0
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.diagnosis import Diagnosis
from ...models.disease import Disease
from ...models.user import User
from .auth import get_current_user

logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/api/v1/chatbot", tags=["chatbot"])


# ============================================
# Pydantic Schemas
# ============================================

class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request from user"""
    message: str = Field(..., min_length=1, max_length=2000)
    context: Optional[str] = None
    language: str = Field(default="ar", pattern="^(ar|en)$")
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response from AI"""
    success: bool = True
    response: str
    response_ar: Optional[str] = None
    suggestions: List[str] = []
    related_diseases: List[Dict[str, Any]] = []
    conversation_id: str
    timestamp: datetime


class QuickAction(BaseModel):
    """Quick action button for chatbot"""
    id: str
    label: str
    label_ar: str
    action: str


# ============================================
# Knowledge Base
# ============================================

PLANT_CARE_KNOWLEDGE = {
    "tomato": {
        "name": "Tomato",
        "name_ar": "طماطم",
        "common_diseases": ["Early Blight", "Late Blight", "Powdery Mildew"],
        "care_tips": [
            "Water deeply but infrequently",
            "Provide 6-8 hours of sunlight",
            "Use stakes or cages for support"
        ],
        "care_tips_ar": [
            "اسقِ بعمق ولكن بشكل غير متكرر",
            "وفر 6-8 ساعات من ضوء الشمس",
            "استخدم الدعامات أو الأقفاص للدعم"
        ]
    },
    "cucumber": {
        "name": "Cucumber",
        "name_ar": "خيار",
        "common_diseases": ["Downy Mildew", "Powdery Mildew", "Bacterial Wilt"],
        "care_tips": [
            "Keep soil consistently moist",
            "Provide trellis for climbing varieties",
            "Harvest regularly to encourage production"
        ],
        "care_tips_ar": [
            "حافظ على رطوبة التربة باستمرار",
            "وفر تعريشة للأصناف المتسلقة",
            "احصد بانتظام لتشجيع الإنتاج"
        ]
    },
    "pepper": {
        "name": "Pepper",
        "name_ar": "فلفل",
        "common_diseases": ["Bacterial Spot", "Anthracnose", "Mosaic Virus"],
        "care_tips": [
            "Maintain warm temperatures",
            "Avoid overhead watering",
            "Mulch to retain moisture"
        ],
        "care_tips_ar": [
            "حافظ على درجات حرارة دافئة",
            "تجنب الري من الأعلى",
            "استخدم المهاد للحفاظ على الرطوبة"
        ]
    }
}

DISEASE_TREATMENTS = {
    "early_blight": {
        "name": "Early Blight",
        "name_ar": "اللفحة المبكرة",
        "symptoms": "Dark spots with concentric rings on lower leaves",
        "symptoms_ar": "بقع داكنة مع حلقات متحدة المركز على الأوراق السفلية",
        "treatment": [
            "Remove infected leaves immediately",
            "Apply copper-based fungicide",
            "Improve air circulation",
            "Avoid overhead watering"
        ],
        "treatment_ar": [
            "أزل الأوراق المصابة فوراً",
            "طبق مبيد فطري أساسه النحاس",
            "حسّن دوران الهواء",
            "تجنب الري من الأعلى"
        ],
        "prevention": "Rotate crops, use resistant varieties, mulch around plants"
    },
    "powdery_mildew": {
        "name": "Powdery Mildew",
        "name_ar": "البياض الدقيقي",
        "symptoms": "White powdery coating on leaves and stems",
        "symptoms_ar": "طبقة بيضاء مسحوقية على الأوراق والسيقان",
        "treatment": [
            "Apply neem oil or sulfur-based fungicide",
            "Remove severely infected parts",
            "Increase spacing between plants",
            "Water at soil level"
        ],
        "treatment_ar": [
            "طبق زيت النيم أو مبيد فطري أساسه الكبريت",
            "أزل الأجزاء المصابة بشدة",
            "زد المسافة بين النباتات",
            "اسقِ على مستوى التربة"
        ]
    }
}

# Conversation storage (in-memory for demo; use Redis in production)
_conversations: Dict[str, List[Dict]] = {}


# ============================================
# Helper Functions
# ============================================

def generate_conversation_id() -> str:
    """Generate unique conversation ID"""
    import uuid
    return str(uuid.uuid4())[:12]


def get_response_for_query(
    message: str, language: str, db: Session, user_id: int
) -> Dict[str, Any]:
    """Generate intelligent response based on user query"""
    message_lower = message.lower()
    suggestions = []
    related_diseases = []

    # Detect intent and generate response
    if any(word in message_lower for word in [
        "disease", "مرض", "blight", "mildew", "لفحة", "بياض", "علاج", "treatment"
    ]):
        # Disease-related query
        response, response_ar = _handle_disease_query(message_lower, db)
        suggestions = [
            "Show treatment options" if language == "en" else "عرض خيارات العلاج",
            "Prevention tips" if language == "en" else "نصائح الوقاية",
            "Similar diseases" if language == "en" else "أمراض مشابهة"
        ]
    elif any(word in message_lower for word in [
        "tomato", "cucumber", "pepper", "طماطم", "خيار", "فلفل", "care", "رعاية"
    ]):
        # Plant care query
        response, response_ar = _handle_plant_query(message_lower)
        suggestions = [
            "Common diseases" if language == "en" else "الأمراض الشائعة",
            "Watering guide" if language == "en" else "دليل الري",
            "Growth tips" if language == "en" else "نصائح النمو"
        ]
    elif any(word in message_lower for word in [
        "diagnos", "تشخيص", "scan", "فحص", "check", "فحص"
    ]):
        # Diagnosis query
        response = "To diagnose plant diseases, upload an image using the Diagnosis feature."
        response_ar = "لتشخيص أمراض النباتات، قم برفع صورة باستخدام ميزة التشخيص."
        suggestions = [
            "Start diagnosis" if language == "en" else "بدء التشخيص",
            "View history" if language == "en" else "عرض السجل",
            "Tips for better scans" if language == "en" else "نصائح لفحص أفضل"
        ]
    elif any(word in message_lower for word in ["hello", "hi", "مرحبا", "السلام"]):
        # Greeting
        response = "Hello! I'm your plant care assistant. How can I help you today?"
        response_ar = "مرحباً! أنا مساعدك للعناية بالنباتات. كيف يمكنني مساعدتك اليوم؟"
        suggestions = [
            "Diagnose plant" if language == "en" else "تشخيص نبات",
            "Plant care tips" if language == "en" else "نصائح رعاية النباتات",
            "Disease treatment" if language == "en" else "علاج الأمراض"
        ]
    else:
        # Default response
        response = "I can help with plant diseases, care tips, and diagnosis. What would you like to know?"
        response_ar = "يمكنني المساعدة في أمراض النباتات ونصائح الرعاية والتشخيص. ماذا تريد أن تعرف؟"
        suggestions = [
            "Common diseases" if language == "en" else "الأمراض الشائعة",
            "Plant care" if language == "en" else "رعاية النباتات",
            "Start diagnosis" if language == "en" else "بدء التشخيص"
        ]

    return {
        "response": response,
        "response_ar": response_ar,
        "suggestions": suggestions,
        "related_diseases": related_diseases
    }


def _handle_disease_query(message: str, db: Session) -> tuple:
    """Handle disease-related queries"""
    # Check for specific diseases
    for key, disease in DISEASE_TREATMENTS.items():
        if key.replace("_", " ") in message or disease["name"].lower() in message:
            treatment_text = "\n".join(f"• {t}" for t in disease["treatment"])
            treatment_ar = "\n".join(f"• {t}" for t in disease["treatment_ar"])
            return (
                f"**{disease['name']}**\n\n"
                f"Symptoms: {disease['symptoms']}\n\n"
                f"Treatment:\n{treatment_text}",
                f"**{disease['name_ar']}**\n\n"
                f"الأعراض: {disease['symptoms_ar']}\n\n"
                f"العلاج:\n{treatment_ar}"
            )

    # Generic disease response
    return (
        "Please describe the symptoms or specify the disease name for treatment advice.",
        "يرجى وصف الأعراض أو تحديد اسم المرض للحصول على نصائح العلاج."
    )


def _handle_plant_query(message: str) -> tuple:
    """Handle plant care queries"""
    for key, plant in PLANT_CARE_KNOWLEDGE.items():
        if key in message or plant["name"].lower() in message:
            tips_text = "\n".join(f"• {t}" for t in plant["care_tips"])
            tips_ar = "\n".join(f"• {t}" for t in plant["care_tips_ar"])
            diseases = ", ".join(plant["common_diseases"])
            return (
                f"**{plant['name']} Care Guide**\n\n"
                f"Care Tips:\n{tips_text}\n\n"
                f"Common Diseases: {diseases}",
                f"**دليل رعاية {plant['name_ar']}**\n\n"
                f"نصائح الرعاية:\n{tips_ar}\n\n"
                f"الأمراض الشائعة: {diseases}"
            )

    return (
        "Please specify the plant type for care recommendations.",
        "يرجى تحديد نوع النبات للحصول على توصيات الرعاية."
    )


# ============================================
# API Endpoints
# ============================================

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint for conversational AI.
    Processes user messages and returns intelligent responses.
    """
    # Get or create conversation
    conv_id = request.conversation_id or generate_conversation_id()

    if conv_id not in _conversations:
        _conversations[conv_id] = []

    # Store user message
    _conversations[conv_id].append({
        "role": "user",
        "content": request.message,
        "timestamp": datetime.utcnow().isoformat()
    })

    # Generate response
    result = get_response_for_query(
        request.message, request.language, db, current_user.id
    )

    # Store assistant response
    _conversations[conv_id].append({
        "role": "assistant",
        "content": result["response"],
        "timestamp": datetime.utcnow().isoformat()
    })

    logger.info(f"Chat: user={current_user.id}, conv={conv_id}")

    return ChatResponse(
        success=True,
        response=result["response"],
        response_ar=result["response_ar"],
        suggestions=result["suggestions"],
        related_diseases=result["related_diseases"],
        conversation_id=conv_id,
        timestamp=datetime.utcnow()
    )


@router.get("/quick-actions", response_model=List[QuickAction])
async def get_quick_actions(
    current_user: User = Depends(get_current_user)
):
    """Get available quick action buttons for the chatbot UI"""
    return [
        QuickAction(
            id="diagnose",
            label="Diagnose Plant",
            label_ar="تشخيص نبات",
            action="navigate:/diagnosis"
        ),
        QuickAction(
            id="diseases",
            label="Common Diseases",
            label_ar="الأمراض الشائعة",
            action="query:common diseases"
        ),
        QuickAction(
            id="care",
            label="Plant Care Tips",
            label_ar="نصائح رعاية النباتات",
            action="query:plant care tips"
        ),
        QuickAction(
            id="history",
            label="My Diagnosis History",
            label_ar="سجل التشخيص",
            action="navigate:/diagnosis/history"
        )
    ]


@router.get("/disease-info/{disease_name}")
async def get_disease_info(
    disease_name: str,
    current_user: User = Depends(get_current_user)
):
    """Get detailed information about a specific disease"""
    key = disease_name.lower().replace(" ", "_")

    if key in DISEASE_TREATMENTS:
        disease = DISEASE_TREATMENTS[key]
        return {
            "success": True,
            "disease": disease
        }

    # Search in database
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Disease '{disease_name}' not found"
    )


@router.get("/plant-care/{plant_type}")
async def get_plant_care(
    plant_type: str,
    current_user: User = Depends(get_current_user)
):
    """Get care information for a specific plant type"""
    key = plant_type.lower()

    if key in PLANT_CARE_KNOWLEDGE:
        plant = PLANT_CARE_KNOWLEDGE[key]
        return {
            "success": True,
            "plant": plant
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Plant type '{plant_type}' not found"
    )


@router.get("/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Retrieve conversation history"""
    if conversation_id not in _conversations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return {
        "success": True,
        "conversation_id": conversation_id,
        "messages": _conversations[conversation_id]
    }
