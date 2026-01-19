# تصميم بنية التدريب الموزع لنظام الذكاء الاصطناعي الزراعي

## 1. نظرة عامة

يهدف هذا المستند إلى تصميم بنية تحتية للتدريب الموزع لنماذج الذكاء الاصطناعي الخاصة بالنظام الزراعي. يستفيد التصميم من مجموعة خوادم Linux تعمل بنظام Docker Swarm لإدارة المكونات الرئيسية للنظام، بينما يتم تخصيص جهاز Windows مزود بوحدة معالجة رسومات (GPU) لتنفيذ مهام التدريب المكثفة حسابياً. يتم استخدام نهج هجين لفصل مهام التدريب التي تتطلب GPU عن باقي مكونات النظام لتجنب تعقيدات دمج عقد Windows GPU مباشرة في Docker Swarm.

**الأهداف:**

*   تسريع عملية تدريب نماذج الذكاء الاصطناعي باستخدام GPU.
*   توزيع الحمل بين الخوادم المتاحة.
*   إنشاء بنية قابلة للتطوير والإدارة.
*   فصل مهام التدريب عن الخدمات الأساسية للنظام.

**الخوادم المتاحة:**

*   `100.127.77.118` (mimic): غير محدد
*   `100.127.22.35` (gaara-prox): Linux
*   `100.78.19.7` (gaara): Linux (مرشح ليكون مدير Swarm)
*   `100.109.208.97` (hadyfamily-hostinger): Linux (مرشح ليكون عامل Swarm)
*   `100.104.23.62` (mail-contapo): Linux (مرشح ليكون عامل Swarm)
*   `100.77.215.80` (truenas): تخزين (سيتم استخدامه للتخزين المشترك)
*   `100.95.120.21` (victus): Windows (يحتوي على GPU، سيُستخدم للتدريب)

## 2. مخطط البنية

```mermaid
graph TD
    subgraph Docker Swarm Cluster (Linux)
        SwarmManager[Swarm Manager (gaara)]
        Worker1[Worker Node (hadyfamily-hostinger)]
        Worker2[Worker Node (mail-contapo)]
        APIServer(API Server - FastAPI/Django)
        Database[(Database - PostgreSQL)]
        WebUI(Web UI - Flask)
        MsgQueue(Message Queue - RabbitMQ)
        Monitoring(Monitoring - Prometheus/Grafana)

        SwarmManager --- Worker1
        SwarmManager --- Worker2
        SwarmManager -- Manages --> APIServer
        SwarmManager -- Manages --> Database
        SwarmManager -- Manages --> WebUI
        SwarmManager -- Manages --> MsgQueue
        SwarmManager -- Manages --> Monitoring
    end

    subgraph Windows GPU Node (victus)
        DockerGPU[Docker Engine + GPU Support]
        TrainingService(Training Service - Python/PyTorch)
        DockerGPU -- Runs --> TrainingService
    end

    subgraph Shared Storage (truenas)
        Storage[(NFS/SMB Share)]
        Datasets[/Datasets/]
        Models[/Models/]
        Logs[/Logs/]
        Storage -- Contains --> Datasets
        Storage -- Contains --> Models
        Storage -- Contains --> Logs
    end

    User[User] -- Interacts --> WebUI
    WebUI -- API Calls --> APIServer
    APIServer -- Publishes Job --> MsgQueue
    APIServer -- Reads/Writes --> Database
    TrainingService -- Subscribes --> MsgQueue
    TrainingService -- Reads/Writes --> Datasets
    TrainingService -- Reads/Writes --> Models
    TrainingService -- Writes --> Logs
    TrainingService -- Publishes Result --> MsgQueue
    APIServer -- Reads --> Logs
    APIServer -- Reads --> Models
    Monitoring -- Scrapes --> APIServer
    Monitoring -- Scrapes --> TrainingService

    %% Storage Access
    APIServer -- Accesses --> Storage
    Database -- Accesses --> Storage
    TrainingService -- Accesses --> Storage
    Worker1 -- Accesses --> Storage
    Worker2 -- Accesses --> Storage

```

**شرح المخطط:**

*   **Docker Swarm Cluster (Linux):** مجموعة من خوادم Linux (`gaara`, `hadyfamily-hostinger`, `mail-contapo`) تعمل كعقد في Docker Swarm. يقوم مدير Swarm (`gaara`) بتوزيع وإدارة الخدمات الأساسية (API، قاعدة البيانات، واجهة المستخدم، قائمة انتظار الرسائل، المراقبة) عبر العقد العاملة.
*   **Windows GPU Node (victus):** جهاز Windows (`victus`) يعمل عليه Docker مع دعم GPU. يستضيف خدمة التدريب (Training Service) المسؤولة عن تنفيذ مهام التدريب.
*   **Shared Storage (truenas):** خادم تخزين (`truenas`) يوفر مساحة تخزين مشتركة (باستخدام NFS أو SMB) يمكن الوصول إليها من جميع العقد (Linux و Windows). تُستخدم لتخزين مجموعات البيانات، النماذج المدربة، والسجلات.
*   **Communication:** يتم استخدام قائمة انتظار الرسائل (RabbitMQ) كوسيط لتنسيق مهام التدريب. يقوم خادم API بنشر مهام التدريب في القائمة، وتشترك خدمة التدريب على عقدة Windows في هذه القائمة لسحب المهام وتنفيذها، ثم تنشر النتائج مرة أخرى.

## 3. المكونات

*   **Linux Swarm Cluster:**
    *   **الخدمات:**
        *   `api-server`: واجهة برمجة التطبيقات (FastAPI/Django) لإدارة النظام وطلبات التدريب.
        *   `database`: قاعدة بيانات (PostgreSQL) لتخزين بيانات النظام وحالة المهام.
        *   `web-ui`: واجهة مستخدم ويب (Flask) للتفاعل مع المستخدم.
        *   `message-queue`: وسيط رسائل (RabbitMQ) لتنسيق مهام التدريب.
        *   `monitoring`: أدوات مراقبة (Prometheus/Grafana) لتتبع أداء النظام.
    *   **العقد:**
        *   **Manager:** `100.78.19.7` (gaara)
        *   **Workers:** `100.109.208.97` (hadyfamily-hostinger), `100.104.23.62` (mail-contapo)
*   **Windows GPU Node (`victus` - `100.95.120.21`):**
    *   **Docker Engine:** Docker Desktop مع WSL2 ودعم NVIDIA GPU (أو ما يعادله).
    *   **Training Service:** تطبيق Python داخل حاوية Docker:
        *   يستخدم مكتبات مثل `pika` للاتصال بـ RabbitMQ.
        *   يستخدم PyTorch/TensorFlow للتدريب مع الاستفادة من GPU.
        *   يقرأ ويكتب البيانات والنماذج من/إلى التخزين المشترك.
        *   يسجل حالة التقدم والنتائج.
*   **Storage Node (`truenas` - `100.77.215.80`):**
    *   يوفر مشاركات NFS (لـ Linux) و/أو SMB (لـ Windows) للمسارات التالية:
        *   `/data/datasets`: لتخزين مجموعات بيانات التدريب.
        *   `/data/models`: لتخزين النماذج المدربة ونقاط التحقق.
        *   `/data/logs`: لتخزين سجلات التدريب.
*   **Coordination Mechanism:**
    *   **Message Queue (RabbitMQ):** هو الخيار المفضل للتنسيق:
        *   **`training_jobs` queue:** ينشر فيها `api-server` تفاصيل مهام التدريب الجديدة.
        *   **`training_results` queue:** تنشر فيها `Training Service` نتائج المهام المكتملة أو الفاشلة.
        *   يضمن هذا النهج فصل المكونات وقابلية التوسع.

## 4. سير العمل (Workflow)

1.  **طلب التدريب:** المستخدم يبدأ مهمة تدريب جديدة عبر واجهة المستخدم (`web-ui`).
2.  **إرسال المهمة:** `web-ui` ترسل طلبًا إلى `api-server`.
3.  **تحضير المهمة:** `api-server` يتحقق من الطلب، يحضر تفاصيل المهمة (مسار مجموعة البيانات على التخزين المشترك، المعلمات الفائقة، نوع النموذج)، وينشئ معرفًا فريدًا للمهمة، ويحفظ حالتها الأولية في `database`.
4.  **نشر المهمة:** `api-server` ينشر رسالة تحتوي على تفاصيل المهمة إلى قائمة الانتظار `training_jobs` في `message-queue`.
5.  **استلام المهمة:** `Training Service` على عقدة Windows (`victus`) تشترك في قائمة الانتظار `training_jobs` وتستلم رسالة المهمة الجديدة.
6.  **بدء التدريب:** `Training Service` تبدأ حاوية Docker جديدة مع تمكين الوصول إلى GPU.
7.  **تنفيذ التدريب:** حاوية التدريب:
    *   تقرأ تفاصيل المهمة.
    *   تحمل مجموعة البيانات المطلوبة من التخزين المشترك (`/data/datasets`).
    *   تبدأ عملية التدريب باستخدام PyTorch/TensorFlow على GPU.
    *   تحفظ نقاط التحقق والنموذج النهائي في التخزين المشترك (`/data/models`).
    *   تسجل التقدم والأخطاء في ملفات السجل على التخزين المشترك (`/data/logs`).
    *   ترسل تحديثات دورية للحالة (اختياري) إلى `message-queue` أو `api-server`.
8.  **نشر النتيجة:** عند اكتمال التدريب (بنجاح أو فشل)، تنشر `Training Service` رسالة تحتوي على معرف المهمة والحالة النهائية ومسار النموذج/السجلات إلى قائمة الانتظار `training_results`.
9.  **تحديث الحالة:** `api-server` يشترك في قائمة الانتظار `training_results` ويستلم رسالة النتيجة.
10. **تحديث قاعدة البيانات:** `api-server` يحدث حالة المهمة في `database` بناءً على النتيجة المستلمة.
11. **إشعار المستخدم:** `api-server` يرسل إشعارًا إلى المستخدم عبر `web-ui` أو طرق أخرى لإعلامه باكتمال المهمة.

## 5. التقنيات المقترحة

*   **Orchestration:** Docker Swarm (Linux Nodes)
*   **Containerization:** Docker Engine (Linux), Docker Desktop with WSL2 (Windows)
*   **GPU Support:** NVIDIA Container Toolkit (Linux equivalent on Swarm nodes if needed for inference later), NVIDIA driver + Docker GPU support (Windows)
*   **Programming Language:** Python 3.10+
*   **ML Framework:** PyTorch أو TensorFlow
*   **API Framework:** FastAPI أو Django
*   **Database:** PostgreSQL
*   **Message Queue:** RabbitMQ
*   **Web Framework:** Flask
*   **Shared Storage:** NFS (Linux primary), SMB (Windows access)
*   **Monitoring:** Prometheus, Grafana, cAdvisor

## 6. خطوات التنفيذ (مستوى عالٍ)

1.  **إعداد Docker Swarm:** تهيئة Swarm على خوادم Linux (`gaara` كمدير، الآخرون كعمال).
2.  **إعداد عقدة Windows:** تثبيت Docker Desktop مع WSL2 ودعم GPU على `victus`.
3.  **إعداد التخزين المشترك:** تكوين `truenas` لتوفير مشاركات NFS/SMB وتركيبها على جميع العقد (Swarm و Windows).
4.  **تطوير خدمة التدريب:** إنشاء وتعبئة تطبيق Python (`Training Service`) الذي يتصل بـ RabbitMQ وينفذ التدريب على GPU.
5.  **تعديل API Server:** تحديث `api-server` لإدارة دورة حياة مهام التدريب (الإنشاء، النشر عبر RabbitMQ، استقبال النتائج، تحديث قاعدة البيانات).
6.  **تكوين RabbitMQ:** إعداد قوائم الانتظار والتبادلات اللازمة في RabbitMQ.
7.  **نشر الخدمات:** نشر الخدمات الأساسية (API, DB, UI, MQ) على Docker Swarm ونشر `Training Service` على عقدة Windows.
8.  **الاختبار:** اختبار سير العمل الكامل بدءًا من طلب التدريب وحتى الحصول على النتائج والنموذج المدرب.

## 7. اعتبارات الأمان

*   تأمين شبكة Docker Swarm.
*   استخدام Docker Secrets لإدارة المعلومات الحساسة (مفاتيح API، كلمات مرور قاعدة البيانات).
*   تأمين الاتصال بـ RabbitMQ.
*   تطبيق مصادقة وتفويض على `api-server`.
*   تكوين أذونات الوصول المناسبة للتخزين المشترك.
*   تأمين الاتصالات بين العقد (قد يتطلب تكوين جدران الحماية).

## 8. المراقبة

*   استخدام Prometheus و Grafana لمراقبة موارد العقد (CPU, RAM, Disk, Network) وحالة خدمات Swarm.
*   استخدام cAdvisor لجمع مقاييس الحاويات.
*   مراقبة استخدام GPU على عقدة Windows باستخدام أدوات مثل `nvidia-smi` داخل الحاوية أو أدوات مراقبة خاصة بـ Windows.
*   تسجيل شامل من جميع المكونات وتجميع السجلات في مكان مركزي (مثل ELK stack أو Loki) للمساعدة في استكشاف الأخطاء وإصلاحها.
*   مراقبة حالة قوائم الانتظار في RabbitMQ.

---

هذا التصميم يوفر أساسًا قويًا لتنفيذ التدريب الموزع. الخطوات التالية تتضمن مراجعة هذا التصميم والموافقة عليه قبل البدء في التنفيذ الفعلي.
