"""
/home/ubuntu/code_fixes/ai_integration_modules/memory_ai_fix.py

هذا الملف يحتوي على إصلاحات لمديول ذاكرة الذكاء الاصطناعي (Memory AI)
"""
import json
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    نموذج أساسي يوفر حقول مشتركة لجميع النماذج
    """
    class Meta:
        app_label = 'memory_ai'


    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name=_("تم الإنشاء بواسطة")
    )
    updated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        verbose_name=_("تم التحديث بواسطة")
    )
    is_active = models.BooleanField(_("نشط"), default=True)

    class Meta:
        app_label = 'memory_ai'
        abstract = True


class Memory(models.Model):
    class Meta:
        app_label = 'memory_ai'

    """
    نموذج ذاكرة الذكاء الاصطناعي
    """

    MEMORY_TYPES = (
        ('short_term', _('قصيرة المدى')),
        ('long_term', _('طويلة المدى')),
        ('episodic', _('حلقية')),
        ('semantic', _('دلالية')),
        ('procedural', _('إجرائية')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(
        _("المفتاح"),
        max_length=255,
        db_index=True,
        help_text=_("مفتاح فريد للذاكرة")
    )
    memory_type = models.CharField(
        _("نوع الذاكرة"),
        max_length=20,
        choices=MEMORY_TYPES,
        default='short_term',
        db_index=True,
        help_text=_("نوع الذاكرة")
    )
    content = models.JSONField(
        _("المحتوى"),
        help_text=_("محتوى الذاكرة بتنسيق JSON")
    )
    metadata = models.JSONField(
        _("البيانات الوصفية"),
        default=dict,
        blank=True,
        help_text=_("بيانات وصفية إضافية للذاكرة")
    )
    expiry_date = models.DateTimeField(
        _("تاريخ انتهاء الصلاحية"),
        null=True,
        blank=True,
        db_index=True,
        help_text=_("تاريخ انتهاء صلاحية الذاكرة (فارغ = لا تنتهي)")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
        related_name="memories",
        help_text=_("المستخدم المرتبط بالذاكرة")
    )
    agent_id = models.CharField(
        _("معرف الوكيل"),
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("معرف وكيل الذكاء الاصطناعي المرتبط بالذاكرة")
    )
    importance = models.FloatField(
        _("الأهمية"),
        default=0.5,
        help_text=_("درجة أهمية الذاكرة (0.0 - 1.0)")
    )
    embedding = models.JSONField(
        _("التضمين"),
        null=True,
        blank=True,
        help_text=_("تضمين متجه للذاكرة للبحث الدلالي")
    )
    last_accessed = models.DateTimeField(
        _("آخر وصول"),
        default=timezone.now,
        db_index=True,
        help_text=_("آخر وقت تم فيه الوصول إلى الذاكرة")
    )
    access_count = models.PositiveIntegerField(
        _("عدد مرات الوصول"),
        default=0,
        help_text=_("عدد مرات الوصول إلى الذاكرة")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("ذاكرة")
        verbose_name_plural = _("الذاكرة")
        ordering = ["-last_accessed"]
        unique_together = [['key', 'user', 'agent_id']]
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['memory_type']),
            models.Index(fields=['user']),
            models.Index(fields=['agent_id']),
            models.Index(fields=['importance']),
            models.Index(fields=['-last_accessed']),
            models.Index(fields=['expiry_date']),
        ]

    def __str__(self):
        return f"{self.key} ({self.get_memory_type_display()})"

    def clean(self):
        """التحقق من صحة البيانات قبل الحفظ"""
        if self.expiry_date and self.expiry_date <= timezone.now():
            raise ValidationError(
                _("تاريخ انتهاء الصلاحية يجب أن يكون في المستقبل"))
        if self.importance < 0.0 or self.importance > 1.0:
            raise ValidationError(_("الأهمية يجب أن تكون بين 0.0 و 1.0"))

    def access(self):
        """تسجيل وصول إلى الذاكرة"""
        self.last_accessed = timezone.now()
        self.access_count += 1
        self.save(update_fields=['last_accessed',
                  'access_count', 'updated_at'])

    def update_content(self, content):
        """تحديث محتوى الذاكرة"""
        self.content = content
        self.updated_at = timezone.now()
        self.save(update_fields=['content', 'updated_at'])

    def is_expired(self):
        """التحقق مما إذا كانت الذاكرة منتهية الصلاحية"""
        if self.expiry_date:
            return timezone.now() >= self.expiry_date
        return False


class MemoryCollection(models.Model):
    """
    مجموعة ذاكرة الذكاء الاصطناعي
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("الاسم"),
        max_length=100,
        help_text=_("اسم مجموعة الذاكرة")
    )
    description = models.TextField(
        _("الوصف"),
        blank=True,
        help_text=_("وصف مجموعة الذاكرة")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
        related_name="memory_collections",
        help_text=_("المستخدم المرتبط بمجموعة الذاكرة")
    )
    agent_id = models.CharField(
        _("معرف الوكيل"),
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("معرف وكيل الذكاء الاصطناعي المرتبط بمجموعة الذاكرة")
    )
    metadata = models.JSONField(
        _("البيانات الوصفية"),
        default=dict,
        blank=True,
        help_text=_("بيانات وصفية إضافية لمجموعة الذاكرة")
    )
    is_default = models.BooleanField(
        _("افتراضية"),
        default=False,
        help_text=_("هل هذه مجموعة الذاكرة الافتراضية للمستخدم/الوكيل")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("مجموعة ذاكرة")
        verbose_name_plural = _("مجموعات الذاكرة")
        ordering = ["name"]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['agent_id']),
            models.Index(fields=['is_default']),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """التحقق من صحة البيانات قبل الحفظ"""
        if self.is_default:
            # التأكد من عدم وجود مجموعة افتراضية أخرى لنفس المستخدم/الوكيل
            existing = MemoryCollection.objects.filter(
                user=self.user,
                agent_id=self.agent_id,
                is_default=True
            ).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError(
                    _("يوجد بالفعل مجموعة ذاكرة افتراضية لهذا المستخدم/الوكيل")
                )


class MemoryCollectionItem(models.Model):
    """
    عنصر في مجموعة ذاكرة الذكاء الاصطناعي
    """
    collection = models.ForeignKey(
        MemoryCollection,
        on_delete=models.CASCADE,
        verbose_name=_("المجموعة"),
        related_name="items",
        help_text=_("مجموعة الذاكرة التي ينتمي إليها العنصر")
    )
    memory = models.ForeignKey(
        Memory,
        on_delete=models.CASCADE,
        verbose_name=_("الذاكرة"),
        related_name="collection_items",
        help_text=_("الذاكرة المرتبطة بالعنصر")
    )
    added_at = models.DateTimeField(
        _("تاريخ الإضافة"),
        default=timezone.now,
        help_text=_("تاريخ إضافة الذاكرة إلى المجموعة")
    )
    order = models.PositiveIntegerField(
        _("الترتيب"),
        default=0,
        help_text=_("ترتيب العنصر في المجموعة")
    )
    metadata = models.JSONField(
        _("البيانات الوصفية"),
        default=dict,
        blank=True,
        help_text=_("بيانات وصفية إضافية للعنصر")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("عنصر مجموعة ذاكرة")
        verbose_name_plural = _("عناصر مجموعة الذاكرة")
        ordering = ["collection", "order"]
        unique_together = [['collection', 'memory']]
        indexes = [
            models.Index(fields=['collection']),
            models.Index(fields=['memory']),
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f"{self.collection.name} - {self.memory.key}"


class ConversationMemory(models.Model):
    """
    ذاكرة المحادثة للذكاء الاصطناعي
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.CharField(
        _("معرف المحادثة"),
        max_length=100,
        db_index=True,
        help_text=_("معرف المحادثة المرتبطة بالذاكرة")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
        related_name="conversation_memories",
        help_text=_("المستخدم المرتبط بذاكرة المحادثة")
    )
    agent_id = models.CharField(
        _("معرف الوكيل"),
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("معرف وكيل الذكاء الاصطناعي المرتبط بذاكرة المحادثة")
    )
    summary = models.TextField(
        _("الملخص"),
        blank=True,
        help_text=_("ملخص المحادثة")
    )
    context = models.JSONField(
        _("السياق"),
        default=dict,
        help_text=_("سياق المحادثة بتنسيق JSON")
    )
    messages = models.JSONField(
        _("الرسائل"),
        default=list,
        help_text=_("سجل رسائل المحادثة بتنسيق JSON")
    )
    metadata = models.JSONField(
        _("البيانات الوصفية"),
        default=dict,
        blank=True,
        help_text=_("بيانات وصفية إضافية لذاكرة المحادثة")
    )
    last_updated = models.DateTimeField(
        _("آخر تحديث"),
        default=timezone.now,
        db_index=True,
        help_text=_("آخر وقت تم فيه تحديث ذاكرة المحادثة")
    )
    expiry_date = models.DateTimeField(
        _("تاريخ انتهاء الصلاحية"),
        null=True,
        blank=True,
        db_index=True,
        help_text=_("تاريخ انتهاء صلاحية ذاكرة المحادثة (فارغ = لا تنتهي)")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("ذاكرة محادثة")
        verbose_name_plural = _("ذاكرة المحادثات")
        ordering = ["-last_updated"]
        indexes = [
            models.Index(fields=['conversation_id']),
            models.Index(fields=['user']),
            models.Index(fields=['agent_id']),
            models.Index(fields=['-last_updated']),
            models.Index(fields=['expiry_date']),
        ]

    def __str__(self):
        return f"ذاكرة محادثة {self.conversation_id}"

    def add_message(self, role, content, metadata=None):
        """إضافة رسالة إلى ذاكرة المحادثة"""
        if metadata is None:
            metadata = {}

        message = {
            "role": role,
            "content": content,
            "timestamp": timezone.now().isoformat(),
            "metadata": metadata,
        }

        if isinstance(self.messages, str):
            # تحويل من سلسلة نصية إلى قائمة إذا لزم الأمر
            self.messages = json.loads(self.messages)

        if not isinstance(self.messages, list):
            self.messages = []

        self.messages.append(message)
        self.last_updated = timezone.now()
        self.save(update_fields=['messages', 'last_updated', 'updated_at'])

        return message

    def update_summary(self, summary):
        """تحديث ملخص المحادثة"""
        self.summary = summary
        self.last_updated = timezone.now()
        self.save(update_fields=['summary', 'last_updated', 'updated_at'])

    def update_context(self, context):
        """تحديث سياق المحادثة"""
        self.context = context
        self.last_updated = timezone.now()
        self.save(update_fields=['context', 'last_updated', 'updated_at'])

    def get_recent_messages(self, limit=10):
        """الحصول على الرسائل الأخيرة في المحادثة"""
        if isinstance(self.messages, str):
            messages = json.loads(self.messages)
        else:
            messages = self.messages

        return messages[-limit:] if messages else []

    def is_expired(self):
        """التحقق مما إذا كانت ذاكرة المحادثة منتهية الصلاحية"""
        if self.expiry_date:
            return timezone.now() >= self.expiry_date
        return False


class KnowledgeBase(models.Model):
    """
    قاعدة المعرفة للذكاء الاصطناعي
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("الاسم"),
        max_length=100,
        help_text=_("اسم قاعدة المعرفة")
    )
    description = models.TextField(
        _("الوصف"),
        blank=True,
        help_text=_("وصف قاعدة المعرفة")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
        related_name="knowledge_bases",
        help_text=_("المستخدم المرتبط بقاعدة المعرفة")
    )
    is_public = models.BooleanField(
        _("عامة"),
        default=False,
        help_text=_("هل قاعدة المعرفة متاحة للجميع")
    )
    metadata = models.JSONField(
        _("البيانات الوصفية"),
        default=dict,
        blank=True,
        help_text=_("بيانات وصفية إضافية لقاعدة المعرفة")
    )
    vector_store_id = models.CharField(
        _("معرف مخزن المتجهات"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("معرف مخزن المتجهات المرتبط بقاعدة المعرفة")
    )
    embedding_model = models.CharField(
        _("نموذج التضمين"),
        max_length=100,
        default="default",
        help_text=_("نموذج التضمين المستخدم لقاعدة المعرفة")
    )
    created_at = models.DateTimeField(
        _("تاريخ الإنشاء"),
        default=timezone.now,
        help_text=_("تاريخ إنشاء قاعدة المعرفة")
    )
    updated_at = models.DateTimeField(
        _("تاريخ التحديث"),
        auto_now=True,
        help_text=_("تاريخ آخر تحديث لقاعدة المعرفة")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("قاعدة معرفة")
        verbose_name_plural = _("قواعد المعرفة")
    class Meta:
        app_label = 'memory_ai'

        ordering = ["name"]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_public']),
        ]

    def __str__(self):
        return self.name


class KnowledgeItem(models.Model):
    """
    عنصر في قاعدة المعرفة للذكاء الاصطناعي
    """

    ITEM_TYPES = (
        ('text', _('نص')),
        ('document', _('مستند')),
        ('url', _('رابط')),
        ('image', _('صورة')),
        ('video', _('فيديو')),
        ('audio', _('صوت')),
        ('custom', _('مخصص')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        verbose_name=_("قاعدة المعرفة"),
        related_name="items",
        help_text=_("قاعدة المعرفة التي ينتمي إليها العنصر")
    )
    title = models.CharField(
        _("العنوان"),
        max_length=200,
        help_text=_("عنوان عنصر المعرفة")
    )
    content = models.TextField(
        _("المحتوى"),
        help_text=_("محتوى عنصر المعرفة")
    )
    item_type = models.CharField(
        _("نوع العنصر"),
        max_length=20,
        choices=ITEM_TYPES,
        default='text',
        db_index=True,
        help_text=_("نوع عنصر المعرفة")
    )
    source_url = models.URLField(
        _("رابط المصدر"),
        max_length=1000,
        null=True,
        blank=True,
        help_text=_("رابط المصدر الأصلي للمحتوى")
    )
    metadata = models.JSONField(
        _("البيانات الوصفية"),
        default=dict,
        blank=True,
        help_text=_("بيانات وصفية إضافية لعنصر المعرفة")
    )
    embedding = models.JSONField(
        _("التضمين"),
        null=True,
        blank=True,
        help_text=_("تضمين متجه لعنصر المعرفة للبحث الدلالي")
    )
    embedding_model = models.CharField(
        _("نموذج التضمين"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("نموذج التضمين المستخدم لهذا العنصر")
    )
    vector_id = models.CharField(
        _("معرف المتجه"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("معرف المتجه في مخزن المتجهات")
    )
    created_at = models.DateTimeField(
        _("تاريخ الإنشاء"),
        default=timezone.now,
        help_text=_("تاريخ إنشاء عنصر المعرفة")
    )
    updated_at = models.DateTimeField(
        _("تاريخ التحديث"),
        auto_now=True,
        help_text=_("تاريخ آخر تحديث لعنصر المعرفة")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("عنصر معرفة")
        verbose_name_plural = _("عناصر المعرفة")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['knowledge_base']),
            models.Index(fields=['item_type']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title


class MemoryIndex(models.Model):
    """
    فهرس الذاكرة للذكاء الاصطناعي
    """

    INDEX_TYPES = (
        ('vector', _('متجه')),
        ('keyword', _('كلمة مفتاحية')),
        ('hybrid', _('هجين')),
        ('custom', _('مخصص')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("الاسم"),
        max_length=100,
        help_text=_("اسم فهرس الذاكرة")
    )
    description = models.TextField(
        _("الوصف"),
        blank=True,
        help_text=_("وصف فهرس الذاكرة")
    )
    index_type = models.CharField(
        _("نوع الفهرس"),
        max_length=20,
        choices=INDEX_TYPES,
        default='vector',
        db_index=True,
        help_text=_("نوع فهرس الذاكرة")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
        related_name="memory_indexes",
        help_text=_("المستخدم المرتبط بفهرس الذاكرة")
    )
    agent_id = models.CharField(
        _("معرف الوكيل"),
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("معرف وكيل الذكاء الاصطناعي المرتبط بفهرس الذاكرة")
    )
    config = models.JSONField(
        _("الإعدادات"),
        default=dict,
        help_text=_("إعدادات فهرس الذاكرة بتنسيق JSON")
    )
    metadata = models.JSONField(
        _("البيانات الوصفية"),
        default=dict,
        blank=True,
        help_text=_("بيانات وصفية إضافية لفهرس الذاكرة")
    )
    external_id = models.CharField(
        _("المعرف الخارجي"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("معرف الفهرس في نظام خارجي")
    )
    created_at = models.DateTimeField(
        _("تاريخ الإنشاء"),
        default=timezone.now,
        help_text=_("تاريخ إنشاء فهرس الذاكرة")
    )
    updated_at = models.DateTimeField(
        _("تاريخ التحديث"),
        auto_now=True,
        help_text=_("تاريخ آخر تحديث لفهرس الذاكرة")
    )
    last_optimized = models.DateTimeField(
        _("آخر تحسين"),
        null=True,
        blank=True,
        help_text=_("تاريخ آخر تحسين للفهرس")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("فهرس ذاكرة")
        verbose_name_plural = _("فهارس الذاكرة")
        ordering = ["name"]
        indexes = [
            models.Index(fields=['index_type']),
            models.Index(fields=['user']),
            models.Index(fields=['agent_id']),
        ]

    def __str__(self):
        return self.name


class MemoryQuery(models.Model):
    """
    استعلام ذاكرة الذكاء الاصطناعي
    """

    QUERY_TYPES = (
        ('exact', _('مطابق')),
        ('semantic', _('دلالي')),
        ('hybrid', _('هجين')),
        ('custom', _('مخصص')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query_text = models.TextField(
        _("نص الاستعلام"),
        help_text=_("نص الاستعلام")
    )
    query_type = models.CharField(
        _("نوع الاستعلام"),
        max_length=20,
        choices=QUERY_TYPES,
        default='semantic',
        db_index=True,
        help_text=_("نوع الاستعلام")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
        related_name="memory_queries",
        help_text=_("المستخدم الذي أجرى الاستعلام")
    )
    agent_id = models.CharField(
        _("معرف الوكيل"),
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("معرف وكيل الذكاء الاصطناعي الذي أجرى الاستعلام")
    )
    index = models.ForeignKey(
        MemoryIndex,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("الفهرس"),
        related_name="queries",
        help_text=_("فهرس الذاكرة المستخدم للاستعلام")
    )
    parameters = models.JSONField(
        _("المعلمات"),
        default=dict,
        blank=True,
        help_text=_("معلمات الاستعلام بتنسيق JSON")
    )
    results = models.JSONField(
        _("النتائج"),
        default=list,
        blank=True,
        help_text=_("نتائج الاستعلام بتنسيق JSON")
    )
    execution_time_ms = models.PositiveIntegerField(
        _("وقت التنفيذ (مللي ثانية)"),
        null=True,
        blank=True,
        help_text=_("وقت تنفيذ الاستعلام بالمللي ثانية")
    )
    timestamp = models.DateTimeField(
        _("الطابع الزمني"),
        default=timezone.now,
        db_index=True,
        help_text=_("وقت إجراء الاستعلام")
    )
    conversation_id = models.CharField(
        _("معرف المحادثة"),
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("معرف المحادثة المرتبطة بالاستعلام")
    )
    metadata = models.JSONField(
        _("البيانات الوصفية"),
        default=dict,
        blank=True,
        help_text=_("بيانات وصفية إضافية للاستعلام")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("استعلام ذاكرة")
        verbose_name_plural = _("استعلامات الذاكرة")
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['query_type']),
            models.Index(fields=['user']),
            models.Index(fields=['agent_id']),
            models.Index(fields=['conversation_id']),
        ]

    def __str__(self):
        return f"""{self.query_text[:50]}... ({self.get_query_type_display()})"""


class MemoryStatistics(models.Model):
    """
    إحصائيات ذاكرة الذكاء الاصطناعي
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
        related_name="memory_statistics",
        help_text=_("المستخدم المرتبط بالإحصائيات")
    )
    agent_id = models.CharField(
        _("معرف الوكيل"),
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("معرف وكيل الذكاء الاصطناعي المرتبط بالإحصائيات")
    )
    date = models.DateField(
        _("التاريخ"),
        default=timezone.now,
        db_index=True,
        help_text=_("تاريخ الإحصائيات")
    )
    memory_count = models.PositiveIntegerField(
        _("عدد الذاكرة"),
        default=0,
        help_text=_("إجمالي عدد عناصر الذاكرة")
    )
    query_count = models.PositiveIntegerField(
        _("عدد الاستعلامات"),
        default=0,
        help_text=_("إجمالي عدد الاستعلامات")
    )
    avg_query_time_ms = models.PositiveIntegerField(
        _("متوسط وقت الاستعلام (مللي ثانية)"),
        null=True,
        blank=True,
        help_text=_("متوسط وقت تنفيذ الاستعلام بالمللي ثانية")
    )
    storage_bytes = models.PositiveBigIntegerField(
        _("حجم التخزين (بايت)"),
        default=0,
        help_text=_("إجمالي حجم التخزين المستخدم بالبايت")
    )
    conversation_count = models.PositiveIntegerField(
        _("عدد المحادثات"),
        default=0,
        help_text=_("إجمالي عدد المحادثات")
    )
    knowledge_item_count = models.PositiveIntegerField(
        _("عدد عناصر المعرفة"),
        default=0,
        help_text=_("إجمالي عدد عناصر المعرفة")
    )
    statistics = models.JSONField(
        _("إحصائيات"),
        default=dict,
        help_text=_("إحصائيات إضافية بتنسيق JSON")
    )

    class Meta:
        app_label = 'memory_ai'
        verbose_name = _("إحصائيات ذاكرة")
        verbose_name_plural = _("إحصائيات الذاكرة")
        ordering = ["-date"]
        unique_together = [['user', 'agent_id', 'date']]
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['user']),
            models.Index(fields=['agent_id']),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else "النظام"
        agent_str = self.agent_id if self.agent_id else "جميع الوكلاء"
        return f"إحصائيات {user_str} - {agent_str} - {self.date}"
