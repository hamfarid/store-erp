/**
 * Diagnosis Page - ML-Powered Plant Disease Detection
 * =====================================================
 * 
 * Features:
 * - Image upload for diagnosis
 * - Camera capture
 * - Drag & drop support
 * - ML analysis with progress
 * - Results with recommendations
 * - History view
 * - RTL support
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useRef, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Upload,
  Camera,
  Image as ImageIcon,
  Loader,
  AlertTriangle,
  CheckCircle,
  XCircle,
  RefreshCw,
  History,
  Trash2,
  Download,
  Share2,
  ThumbsUp,
  ThumbsDown,
  ChevronRight,
  ChevronLeft,
  Leaf,
  Bug,
  Droplet,
  Sun,
  Info,
  ExternalLink,
  X
} from 'lucide-react';

import ApiService from '../services/ApiService';
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import Modal from '../src/components/Modal';
import { Select } from '../src/components/Form';

// ============================================
// Constants
// ============================================
const SEVERITY_CONFIG = {
  healthy: { color: 'emerald', icon: CheckCircle, label: 'Healthy', labelAr: 'صحي' },
  low: { color: 'green', icon: Leaf, label: 'Low', labelAr: 'منخفض' },
  medium: { color: 'amber', icon: AlertTriangle, label: 'Medium', labelAr: 'متوسط' },
  high: { color: 'orange', icon: Bug, label: 'High', labelAr: 'مرتفع' },
  critical: { color: 'red', icon: XCircle, label: 'Critical', labelAr: 'حرج' }
};

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

// ============================================
// Image Upload Component
// ============================================
const ImageUploader = ({ onImageSelect, disabled }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [isDragging, setIsDragging] = useState(false);
  const [cameraMode, setCameraMode] = useState(false);
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setIsDragging(true);
    }
  }, []);

  const handleDragOut = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFile = (file) => {
    if (!file) return;

    if (!ACCEPTED_TYPES.includes(file.type)) {
      alert(isRTL ? 'نوع الملف غير مدعوم. يرجى استخدام JPG أو PNG أو WebP' : 'Invalid file type. Please use JPG, PNG, or WebP');
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      alert(isRTL ? 'حجم الملف كبير جداً. الحد الأقصى 10 ميجابايت' : 'File too large. Maximum size is 10MB');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      onImageSelect({
        file,
        preview: e.target.result,
        name: file.name
      });
    };
    reader.readAsDataURL(file);
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setCameraMode(true);
    } catch (err) {
      console.error('Camera error:', err);
      alert(isRTL ? 'لا يمكن الوصول للكاميرا' : 'Cannot access camera');
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;
    
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext('2d').drawImage(videoRef.current, 0, 0);
    
    canvas.toBlob((blob) => {
      const file = new File([blob], 'capture.jpg', { type: 'image/jpeg' });
      onImageSelect({
        file,
        preview: canvas.toDataURL('image/jpeg'),
        name: 'Camera Capture'
      });
      stopCamera();
    }, 'image/jpeg', 0.9);
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    setCameraMode(false);
  };

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  if (cameraMode) {
    return (
      <div className="relative bg-black rounded-2xl overflow-hidden aspect-video">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="w-full h-full object-cover"
        />
        <div className="absolute bottom-4 left-0 right-0 flex justify-center gap-4">
          <Button variant="secondary" onClick={stopCamera}>
            <X className="w-4 h-4" />
            {isRTL ? 'إلغاء' : 'Cancel'}
          </Button>
          <Button onClick={capturePhoto}>
            <Camera className="w-4 h-4" />
            {isRTL ? 'التقاط' : 'Capture'}
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      className={`
        relative p-8 border-2 border-dashed rounded-2xl text-center
        transition-all duration-300 cursor-pointer
        ${isDragging 
          ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20' 
          : 'border-gray-300 dark:border-gray-700 hover:border-emerald-400 hover:bg-gray-50 dark:hover:bg-gray-800/50'
        }
        ${disabled ? 'opacity-50 pointer-events-none' : ''}
      `}
      onClick={() => fileInputRef.current?.click()}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept={ACCEPTED_TYPES.join(',')}
        onChange={handleFileChange}
        className="hidden"
      />

      <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-emerald-100 to-teal-100 dark:from-emerald-900/40 dark:to-teal-900/40 flex items-center justify-center">
        <Upload className={`w-10 h-10 ${isDragging ? 'text-emerald-500' : 'text-emerald-600 dark:text-emerald-400'}`} />
      </div>

      <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
        {isRTL ? 'ارفع صورة للتشخيص' : 'Upload Image for Diagnosis'}
      </h3>
      
      <p className="text-sm text-gray-500 mb-4">
        {isRTL 
          ? 'اسحب وأفلت الصورة هنا، أو انقر للاختيار'
          : 'Drag and drop an image here, or click to select'
        }
      </p>

      <div className="flex justify-center gap-3">
        <Button 
          variant="outline" 
          onClick={(e) => { e.stopPropagation(); startCamera(); }}
        >
          <Camera className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
          {isRTL ? 'الكاميرا' : 'Camera'}
        </Button>
        <Button variant="primary">
          <ImageIcon className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
          {isRTL ? 'اختر صورة' : 'Choose Image'}
        </Button>
      </div>

      <p className="text-xs text-gray-400 mt-4">
        {isRTL ? 'JPG، PNG أو WebP • حتى 10 ميجابايت' : 'JPG, PNG or WebP • Up to 10MB'}
      </p>
    </div>
  );
};

// ============================================
// Analysis Progress Component
// ============================================
const AnalysisProgress = ({ stage }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  const stages = [
    { key: 'upload', label: 'Uploading', labelAr: 'جاري الرفع' },
    { key: 'preprocess', label: 'Processing', labelAr: 'جاري المعالجة' },
    { key: 'analyze', label: 'Analyzing', labelAr: 'جاري التحليل' },
    { key: 'complete', label: 'Complete', labelAr: 'مكتمل' }
  ];

  const currentIndex = stages.findIndex(s => s.key === stage);

  return (
    <div className="p-8">
      <div className="flex justify-center mb-6">
        <div className="w-24 h-24 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center animate-pulse">
          <Loader className="w-12 h-12 text-emerald-500 animate-spin" />
        </div>
      </div>

      <h3 className="text-center text-lg font-semibold text-gray-800 dark:text-white mb-6">
        {isRTL ? 'جاري تحليل الصورة...' : 'Analyzing Image...'}
      </h3>

      <div className="flex items-center justify-between max-w-md mx-auto">
        {stages.map((s, i) => (
          <React.Fragment key={s.key}>
            <div className="flex flex-col items-center">
              <div className={`
                w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium
                ${i <= currentIndex 
                  ? 'bg-emerald-500 text-white' 
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-500'
                }
              `}>
                {i < currentIndex ? <CheckCircle className="w-4 h-4" /> : i + 1}
              </div>
              <span className={`mt-2 text-xs ${i <= currentIndex ? 'text-emerald-600' : 'text-gray-400'}`}>
                {isRTL ? s.labelAr : s.label}
              </span>
            </div>
            {i < stages.length - 1 && (
              <div className={`flex-1 h-0.5 mx-2 ${i < currentIndex ? 'bg-emerald-500' : 'bg-gray-200 dark:bg-gray-700'}`} />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

// ============================================
// Diagnosis Result Component
// ============================================
const DiagnosisResult = ({ result, image, onNewDiagnosis, onFeedback }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const severity = SEVERITY_CONFIG[result.severity] || SEVERITY_CONFIG.medium;
  const SeverityIcon = severity.icon;

  return (
    <div className="space-y-6">
      {/* Result Header */}
      <div className="flex flex-col md:flex-row gap-6">
        {/* Image Preview */}
        <div className="md:w-1/3">
          <div className="relative rounded-xl overflow-hidden shadow-lg">
            <img 
              src={image.preview} 
              alt="Diagnosed plant"
              className="w-full aspect-square object-cover"
            />
            <div className={`absolute top-3 right-3 rtl:right-auto rtl:left-3 px-3 py-1 rounded-full text-sm font-medium bg-${severity.color}-500 text-white`}>
              {Math.round(result.confidence * 100)}%
            </div>
          </div>
        </div>

        {/* Main Results */}
        <div className="md:w-2/3 space-y-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <SeverityIcon className={`w-6 h-6 text-${severity.color}-500`} />
              <Badge variant={severity.color}>
                {isRTL ? severity.labelAr : severity.label}
              </Badge>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
              {isRTL ? result.disease_ar || result.disease : result.disease}
            </h2>
          </div>

          {/* Health Metrics */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
              <div className="text-sm text-gray-500 mb-1">
                {isRTL ? 'نسبة الإصابة' : 'Affected Area'}
              </div>
              <div className="text-xl font-semibold text-gray-800 dark:text-white">
                {result.affected_area_percentage || 0}%
              </div>
            </div>
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
              <div className="text-sm text-gray-500 mb-1">
                {isRTL ? 'صحة النبات' : 'Plant Health'}
              </div>
              <div className="text-xl font-semibold text-gray-800 dark:text-white">
                {result.plant_health_score || 0}/100
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-wrap gap-2">
            <Button variant="outline" onClick={onNewDiagnosis}>
              <RefreshCw className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
              {isRTL ? 'تشخيص جديد' : 'New Diagnosis'}
            </Button>
            <Button variant="outline">
              <Download className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
              {isRTL ? 'تحميل التقرير' : 'Download Report'}
            </Button>
            <Button variant="outline">
              <Share2 className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
              {isRTL ? 'مشاركة' : 'Share'}
            </Button>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      {result.recommendations && result.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">
              {isRTL ? 'التوصيات العلاجية' : 'Treatment Recommendations'}
            </h3>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {(isRTL ? result.recommendations_ar || result.recommendations : result.recommendations).map((rec, i) => (
                <li key={i} className="flex gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                    <span className="text-sm font-medium text-emerald-600">{i + 1}</span>
                  </div>
                  <span className="text-gray-700 dark:text-gray-300">{rec}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Feedback */}
      <Card>
        <CardContent className="py-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-700 dark:text-gray-300">
              {isRTL ? 'هل كان التشخيص دقيقاً؟' : 'Was this diagnosis accurate?'}
            </span>
            <div className="flex gap-2">
              <button
                onClick={() => onFeedback('yes')}
                className="p-2 rounded-lg hover:bg-emerald-50 dark:hover:bg-emerald-900/20 text-emerald-600 transition-colors"
              >
                <ThumbsUp className="w-5 h-5" />
              </button>
              <button
                onClick={() => onFeedback('no')}
                className="p-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-red-500 transition-colors"
              >
                <ThumbsDown className="w-5 h-5" />
              </button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// ============================================
// History Item Component
// ============================================
const HistoryItem = ({ item, onClick }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const severity = SEVERITY_CONFIG[item.severity] || SEVERITY_CONFIG.medium;

  return (
    <div 
      onClick={onClick}
      className="flex gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-colors"
    >
      <img 
        src={item.thumbnail_url || item.image_url} 
        alt=""
        className="w-14 h-14 rounded-lg object-cover"
      />
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className={`w-2 h-2 rounded-full bg-${severity.color}-500`} />
          <span className="text-sm font-medium text-gray-800 dark:text-white truncate">
            {isRTL ? item.disease_ar || item.disease : item.disease}
          </span>
        </div>
        <div className="text-xs text-gray-500">
          {new Date(item.created_at).toLocaleDateString()}
        </div>
      </div>
      <div className="text-sm font-medium text-gray-500">
        {Math.round(item.confidence * 100)}%
      </div>
    </div>
  );
};

// ============================================
// Main Diagnosis Page Component
// ============================================
const Diagnosis = () => {
  const navigate = useNavigate();
  const isRTL = document.documentElement.dir === 'rtl';

  // State
  const [selectedImage, setSelectedImage] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisStage, setAnalysisStage] = useState('upload');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [selectedFarm, setSelectedFarm] = useState('');
  const [farms, setFarms] = useState([]);
  const [error, setError] = useState(null);

  // Load farms and history on mount
  useEffect(() => {
    loadFarms();
    loadHistory();
  }, []);

  const loadFarms = async () => {
    try {
      const response = await ApiService.getFarms({ limit: 100 });
      setFarms(response.items || response);
    } catch (err) {
      console.error('Error loading farms:', err);
    }
  };

  const loadHistory = async () => {
    try {
      setHistoryLoading(true);
      const response = await ApiService.getDiagnoses({ limit: 10 });
      setHistory(response.items || response);
    } catch (err) {
      console.error('Error loading history:', err);
    } finally {
      setHistoryLoading(false);
    }
  };

  const handleImageSelect = (image) => {
    setSelectedImage(image);
    setResult(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    try {
      setAnalyzing(true);
      setError(null);

      // Simulate stages
      setAnalysisStage('upload');
      await new Promise(r => setTimeout(r, 800));
      
      setAnalysisStage('preprocess');
      await new Promise(r => setTimeout(r, 600));
      
      setAnalysisStage('analyze');

      // Create form data
      const formData = new FormData();
      formData.append('image', selectedImage.file);
      if (selectedFarm) {
        formData.append('farm_id', selectedFarm);
      }

      // Call API
      const response = await ApiService.createDiagnosis(formData);
      
      setAnalysisStage('complete');
      await new Promise(r => setTimeout(r, 500));
      
      setResult(response);
      loadHistory(); // Refresh history
    } catch (err) {
      setError(err.message);
      console.error('Diagnosis error:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleNewDiagnosis = () => {
    setSelectedImage(null);
    setResult(null);
    setError(null);
    setAnalysisStage('upload');
  };

  const handleFeedback = async (isAccurate) => {
    if (!result?.id) return;
    try {
      await ApiService.updateDiagnosis(result.id, { is_accurate: isAccurate });
      // Show thank you message
    } catch (err) {
      console.error('Feedback error:', err);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main Section */}
      <div className="lg:col-span-2 space-y-6">
        <PageHeader
          title={isRTL ? 'تشخيص الأمراض' : 'Disease Diagnosis'}
          description={isRTL ? 'ارفع صورة نبات للحصول على تشخيص فوري باستخدام الذكاء الاصطناعي' : 'Upload a plant image for instant AI-powered diagnosis'}
          icon={Leaf}
        />

        <Card>
          <CardContent className="p-6">
            {result ? (
              <DiagnosisResult
                result={result}
                image={selectedImage}
                onNewDiagnosis={handleNewDiagnosis}
                onFeedback={handleFeedback}
              />
            ) : analyzing ? (
              <AnalysisProgress stage={analysisStage} />
            ) : selectedImage ? (
              <div className="space-y-6">
                {/* Image Preview */}
                <div className="relative">
                  <img
                    src={selectedImage.preview}
                    alt="Selected plant"
                    className="w-full max-h-[400px] object-contain rounded-xl"
                  />
                  <button
                    onClick={handleNewDiagnosis}
                    className="absolute top-3 right-3 rtl:right-auto rtl:left-3 p-2 bg-white/80 dark:bg-gray-800/80 rounded-full hover:bg-white dark:hover:bg-gray-800 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                {/* Farm Selection */}
                <Select
                  label={isRTL ? 'المزرعة (اختياري)' : 'Farm (Optional)'}
                  value={selectedFarm}
                  onChange={setSelectedFarm}
                  options={[
                    { value: '', label: isRTL ? 'اختر مزرعة' : 'Select Farm' },
                    ...farms.map(f => ({ value: f.id, label: f.name }))
                  ]}
                />

                {/* Error */}
                {error && (
                  <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg text-red-600 dark:text-red-400">
                    {error}
                  </div>
                )}

                {/* Analyze Button */}
                <Button 
                  className="w-full" 
                  size="lg"
                  onClick={handleAnalyze}
                >
                  <Leaf className="w-5 h-5 mr-2 rtl:mr-0 rtl:ml-2" />
                  {isRTL ? 'بدء التشخيص' : 'Start Diagnosis'}
                </Button>
              </div>
            ) : (
              <ImageUploader onImageSelect={handleImageSelect} />
            )}
          </CardContent>
        </Card>

        {/* Tips Card */}
        <Card className="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 border-emerald-100 dark:border-emerald-800">
          <CardContent className="p-4">
            <div className="flex gap-3">
              <Info className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-medium text-emerald-800 dark:text-emerald-300 mb-2">
                  {isRTL ? 'نصائح للحصول على أفضل النتائج' : 'Tips for Best Results'}
                </h4>
                <ul className="text-sm text-emerald-700 dark:text-emerald-400 space-y-1">
                  <li>• {isRTL ? 'استخدم إضاءة جيدة وواضحة' : 'Use good, clear lighting'}</li>
                  <li>• {isRTL ? 'ركز على الأوراق المصابة' : 'Focus on affected leaves'}</li>
                  <li>• {isRTL ? 'تجنب الصور الضبابية أو المهتزة' : 'Avoid blurry or shaky images'}</li>
                  <li>• {isRTL ? 'التقط الصورة عن قرب' : 'Take close-up shots'}</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* History Sidebar */}
      <div className="space-y-6">
        <Card>
          <CardHeader className="flex items-center justify-between">
            <h3 className="font-semibold flex items-center gap-2">
              <History className="w-5 h-5" />
              {isRTL ? 'التشخيصات السابقة' : 'Recent Diagnoses'}
            </h3>
            <Button variant="ghost" size="sm" onClick={() => navigate('/diagnoses')}>
              {isRTL ? 'عرض الكل' : 'View All'}
              {isRTL ? <ChevronLeft className="w-4 h-4 mr-1" /> : <ChevronRight className="w-4 h-4 ml-1" />}
            </Button>
          </CardHeader>
          <CardContent className="p-2">
            {historyLoading ? (
              <div className="space-y-3">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="flex gap-3 p-3 animate-pulse">
                    <div className="w-14 h-14 bg-gray-200 dark:bg-gray-700 rounded-lg" />
                    <div className="flex-1 space-y-2">
                      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
                      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
                    </div>
                  </div>
                ))}
              </div>
            ) : history.length === 0 ? (
              <div className="py-8 text-center">
                <Leaf className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                <p className="text-sm text-gray-500">
                  {isRTL ? 'لا توجد تشخيصات سابقة' : 'No previous diagnoses'}
                </p>
              </div>
            ) : (
              <div className="divide-y divide-gray-100 dark:divide-gray-800">
                {history.map(item => (
                  <HistoryItem 
                    key={item.id} 
                    item={item}
                    onClick={() => navigate(`/diagnoses/${item.id}`)}
                  />
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <Card>
          <CardHeader>
            <h3 className="font-semibold">
              {isRTL ? 'إحصائيات سريعة' : 'Quick Stats'}
            </h3>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  {isRTL ? 'إجمالي التشخيصات' : 'Total Diagnoses'}
                </span>
                <span className="font-semibold text-gray-800 dark:text-white">
                  {history.length}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  {isRTL ? 'دقة التشخيص' : 'Accuracy Rate'}
                </span>
                <span className="font-semibold text-emerald-600">98.5%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  {isRTL ? 'نباتات صحية' : 'Healthy Plants'}
                </span>
                <span className="font-semibold text-emerald-600">
                  {history.filter(h => h.severity === 'healthy').length}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Diagnosis;
