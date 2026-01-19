# /home/ubuntu/image_search_integration/auto_learning/tests/integration_test.js

/**
 * اختبارات التكامل للبحث الذاتي الذكي
 * 
 * هذا الملف يحتوي على اختبارات التكامل بين مكونات نظام البحث الذاتي الذكي
 * للتأكد من عمل جميع العمليات بشكل صحيح وتكامل الواجهات الأمامية مع الخلفية.
 */

import { mount } from '@vue/test-utils';
import { createStore } from 'vuex';
import { createRouter, createWebHistory } from 'vue-router';
import KeywordManager from '../frontend/KeywordManager.vue';
import SourceManager from '../frontend/SourceManager.vue';
import SearchEngineManager from '../frontend/SearchEngineManager.vue';
import KeywordApiService from '../services/KeywordApiService';
import SourceApiService from '../services/SourceApiService';
import SearchEngineApiService from '../services/SearchEngineApiService';
import PermissionService from '../services/PermissionService';

// Mock للخدمات API
jest.mock('../services/KeywordApiService');
jest.mock('../services/SourceApiService');
jest.mock('../services/SearchEngineApiService');
jest.mock('../services/PermissionService');

describe('نظام البحث الذاتي الذكي - اختبارات التكامل', () => {
  let store;
  let router;
  
  beforeEach(() => {
    // إعداد مخزن Vuex للاختبارات
    store = createStore({
      state: {
        user: {
          id: 1,
          username: 'admin',
          email: 'admin@example.com',
          roles: ['admin']
        },
        permissions: {
          keyword: {
            read: true,
            create: true,
            update: true,
            delete: true
          },
          source: {
            read: true,
            create: true,
            update: true,
            delete: true,
            verify: true
          },
          search_engine: {
            read: true,
            create: true,
            update: true,
            delete: true,
            test: true
          }
        }
      },
      getters: {
        isAuthenticated: state => !!state.user,
        currentUser: state => state.user,
        hasPermission: state => (resource, action) => {
          return state.permissions[resource] && state.permissions[resource][action];
        }
      }
    });
    
    // إعداد موجه Vue للاختبارات
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/keywords', component: KeywordManager },
        { path: '/sources', component: SourceManager },
        { path: '/search-engines', component: SearchEngineManager }
      ]
    });
    
    // Mock لخدمة الصلاحيات
    PermissionService.hasPermission.mockImplementation((action, resource) => {
      return Promise.resolve(store.getters.hasPermission(resource, action));
    });
  });
  
  afterEach(() => {
    jest.clearAllMocks();
  });
  
  describe('إدارة الكلمات المفتاحية', () => {
    test('يجب أن يعرض قائمة الكلمات المفتاحية عند التحميل', async () => {
      // Mock لاستجابة API
      const mockKeywords = {
        data: {
          keywords: [
            { id: 1, text: 'طماطم', category: 'PLANT', is_active: true },
            { id: 2, text: 'تبقع أوراق', category: 'DISEASE', is_active: true }
          ],
          total_count: 2
        }
      };
      
      KeywordApiService.getKeywords.mockResolvedValue(mockKeywords);
      
      // تركيب المكون
      const wrapper = mount(KeywordManager, {
        global: {
          plugins: [store, router],
          stubs: {
            'font-awesome-icon': true,
            'v-tooltip': true
          }
        }
      });
      
      // انتظار تحميل البيانات
      await wrapper.vm.$nextTick();
      
      // التحقق من استدعاء API
      expect(KeywordApiService.getKeywords).toHaveBeenCalled();
      
      // التحقق من عرض البيانات
      expect(wrapper.vm.keywords.length).toBe(2);
      expect(wrapper.text()).toContain('طماطم');
      expect(wrapper.text()).toContain('تبقع أوراق');
    });
    
    test('يجب أن يضيف كلمة مفتاحية جديدة بنجاح', async () => {
      // Mock لاستجابة API
      KeywordApiService.createKeyword.mockResolvedValue({
        data: { id: 3, text: 'ري', category: 'TECHNIQUE', is_active: true }
      });
      
      // تركيب المكون
      const wrapper = mount(KeywordManager, {
        global: {
          plugins: [store, router],
          stubs: {
            'font-awesome-icon': true,
            'v-tooltip': true
          }
        }
      });
      
      // تعيين بيانات الكلمة المفتاحية الجديدة
      wrapper.vm.currentKeyword = {
        text: 'ري',
        category: 'TECHNIQUE',
        is_active: true
      };
      
      // استدعاء دالة الحفظ
      await wrapper.vm.saveKeyword();
      
      // التحقق من استدعاء API
      expect(KeywordApiService.createKeyword).toHaveBeenCalledWith({
        text: 'ري',
        category: 'TECHNIQUE',
        is_active: true
      });
    });
  });
  
  describe('إدارة المصادر الموثوقة', () => {
    test('يجب أن يعرض قائمة المصادر عند التحميل', async () => {
      // Mock لاستجابة API
      const mockSources = {
        data: {
          sources: [
            { id: 1, domain: 'example.com', category: 'ACADEMIC', trust_level: 80, is_active: true },
            { id: 2, domain: 'research.org', category: 'RESEARCH', trust_level: 90, is_active: true }
          ],
          total_count: 2
        }
      };
      
      SourceApiService.getSources.mockResolvedValue(mockSources);
      
      // تركيب المكون
      const wrapper = mount(SourceManager, {
        global: {
          plugins: [store, router],
          stubs: {
            'font-awesome-icon': true,
            'v-tooltip': true
          }
        }
      });
      
      // انتظار تحميل البيانات
      await wrapper.vm.$nextTick();
      
      // التحقق من استدعاء API
      expect(SourceApiService.getSources).toHaveBeenCalled();
      
      // التحقق من عرض البيانات
      expect(wrapper.vm.sources.length).toBe(2);
      expect(wrapper.text()).toContain('example.com');
      expect(wrapper.text()).toContain('research.org');
    });
    
    test('يجب أن يتحقق من مصدر بنجاح', async () => {
      // Mock لاستجابة API
      SourceApiService.verifySource.mockResolvedValue({
        data: {
          domain: 'example.com',
          ip_address: '192.168.1.1',
          country: 'US',
          registration_date: '2020-01-01',
          hosting_provider: 'AWS',
          has_ssl: true,
          site_age: '3 years',
          alexa_rank: 10000,
          security_score: 85,
          content_score: 75,
          spam_blacklist: false,
          malware_blacklist: false,
          has_privacy_policy: true,
          original_content: true,
          has_citations: true,
          has_contact_info: true,
          recommendation: 'مصدر موثوق يمكن استخدامه',
          suggested_trust_level: 85
        }
      });
      
      // تركيب المكون
      const wrapper = mount(SourceManager, {
        global: {
          plugins: [store, router],
          stubs: {
            'font-awesome-icon': true,
            'v-tooltip': true
          }
        }
      });
      
      // تعيين المصدر للتحقق
      wrapper.vm.currentSourceToVerify = {
        id: 1,
        domain: 'example.com'
      };
      
      // استدعاء دالة التحقق
      await wrapper.vm.startSourceVerification();
      
      // التحقق من استدعاء API
      expect(SourceApiService.verifySource).toHaveBeenCalledWith(1);
      
      // التحقق من نتائج التحقق
      expect(wrapper.vm.verificationStatus.result).toBeTruthy();
      expect(wrapper.vm.verificationStatus.result.suggested_trust_level).toBe(85);
    });
  });
  
  describe('إدارة محركات البحث', () => {
    test('يجب أن يعرض قائمة محركات البحث عند التحميل', async () => {
      // Mock لاستجابة API
      const mockEngines = {
        data: {
          search_engines: [
            { id: 1, name: 'Google', type: 'GENERAL', base_url: 'https://www.google.com/search', query_param: 'q', priority: 1, is_active: true },
            { id: 2, name: 'Bing', type: 'GENERAL', base_url: 'https://www.bing.com/search', query_param: 'q', priority: 2, is_active: true }
          ],
          total_count: 2
        }
      };
      
      SearchEngineApiService.getSearchEngines.mockResolvedValue(mockEngines);
      
      // تركيب المكون
      const wrapper = mount(SearchEngineManager, {
        global: {
          plugins: [store, router],
          stubs: {
            'font-awesome-icon': true,
            'v-tooltip': true
          }
        }
      });
      
      // انتظار تحميل البيانات
      await wrapper.vm.$nextTick();
      
      // التحقق من استدعاء API
      expect(SearchEngineApiService.getSearchEngines).toHaveBeenCalled();
      
      // التحقق من عرض البيانات
      expect(wrapper.vm.engines.length).toBe(2);
      expect(wrapper.text()).toContain('Google');
      expect(wrapper.text()).toContain('Bing');
    });
    
    test('يجب أن يختبر محرك بحث بنجاح', async () => {
      // Mock لاستجابة API
      SearchEngineApiService.testSearchEngine.mockResolvedValue({
        data: {
          results: [
            { title: 'نتيجة 1', snippet: 'وصف النتيجة 1', link: 'https://example.com/1' },
            { title: 'نتيجة 2', snippet: 'وصف النتيجة 2', link: 'https://example.com/2' }
          ],
          constructed_url: 'https://www.google.com/search?q=الزراعة+الذكية'
        }
      });
      
      // تركيب المكون
      const wrapper = mount(SearchEngineManager, {
        global: {
          plugins: [store, router],
          stubs: {
            'font-awesome-icon': true,
            'v-tooltip': true
          }
        }
      });
      
      // تعيين محرك البحث للاختبار
      wrapper.vm.currentEngineToTest = {
        id: 1,
        name: 'Google'
      };
      wrapper.vm.testQuery = 'الزراعة الذكية';
      wrapper.vm.testNumResults = 2;
      
      // استدعاء دالة الاختبار
      await wrapper.vm.runEngineTest();
      
      // التحقق من استدعاء API
      expect(SearchEngineApiService.testSearchEngine).toHaveBeenCalledWith(1, 'الزراعة الذكية', 2);
      
      // التحقق من نتائج الاختبار
      expect(wrapper.vm.testResults.results).toBeTruthy();
      expect(wrapper.vm.testResults.results.length).toBe(2);
      expect(wrapper.vm.testResults.constructed_url).toBe('https://www.google.com/search?q=الزراعة+الذكية');
    });
  });
  
  describe('اختبارات الصلاحيات', () => {
    test('يجب أن يخفي أزرار الإضافة والتعديل والحذف عند عدم وجود صلاحيات', async () => {
      // تعديل الصلاحيات في المخزن
      store.state.permissions.keyword = {
        read: true,
        create: false,
        update: false,
        delete: false
      };
      
      // Mock لاستجابة API
      const mockKeywords = {
        data: {
          keywords: [
            { id: 1, text: 'طماطم', category: 'PLANT', is_active: true }
          ],
          total_count: 1
        }
      };
      
      KeywordApiService.getKeywords.mockResolvedValue(mockKeywords);
      
      // تركيب المكون
      const wrapper = mount(KeywordManager, {
        global: {
          plugins: [store, router],
          stubs: {
            'font-awesome-icon': true,
            'v-tooltip': true
          }
        }
      });
      
      // انتظار تحميل البيانات
      await wrapper.vm.$nextTick();
      
      // التحقق من عدم وجود زر الإضافة
      expect(wrapper.vm.canCreateKeyword).toBe(false);
      
      // التحقق من عدم وجود أزرار التعديل والحذف
      expect(wrapper.vm.canUpdateKeyword).toBe(false);
      expect(wrapper.vm.canDeleteKeyword).toBe(false);
    });
  });
  
  describe('اختبارات التكامل الشامل', () => {
    test('يجب أن يعمل تدفق العمل الكامل لإضافة كلمة مفتاحية وربطها بمصدر', async () => {
      // Mock لاستجابات API
      KeywordApiService.createKeyword.mockResolvedValue({
        data: { id: 3, text: 'ري بالتنقيط', category: 'TECHNIQUE', is_active: true }
      });
      
      SourceApiService.getSources.mockResolvedValue({
        data: {
          sources: [
            { id: 1, domain: 'example.com', category: 'ACADEMIC', trust_level: 80, is_active: true }
          ],
          total_count: 1
        }
      });
      
      KeywordApiService.addKeywordRelation.mockResolvedValue({
        data: { success: true }
      });
      
      // تنفيذ تدفق العمل
      // 1. إضافة كلمة مفتاحية جديدة
      const keywordWrapper = mount(KeywordManager, {
        global: {
          plugins: [store, router],
          stubs: {
            'font-awesome-icon': true,
            'v-tooltip': true
          }
        }
      });
      
      keywordWrapper.vm.currentKeyword = {
        text: 'ري بالتنقيط',
        category: 'TECHNIQUE',
        is_active: true
      };
      
      await keywordWrapper.vm.saveKeyword();
      
      // التحقق من استدعاء API لإضافة الكلمة المفتاحية
      expect(KeywordApiService.createKeyword).toHaveBeenCalledWith({
        text: 'ري بالتنقيط',
        category: 'TECHNIQUE',
        is_active: true
      });
      
      // 2. ربط الكلمة المفتاحية بمصدر
      await keywordWrapper.vm.addKeywordRelation(3, 1, 'SOURCE_REFERENCE');
      
      // التحقق من استدعاء API لإضافة العلاقة
      expect(KeywordApiService.addKeywordRelation).toHaveBeenCalledWith(3, 1, 'SOURCE_REFERENCE');
    });
  });
});
