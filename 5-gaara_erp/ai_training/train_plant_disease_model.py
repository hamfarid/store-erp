import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os

# مسارات البيانات
base_dir = '/home/ubuntu/gaara_erp_v12/ai_training_data/plant_diseases'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# إعداد مولدات البيانات مع Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2 # 20% للتحقق
)

train_generator = train_datagen.flow_from_directory(
    base_dir, # استخدام المجلد الأساسي مباشرة
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training' # تحديد مجموعة التدريب
)

validation_generator = train_datagen.flow_from_directory(
    base_dir, # استخدام المجلد الأساسي مباشرة
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation' # تحديد مجموعة التحقق
)

# بناء النموذج
base_model = ResNet50(weights='imagenet', include_top=False)

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# تجميد الطبقات الأساسية للتدريب الأولي
for layer in base_model.layers:
    layer.trainable = False

# تجميع النموذج
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# تدريب النموذج
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size
)

# حفظ النموذج
model.save('/home/ubuntu/gaara_erp_v12/ai_models/plant_disease_model.h5')

print('تم تدريب وحفظ نموذج تشخيص أمراض النباتات بنجاح!')

