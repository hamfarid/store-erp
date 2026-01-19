<!-- صفحة 404 - الصفحة غير موجودة -->
<template>
  <div class="not-found-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-6 col-md-8">
          <div class="text-center">
            <!-- رقم الخطأ -->
            <div class="error-number">404</div>
            
            <!-- رسالة الخطأ -->
            <div class="error-message">
              <h2>الصفحة غير موجودة</h2>
              <p class="lead">عذراً، الصفحة التي تبحث عنها غير موجودة أو تم نقلها إلى موقع آخر.</p>
            </div>
            
            <!-- الإجراءات -->
            <div class="error-actions">
              <router-link to="/" class="btn btn-primary btn-lg me-3">
                <i class="fas fa-home me-2"></i>
                العودة للرئيسية
              </router-link>
              
              <button @click="goBack" class="btn btn-outline-secondary btn-lg">
                <i class="fas fa-arrow-right me-2"></i>
                العودة للخلف
              </button>
            </div>
            
            <!-- روابط مفيدة -->
            <div class="helpful-links mt-5">
              <h5>روابط مفيدة:</h5>
              <div class="row mt-3">
                <div class="col-6 col-md-3 mb-3">
                  <router-link to="/diagnosis/dashboard" class="link-card">
                    <i class="fas fa-stethoscope"></i>
                    <span>التشخيص</span>
                  </router-link>
                </div>
                <div class="col-6 col-md-3 mb-3">
                  <router-link to="/ai/agent" class="link-card">
                    <i class="fas fa-robot"></i>
                    <span>المساعد الذكي</span>
                  </router-link>
                </div>
                <div class="col-6 col-md-3 mb-3">
                  <router-link to="/docker/management" class="link-card">
                    <i class="fab fa-docker"></i>
                    <span>إدارة الحاويات</span>
                  </router-link>
                </div>
                <div class="col-6 col-md-3 mb-3">
                  <router-link to="/admin/settings" class="link-card">
                    <i class="fas fa-cog"></i>
                    <span>الإعدادات</span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'NotFound',
  
  setup() {
    const router = useRouter()
    
    const goBack = () => {
      if (window.history.length > 1) {
        router.go(-1)
      } else {
        router.push('/')
      }
    }
    
    return {
      goBack
    }
  }
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-family: 'Cairo', sans-serif;
}

.error-number {
  font-size: 8rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 2rem;
  background: linear-gradient(45deg, #fff, #f8f9fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.error-message h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.error-message p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 3rem;
}

.error-actions {
  margin-bottom: 4rem;
}

.btn {
  font-family: 'Cairo', sans-serif;
  font-weight: 600;
  border-radius: 50px;
  padding: 12px 30px;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(45deg, #4e73df, #224abe);
  border: none;
  box-shadow: 0 4px 15px rgba(78, 115, 223, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(78, 115, 223, 0.6);
}

.btn-outline-secondary {
  border: 2px solid rgba(255, 255, 255, 0.5);
  color: white;
  background: transparent;
}

.btn-outline-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
  transform: translateY(-2px);
}

.helpful-links h5 {
  font-weight: 600;
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

.link-card {
  display: block;
  padding: 1.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  text-decoration: none;
  color: white;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.link-card:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-5px);
  color: white;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.link-card i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  display: block;
}

.link-card span {
  font-size: 0.9rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .error-number {
    font-size: 6rem;
  }
  
  .error-message h2 {
    font-size: 2rem;
  }
  
  .error-message p {
    font-size: 1rem;
  }
  
  .btn {
    padding: 10px 25px;
    font-size: 0.9rem;
  }
  
  .error-actions .btn {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
  }
  
  .error-actions .btn:last-child {
    margin-bottom: 0;
  }
}
</style>

