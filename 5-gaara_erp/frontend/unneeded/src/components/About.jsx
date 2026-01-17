import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Button } from '../ui/Button';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import { useToast } from '../ui/Toast';

const About = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  useEffect(() => {
    if (id) {
      loadData();
    }
  }, [id]);

  const loadData = async () => {
    setLoading(true);
    try {
      // TODO: تنفيذ تحميل البيانات من API
      // const response = await fetch(`/api/about/${id}`);
      // const result = await response.json();
      // setData(result);
      
      // بيانات تجريبية مؤقتة
      setData({
        id: id || 'new',
        name: 'عنصر تجريبي',
        description: 'وصف تجريبي للعنصر',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      });
    } catch (error) {
      console.error('خطأ في تحميل البيانات:', error);
      showToast('خطأ في تحميل البيانات', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      // TODO: تنفيذ حفظ البيانات
      showToast('تم الحفظ بنجاح', 'success');
    } catch (error) {
      console.error('خطأ في الحفظ:', error);
      showToast('خطأ في الحفظ', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('هل أنت متأكد من الحذف؟')) return;
    
    setLoading(true);
    try {
      // TODO: تنفيذ حذف البيانات
      showToast('تم الحذف بنجاح', 'success');
      navigate(-1);
    } catch (error) {
      console.error('خطأ في الحذف:', error);
      showToast('خطأ في الحذف', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-foreground">
          {id === 'new' ? `إضافة About` : `تفاصيل About`}
        </h1>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => navigate(-1)}
          >
            رجوع
          </Button>
          <Button
            onClick={handleSave}
            disabled={loading}
          >
            حفظ
          </Button>
          {id !== 'new' && (
            <Button
              variant="destructive"
              onClick={handleDelete}
              disabled={loading}
            >
              حذف
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>المعلومات الأساسية</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    الاسم
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    value={data?.name || ''}
                    onChange={(e) => setData(prev => ({...prev, name: e.target.value}))}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    الوصف
                  </label>
                  <textarea
                    className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    rows="4"
                    value={data?.description || ''}
                    onChange={(e) => setData(prev => ({...prev, description: e.target.value}))}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div>
          <Card>
            <CardHeader>
              <CardTitle>معلومات إضافية</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <span className="text-sm text-gray-500">تاريخ الإنشاء:</span>
                  <p className="text-sm font-medium">
                    {data?.createdAt ? new Date(data.createdAt).toLocaleDateString('ar-EG') : '-'}
                  </p>
                </div>
                
                <div>
                  <span className="text-sm text-gray-500">آخر تحديث:</span>
                  <p className="text-sm font-medium">
                    {data?.updatedAt ? new Date(data.updatedAt).toLocaleDateString('ar-EG') : '-'}
                  </p>
                </div>
                
                <div>
                  <span className="text-sm text-gray-500">المعرف:</span>
                  <p className="text-sm font-medium font-mono">
                    {data?.id || '-'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default About;
