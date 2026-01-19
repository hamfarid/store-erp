# إعداد عقدة Windows GPU (victus) لخدمة التدريب

يهدف هذا المستند إلى توجيهك خلال عملية إعداد جهاز Windows (`victus` - `100.95.120.21`) لتشغيل خدمة تدريب الذكاء الاصطناعي التي تستخدم GPU ضمن بنية التدريب الموزع.

**المتطلبات الأساسية:**

*   جهاز يعمل بنظام Windows 10/11 (إصدار Pro أو Enterprise أو Education موصى به).
*   وحدة معالجة رسومات (GPU) من NVIDIA متوافقة مع CUDA.
*   اتصال شبكي بالخوادم الأخرى (Swarm Manager، Shared Storage).
*   حقوق المسؤول (Administrator privileges) على جهاز Windows.

## الخطوة 1: تثبيت وتحديث تعريفات NVIDIA

1.  **تنزيل التعريفات:** قم بزيارة [موقع NVIDIA الرسمي لتنزيل التعريفات](https://www.nvidia.com/Download/index.aspx).
2.  **اختيار التعريف:** حدد نوع المنتج، السلسلة، المنتج، ونظام التشغيل الخاص بك. اختر نوع التعريف "Game Ready Driver (GRD)" أو "Studio Driver (SD)" (Studio Driver قد يكون أكثر استقرارًا لمهام الحوسبة).
3.  **تثبيت التعريف:** قم بتنزيل المثبت وتشغيله. اختر "Custom Installation" وتأكد من تحديد خيار "Perform a clean installation" لإزالة أي تعريفات قديمة.
4.  **التحقق:** بعد التثبيت وإعادة التشغيل، افتح موجه الأوامر (Command Prompt) أو PowerShell وقم بتشغيل الأمر `nvidia-smi`. يجب أن يعرض معلومات حول GPU وتعريف NVIDIA المثبت وإصدار CUDA المدعوم بواسطة التعريف.
    *   **ملاحظة هامة:** لاحظ إصدار CUDA المدعوم (يظهر في أعلى يمين إخراج `nvidia-smi`). يجب أن يكون هذا الإصدار متوافقًا أو أحدث من إصدار CUDA المستخدم في `Dockerfile.training_service` (المتغير `CUDA_VERSION`).

## الخطوة 2: تثبيت WSL 2 و Docker Desktop

1.  **تثبيت WSL 2:**
    *   افتح PowerShell كمسؤول (Administrator).
    *   قم بتشغيل الأمر: `wsl --install`
    *   سيقوم هذا الأمر بتثبيت Windows Subsystem for Linux 2 وتوزيعة Ubuntu افتراضية. قد يتطلب إعادة تشغيل الجهاز.
    *   بعد إعادة التشغيل، سيُطلب منك إنشاء اسم مستخدم وكلمة مرور لتوزيعة Ubuntu داخل WSL.
    *   تأكد من أن WSL 2 هو الإصدار الافتراضي: `wsl --set-default-version 2`
2.  **تثبيت Docker Desktop:**
    *   قم بتنزيل Docker Desktop for Windows من [الموقع الرسمي لـ Docker](https://www.docker.com/products/docker-desktop/).
    *   قم بتشغيل المثبت واتبع التعليمات. تأكد من تحديد خيار "Use WSL 2 instead of Hyper-V" (عادة ما يكون الخيار الافتراضي إذا تم اكتشاف WSL 2).
    *   بعد التثبيت، قد يتطلب Docker Desktop إعادة تشغيل أخرى.
3.  **تكوين Docker Desktop لاستخدام GPU:**
    *   افتح Docker Desktop.
    *   انتقل إلى Settings > Resources > WSL Integration.
    *   تأكد من تمكين التكامل مع توزيعة WSL 2 الافتراضية (مثل Ubuntu).
    *   انتقل إلى Settings > Resources > Advanced.
    *   تأكد من أن "WSL 2 based engine" محدد.
    *   **لا يوجد خيار مباشر لتمكين GPU في واجهة Docker Desktop GUI حاليًا.** يتم الاعتماد على تكامل WSL 2 مع تعريفات NVIDIA.

## الخطوة 3: إعداد الوصول إلى التخزين المشترك (SMB)

يجب أن تتمكن حاوية التدريب من الوصول إلى مجموعات البيانات والنماذج والسجلات المخزنة على خادم التخزين (`truenas` - `100.77.215.80`). الطريقة الأكثر شيوعًا للوصول من Windows هي استخدام SMB/CIFS.

1.  **تأكد من تكوين مشاركة SMB على TrueNAS:** تأكد من أن المسارات (`/path/to/shared/datasets`, `/path/to/shared/models`, `/path/to/shared/logs`) مشتركة عبر SMB على خادم TrueNAS مع الأذونات المناسبة.
2.  **تركيب المشاركة على Windows Host (موصى به):**
    *   افتح File Explorer.
    *   انقر بزر الماوس الأيمن على "This PC" واختر "Map network drive...".
    *   اختر حرف محرك أقراص (مثل `Z:`).
    *   في حقل "Folder"، أدخل مسار المشاركة على TrueNAS، على سبيل المثال: `\\100.77.215.80\path\to\shared` (استبدل `path\to\shared` بالمسار الفعلي للمشاركة على TrueNAS).
    *   حدد "Reconnect at sign-in".
    *   انقر "Finish". قد يُطلب منك إدخال بيانات اعتماد للوصول إلى المشاركة إذا كانت محمية بكلمة مرور.
3.  **توفير الوصول للحاوية:** عند تشغيل حاوية خدمة التدريب (الخطوة 5)، ستقوم بتركيب هذا المحرك الشبكي (أو مجلدات محددة داخله) إلى المسارات المتوقعة داخل الحاوية (`/mnt/shared_storage/...`).

## الخطوة 4: بناء صورة Docker لخدمة التدريب

1.  **نسخ الملفات:** تأكد من وجود الملفات التالية في مكان واحد على جهاز Windows:
    *   `Dockerfile.training_service` (الذي تم إنشاؤه في الخطوة السابقة).
    *   `requirements.txt` (يجب أن يحتوي على `torch`, `torchvision`, `torchaudio` بالإصدارات المتوافقة مع CUDA المحدد في Dockerfile، بالإضافة إلى `pika`, `pandas`, `scikit-learn`, `Pillow`, `matplotlib`, `seaborn`).
    *   مجلد `src/training_service` الذي يحتوي على كود Python لخدمة التدريب (بما في ذلك `run_training_service.py`).
2.  **فتح الطرفية:** افتح PowerShell أو Command Prompt في المجلد الذي يحتوي على `Dockerfile.training_service`.
3.  **بناء الصورة:** قم بتشغيل الأمر التالي لبناء الصورة. استبدل `your_training_image_name` باسم مناسب للصورة (مثل `gaara/training-service`):
    ```bash
    docker build -t your_training_image_name:latest -f Dockerfile.training_service .
    ```
    *   قد تستغرق عملية البناء بعض الوقت، خاصة عند تنزيل صورة PyTorch الأساسية وتثبيت التبعيات.

## الخطوة 5: تشغيل حاوية خدمة التدريب

1.  **أمر التشغيل:** استخدم الأمر التالي لتشغيل الحاوية. قم بتعديل المسارات والبيانات الاعتمادية حسب الحاجة.

    ```bash
    docker run -d --gpus all \
        --name training-service-container \
        -v Z:\datasets:/mnt/shared_storage/datasets \
        -v Z:\models:/mnt/shared_storage/models \
        -v Z:\logs:/mnt/shared_storage/logs \
        -e RABBITMQ_HOST="<IP_ADDRESS_OF_SWARM_MANAGER_OR_RABBITMQ_NODE>" \
        -e RABBITMQ_PORT="5672" \
        -e RABBITMQ_USER="rabbit_user" \
        -e RABBITMQ_PASS="rabbit_password" \
        --restart unless-stopped \
        your_training_image_name:latest
    ```

    **شرح الخيارات:**
    *   `-d`: تشغيل الحاوية في الخلفية.
    *   `--gpus all`: تمكين الوصول إلى جميع وحدات GPU المتاحة داخل الحاوية.
    *   `--name training-service-container`: إعطاء اسم للحاوية لسهولة الإدارة.
    *   `-v Z:\datasets:/mnt/shared_storage/datasets`: تركيب مجلد `datasets` من المحرك الشبكي `Z:` إلى المسار `/mnt/shared_storage/datasets` داخل الحاوية.
    *   `-v Z:\models:/mnt/shared_storage/models`: تركيب مجلد `models`.
    *   `-v Z:\logs:/mnt/shared_storage/logs`: تركيب مجلد `logs`.
    *   `-e RABBITMQ_HOST="<IP_ADDRESS_OF_SWARM_MANAGER_OR_RABBITMQ_NODE>"`: **هام:** استبدل `<IP_ADDRESS_OF_SWARM_MANAGER_OR_RABBITMQ_NODE>` بعنوان IP الخاص بعقدة مدير Swarm (`100.78.19.7`) أو أي عقدة يمكن الوصول إليها تشغل خدمة RabbitMQ. بما أن هذه الحاوية تعمل خارج Swarm، لا يمكنها استخدام اسم الخدمة `message-queue` مباشرة.
    *   `-e RABBITMQ_PORT`, `-e RABBITMQ_USER`, `-e RABBITMQ_PASS`: بيانات اعتماد RabbitMQ.
    *   `--restart unless-stopped`: إعادة تشغيل الحاوية تلقائيًا إلا إذا تم إيقافها يدويًا.
    *   `your_training_image_name:latest`: اسم الصورة التي تم بناؤها.

2.  **التحقق من التشغيل:**
    *   `docker ps`: يجب أن تظهر الحاوية `training-service-container` قيد التشغيل.
    *   `docker logs training-service-container`: لعرض سجلات الحاوية والتحقق من أنها تتصل بـ RabbitMQ بنجاح وتبدأ في الاستماع للمهام.
    *   `docker exec -it training-service-container nvidia-smi`: للدخول إلى الحاوية وتشغيل `nvidia-smi` للتأكد من رؤية GPU.

## الخطوة 6: استكشاف الأخطاء وإصلاحها

*   **مشاكل تعريف NVIDIA/CUDA:** تأكد من توافق إصدار CUDA في Dockerfile مع تعريف NVIDIA على المضيف. جرب إصدارات مختلفة من صورة PyTorch الأساسية إذا لزم الأمر.
*   **مشاكل الوصول إلى GPU:** تأكد من أن WSL 2 يعمل بشكل صحيح وأن تعريفات NVIDIA مثبتة بشكل صحيح. قد تحتاج إلى إعادة تشغيل Docker Desktop أو الجهاز.
*   **مشاكل تركيب التخزين المشترك:** تحقق من صحة مسار SMB والأذونات. تأكد من أن خدمة "Workstation" قيد التشغيل على Windows. جرب الوصول إلى المشاركة من File Explorer أولاً.
*   **مشاكل الاتصال بـ RabbitMQ:** تأكد من صحة عنوان IP والمنفذ لـ RabbitMQ وأن جدار الحماية على عقدة Swarm يسمح بالاتصالات الواردة على المنفذ 5672 من جهاز Windows. تأكد من صحة بيانات الاعتماد.

---

باتباع هذه الخطوات، يجب أن تكون قادرًا على إعداد جهاز Windows (`victus`) لتشغيل خدمة التدريب باستخدام GPU والتكامل مع بقية النظام الذي يعمل على Docker Swarm.
