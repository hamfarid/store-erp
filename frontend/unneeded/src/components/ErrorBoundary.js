/**
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/components/ErrorBoundary.js
 * 
 * مكون Error Boundary لمعالجة الأخطاء في الواجهة الأمامية
 * 
 * يشمل:
 * - التقاط الأخطاء في React components
 * - عرض رسائل خطأ مفيدة للمستخدم
 * - تسجيل الأخطاء للمطورين
 * - إعادة تحميل المكونات
 * - إرسال تقارير الأخطاء للخادم
 */

import React, { Component } from 'react';
import { Alert, Button, Card, Typography, Space, Result, Collapse } from 'antd';
import {
  ReloadOutlined,
  HomeOutlined,
  SendOutlined,
  BugOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Panel } = Collapse;

class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null,
            errorId: null,
            isReporting: false,
            reportSent: false
        };
    }

    static getDerivedStateFromError(error) {
        // تحديث الحالة لعرض واجهة الخطأ
        return { 
            hasError: true,
            error: error,
            errorId: this.generateErrorId(error)
        };
    }

    componentDidCatch(error, errorInfo) {
        // تسجيل تفاصيل الخطأ
        this.setState({
            error: error,
            errorInfo: errorInfo,
            errorId: this.generateErrorId(error)
        });

        // تسجيل الخطأ في console للمطورين
        // إرسال تقرير الخطأ للخادم (اختياري)
        this.reportErrorToServer(error, errorInfo);
    }

    generateErrorId = (error) => {
        const timestamp = Date.now();
        const errorString = error.toString();
        return `ERR_${timestamp}_${errorString.slice(0, 8).toUpperCase()}`;
    }

    reportErrorToServer = async (error, errorInfo) => {
        try {
            const errorReport = {
                message: error.message,
                stack: error.stack,
                componentStack: errorInfo.componentStack,
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent,
                url: window.location.href,
                userId: localStorage.getItem('userId') || 'anonymous',
                errorId: this.state.errorId
            };

            // إرسال التقرير للخادم
            await fetch('/api/errors/report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(errorReport)
            });

        } catch (reportError) {
            }
    }

    handleReload = () => {
        // إعادة تحميل المكون
        this.setState({
            hasError: false,
            error: null,
            errorInfo: null,
            errorId: null,
            reportSent: false
        });
    }

    handleGoHome = () => {
        // العودة للصفحة الرئيسية
        window.location.href = '/';
    }

    handleSendReport = async () => {
        this.setState({ isReporting: true });
        
        try {
            await this.reportErrorToServer(this.state.error, this.state.errorInfo);
            this.setState({ reportSent: true });
        } catch (error) {
            } finally {
            this.setState({ isReporting: false });
        }
    }

    getErrorSeverity = (error) => {
        // تحديد خطورة الخطأ بناءً على نوعه
        if (error.name === 'ChunkLoadError') return 'warning';
        if (error.message.includes('Network')) return 'error';
        if (error.message.includes('Permission')) return 'warning';
        return 'error';
    }

    getErrorCategory = (error) => {
        // تصنيف الخطأ
        if (error.name === 'ChunkLoadError') return 'تحميل الموارد';
        if (error.message.includes('Network')) return 'الشبكة';
        if (error.message.includes('Permission')) return 'الصلاحيات';
        if (error.message.includes('Render')) return 'عرض المكونات';
        return 'عام';
    }

    getUserFriendlyMessage = (error) => {
        // رسائل مفهومة للمستخدم
        if (error.name === 'ChunkLoadError') {
            return 'فشل في تحميل جزء من التطبيق. قد يكون هناك تحديث جديد متاح.';
        }
        if (error.message.includes('Network')) {
            return 'مشكلة في الاتصال بالشبكة. تحقق من اتصال الإنترنت.';
        }
        if (error.message.includes('Permission')) {
            return 'ليس لديك صلاحية للوصول إلى هذه الميزة.';
        }
        return 'حدث خطأ غير متوقع في التطبيق.';
    }

    getSolutions = (error) => {
        // اقتراحات لحل المشكلة
        if (error.name === 'ChunkLoadError') {
            return [
                'أعد تحميل الصفحة (F5)',
                'امسح ذاكرة التخزين المؤقت للمتصفح',
                'تحقق من وجود تحديثات للتطبيق'
            ];
        }
        if (error.message.includes('Network')) {
            return [
                'تحقق من اتصال الإنترنت',
                'أعد تحميل الصفحة',
                'جرب مرة أخرى بعد قليل'
            ];
        }
        return [
            'أعد تحميل الصفحة',
            'اتصل بالدعم الفني',
            'جرب استخدام متصفح آخر'
        ];
    }

    render() {
        if (this.state.hasError) {
            const { error, errorInfo, errorId } = this.state;
            const severity = this.getErrorSeverity(error);
            const category = this.getErrorCategory(error);
            const userMessage = this.getUserFriendlyMessage(error);
            const solutions = this.getSolutions(error);

            return (
                <div style={{ 
                    padding: '24px', 
                    minHeight: '100vh',
                    backgroundColor: '#f5f5f5',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    <Card 
                        style={{ 
                            maxWidth: 800, 
                            width: '100%',
                            boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                        }}
                    >
                        <Result
                            status="error"
                            title="حدث خطأ في التطبيق"
                            subTitle={userMessage}
                            extra={[
                                <Button 
                                    type="primary" 
                                    icon={<ReloadOutlined />}
                                    onClick={this.handleReload}
                                    key="reload"
                                >
                                    إعادة المحاولة
                                </Button>,
                                <Button 
                                    icon={<HomeOutlined />}
                                    onClick={this.handleGoHome}
                                    key="home"
                                >
                                    العودة للرئيسية
                                </Button>
                            ]}
                        />

                        <Space direction="vertical" style={{ width: '100%' }} size="large">
                            {/* معلومات الخطأ الأساسية */}
                            <Alert
                                message={`خطأ في ${category}`}
                                description={
                                    <div>
                                        <Text strong>معرف الخطأ: </Text>
                                        <Text code>{errorId}</Text>
                                        <br />
                                        <Text strong>الوقت: </Text>
                                        <Text>{new Date().toLocaleString('ar-SA')}</Text>
                                    </div>
                                }
                                type={severity}
                                showIcon
                            />

                            {/* الحلول المقترحة */}
                            <Card title="الحلول المقترحة" size="small">
                                <ul>
                                    {solutions.map((solution, index) => (
                                        <li key={index}>
                                            <Text>{solution}</Text>
                                        </li>
                                    ))}
                                </ul>
                            </Card>

                            {/* إرسال تقرير الخطأ */}
                            <Card title="إرسال تقرير الخطأ" size="small">
                                <Paragraph>
                                    يمكنك إرسال تقرير مفصل عن هذا الخطأ لمساعدتنا في تحسين التطبيق.
                                </Paragraph>
                                <Space>
                                    <Button
                                        type="default"
                                        icon={<SendOutlined />}
                                        loading={this.state.isReporting}
                                        disabled={this.state.reportSent}
                                        onClick={this.handleSendReport}
                                    >
                                        {this.state.reportSent ? 'تم الإرسال' : 'إرسال التقرير'}
                                    </Button>
                                    {this.state.reportSent && (
                                        <Text type="success">
                                            ✓ تم إرسال التقرير بنجاح
                                        </Text>
                                    )}
                                </Space>
                            </Card>

                            {/* تفاصيل تقنية (للمطورين) */}
                            {typeof import.meta !== 'undefined' && import.meta.env?.DEV && (
                                <Collapse>
                                    <Panel 
                                        header={
                                            <span>
                                                <BugOutlined /> تفاصيل تقنية (للمطورين)
                                            </span>
                                        } 
                                        key="technical"
                                    >
                                        <Space direction="vertical" style={{ width: '100%' }}>
                                            <div>
                                                <Text strong>نوع الخطأ:</Text>
                                                <br />
                                                <Text code>{error.name}</Text>
                                            </div>
                                            
                                            <div>
                                                <Text strong>رسالة الخطأ:</Text>
                                                <br />
                                                <Text code>{error.message}</Text>
                                            </div>
                                            
                                            <div>
                                                <Text strong>Stack Trace:</Text>
                                                <br />
                                                <pre style={{ 
                                                    backgroundColor: '#f5f5f5', 
                                                    padding: '8px',
                                                    fontSize: '12px',
                                                    overflow: 'auto',
                                                    maxHeight: '200px'
                                                }}>
                                                    {error.stack}
                                                </pre>
                                            </div>
                                            
                                            {errorInfo && (
                                                <div>
                                                    <Text strong>Component Stack:</Text>
                                                    <br />
                                                    <pre style={{ 
                                                        backgroundColor: '#f5f5f5', 
                                                        padding: '8px',
                                                        fontSize: '12px',
                                                        overflow: 'auto',
                                                        maxHeight: '200px'
                                                    }}>
                                                        {errorInfo.componentStack}
                                                    </pre>
                                                </div>
                                            )}
                                        </Space>
                                    </Panel>
                                </Collapse>
                            )}
                        </Space>
                    </Card>
                </div>
            );
        }

        // إذا لم يكن هناك خطأ، عرض المكونات الفرعية
        return this.props.children;
    }
}

// مكون مساعد لمعالجة أخطاء محددة
export const withErrorBoundary = (WrappedComponent, errorBoundaryProps = {}) => {
    return function WithErrorBoundaryComponent(props) {
        return (
            <ErrorBoundary {...errorBoundaryProps}>
                <WrappedComponent {...props} />
            </ErrorBoundary>
        );
    };
};

// Hook لمعالجة الأخطاء في functional components
export const useErrorHandler = () => {
    const handleError = (error, errorInfo = {}) => {
        // تسجيل الخطأ
        // يمكن إضافة منطق إضافي هنا مثل:
        // - إرسال تقرير للخادم
        // - عرض notification
        // - تحديث state management
        
        // إرسال تقرير للخادم
        const errorReport = {
            message: error.message,
            stack: error.stack,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href,
            userId: localStorage.getItem('userId') || 'anonymous',
            ...errorInfo
        };

        fetch('/api/errors/report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(errorReport)
        }).catch(reportError => {
            });
    };

    return { handleError };
};

// مكون لعرض رسائل خطأ بسيطة
export const ErrorMessage = ({ 
    error, 
    onRetry, 
    onDismiss,
    showDetails = false 
}) => {
    if (!error) return null;

    const getUserFriendlyMessage = (error) => {
        if (typeof error === 'string') return error;
        if (error.response?.data?.message) return error.response.data.message;
        if (error.message) return error.message;
        return 'حدث خطأ غير متوقع';
    };

    return (
        <Alert
            message="حدث خطأ"
            description={getUserFriendlyMessage(error)}
            type="error"
            showIcon
            closable={!!onDismiss}
            onClose={onDismiss}
            action={
                onRetry && (
                    <Button size="small" onClick={onRetry}>
                        إعادة المحاولة
                    </Button>
                )
            }
            style={{ marginBottom: 16 }}
        />
    );
};

export default ErrorBoundary;

