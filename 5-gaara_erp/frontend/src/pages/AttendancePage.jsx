import React, { useState, useEffect, useCallback } from 'react';
import {
  Clock, Calendar, LogIn, LogOut, CheckCircle, XCircle,
  RefreshCw, Download, Filter, ChevronRight, ChevronLeft
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// UI Components
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

/**
 * صفحة الحضور والانصراف
 * Attendance Management Page
 */
const AttendancePage = () => {
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [userAttendance, setUserAttendance] = useState(null);
  const [stats, setStats] = useState({
    present: 0,
    absent: 0,
    late: 0,
    onLeave: 0,
  });

  // Load attendance records
  const loadAttendance = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get(`/api/hr/attendance?date=${selectedDate}`);
      
      if (response.success) {
        setAttendanceRecords(response.data || []);
        if (response.stats) {
          setStats(response.stats);
        }
      } else {
        // Demo data
        setAttendanceRecords([
          {
            id: 1,
            employee_id: 1,
            employee_name: 'أحمد محمد',
            department: 'تقنية المعلومات',
            check_in: '08:45:00',
            check_out: '17:30:00',
            status: 'present',
            late_minutes: 0,
            overtime_hours: 0.5,
          },
          {
            id: 2,
            employee_id: 2,
            employee_name: 'سارة أحمد',
            department: 'الموارد البشرية',
            check_in: '09:15:00',
            check_out: '17:00:00',
            status: 'late',
            late_minutes: 15,
            overtime_hours: 0,
          },
          {
            id: 3,
            employee_id: 3,
            employee_name: 'محمد علي',
            department: 'المالية',
            check_in: null,
            check_out: null,
            status: 'absent',
            late_minutes: 0,
            overtime_hours: 0,
          },
          {
            id: 4,
            employee_id: 4,
            employee_name: 'فاطمة خالد',
            department: 'المبيعات',
            check_in: null,
            check_out: null,
            status: 'leave',
            late_minutes: 0,
            overtime_hours: 0,
            leave_type: 'إجازة مرضية',
          },
          {
            id: 5,
            employee_id: 5,
            employee_name: 'عمر حسن',
            department: 'تقنية المعلومات',
            check_in: '08:30:00',
            check_out: '18:00:00',
            status: 'present',
            late_minutes: 0,
            overtime_hours: 1,
          },
        ]);
        setStats({ present: 2, absent: 1, late: 1, onLeave: 1 });
      }
    } catch (error) {
      console.log('Using demo attendance data:', error);
      setAttendanceRecords([
        { id: 1, employee_name: 'أحمد محمد', check_in: '08:45', check_out: '17:30', status: 'present' },
      ]);
      setStats({ present: 1, absent: 0, late: 0, onLeave: 0 });
    } finally {
      setIsLoading(false);
    }
  }, [selectedDate]);

  // Load user's attendance status
  const loadUserAttendance = useCallback(async () => {
    try {
      const response = await apiClient.get('/api/hr/attendance/my-status');
      if (response.success) {
        setUserAttendance(response.data);
      } else {
        // Demo user status
        setUserAttendance({
          checked_in: true,
          check_in_time: '08:45:00',
          checked_out: false,
          check_out_time: null,
        });
      }
    } catch (error) {
      setUserAttendance({
        checked_in: false,
        check_in_time: null,
        checked_out: false,
        check_out_time: null,
      });
    }
  }, []);

  useEffect(() => {
    loadAttendance();
    loadUserAttendance();
  }, [loadAttendance, loadUserAttendance]);

  // Handle check-in
  const handleCheckIn = async () => {
    try {
      const response = await apiClient.post('/api/hr/attendance/check-in');
      if (response.success) {
        toast.success('تم تسجيل الحضور بنجاح');
        loadUserAttendance();
        loadAttendance();
      } else {
        toast.success('وضع العرض - تم تسجيل الحضور');
        setUserAttendance(prev => ({
          ...prev,
          checked_in: true,
          check_in_time: new Date().toTimeString().split(' ')[0],
        }));
      }
    } catch (error) {
      toast.success('وضع العرض - تم تسجيل الحضور');
      setUserAttendance(prev => ({
        ...prev,
        checked_in: true,
        check_in_time: new Date().toTimeString().split(' ')[0],
      }));
    }
  };

  // Handle check-out
  const handleCheckOut = async () => {
    try {
      const response = await apiClient.post('/api/hr/attendance/check-out');
      if (response.success) {
        toast.success('تم تسجيل الانصراف بنجاح');
        loadUserAttendance();
        loadAttendance();
      } else {
        toast.success('وضع العرض - تم تسجيل الانصراف');
        setUserAttendance(prev => ({
          ...prev,
          checked_out: true,
          check_out_time: new Date().toTimeString().split(' ')[0],
        }));
      }
    } catch (error) {
      toast.success('وضع العرض - تم تسجيل الانصراف');
      setUserAttendance(prev => ({
        ...prev,
        checked_out: true,
        check_out_time: new Date().toTimeString().split(' ')[0],
      }));
    }
  };

  // Get status badge
  const getStatusBadge = (status) => {
    const badges = {
      present: { bg: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400', text: 'حاضر' },
      absent: { bg: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400', text: 'غائب' },
      late: { bg: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400', text: 'متأخر' },
      leave: { bg: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400', text: 'إجازة' },
    };
    const badge = badges[status] || badges.absent;
    return <span className={`px-2 py-1 rounded-full text-xs ${badge.bg}`}>{badge.text}</span>;
  };

  // Navigate dates
  const navigateDate = (days) => {
    const current = new Date(selectedDate);
    current.setDate(current.getDate() + days);
    setSelectedDate(current.toISOString().split('T')[0]);
  };

  // Format time
  const formatTime = (time) => {
    if (!time) return '-';
    return time.substring(0, 5);
  };

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Clock className="w-8 h-8" />
            الحضور والانصراف
          </h1>
          <p className="text-muted-foreground mt-1">إدارة ومتابعة حضور الموظفين</p>
        </div>
        <button
          onClick={() => toast.success('جاري تصدير التقرير...')}
          className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
        >
          <Download className="w-5 h-5" />
          تصدير التقرير
        </button>
      </div>

      {/* User Check-in/out Card */}
      <Card className="bg-gradient-to-l from-primary/10 to-transparent border-primary/20">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-4 bg-primary/20 rounded-full">
                <Clock className="w-8 h-8 text-primary" />
              </div>
              <div>
                <h2 className="text-xl font-bold">تسجيل الحضور</h2>
                <p className="text-muted-foreground">
                  {userAttendance?.checked_in
                    ? `تم تسجيل الحضور: ${formatTime(userAttendance.check_in_time)}`
                    : 'لم تقم بتسجيل الحضور بعد'}
                </p>
                {userAttendance?.checked_out && (
                  <p className="text-muted-foreground">
                    تم تسجيل الانصراف: {formatTime(userAttendance.check_out_time)}
                  </p>
                )}
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleCheckIn}
                disabled={userAttendance?.checked_in}
                className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <LogIn className="w-5 h-5" />
                تسجيل الحضور
              </button>
              <button
                onClick={handleCheckOut}
                disabled={!userAttendance?.checked_in || userAttendance?.checked_out}
                className="flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <LogOut className="w-5 h-5" />
                تسجيل الانصراف
              </button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-green-500/10 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.present}</p>
              <p className="text-sm text-muted-foreground">حاضر</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-red-500/10 rounded-lg">
              <XCircle className="w-6 h-6 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.absent}</p>
              <p className="text-sm text-muted-foreground">غائب</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-yellow-500/10 rounded-lg">
              <Clock className="w-6 h-6 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.late}</p>
              <p className="text-sm text-muted-foreground">متأخر</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-blue-500/10 rounded-lg">
              <Calendar className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.onLeave}</p>
              <p className="text-sm text-muted-foreground">إجازة</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Date Navigator & Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button
                onClick={() => navigateDate(-1)}
                className="p-2 hover:bg-muted rounded-lg"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="px-4 py-2 border border-border rounded-lg bg-background"
              />
              <button
                onClick={() => navigateDate(1)}
                className="p-2 hover:bg-muted rounded-lg"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <button
                onClick={() => setSelectedDate(new Date().toISOString().split('T')[0])}
                className="px-3 py-2 text-sm border border-border rounded-lg hover:bg-muted"
              >
                اليوم
              </button>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={loadAttendance}
                className="flex items-center gap-2 px-3 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                تحديث
              </button>
              <button className="flex items-center gap-2 px-3 py-2 border border-border rounded-lg hover:bg-muted">
                <Filter className="w-4 h-4" />
                تصفية
              </button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Attendance Table */}
      <Card>
        <CardHeader>
          <CardTitle>سجل الحضور - {new Date(selectedDate).toLocaleDateString('ar-EG', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="flex items-center justify-center p-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-muted">
                  <tr>
                    <th className="px-4 py-3 text-right">الموظف</th>
                    <th className="px-4 py-3 text-right">القسم</th>
                    <th className="px-4 py-3 text-right">وقت الحضور</th>
                    <th className="px-4 py-3 text-right">وقت الانصراف</th>
                    <th className="px-4 py-3 text-right">الحالة</th>
                    <th className="px-4 py-3 text-right">التأخير</th>
                    <th className="px-4 py-3 text-right">الإضافي</th>
                    <th className="px-4 py-3 text-right">ملاحظات</th>
                  </tr>
                </thead>
                <tbody>
                  {attendanceRecords.length === 0 ? (
                    <tr>
                      <td colSpan={8} className="px-4 py-8 text-center text-muted-foreground">
                        لا توجد سجلات حضور لهذا اليوم
                      </td>
                    </tr>
                  ) : (
                    attendanceRecords.map((record) => (
                      <tr key={record.id} className="border-b border-border hover:bg-muted/50">
                        <td className="px-4 py-3 font-medium">{record.employee_name}</td>
                        <td className="px-4 py-3 text-muted-foreground">{record.department}</td>
                        <td className="px-4 py-3 font-mono">{formatTime(record.check_in)}</td>
                        <td className="px-4 py-3 font-mono">{formatTime(record.check_out)}</td>
                        <td className="px-4 py-3">{getStatusBadge(record.status)}</td>
                        <td className="px-4 py-3">
                          {record.late_minutes > 0 ? (
                            <span className="text-yellow-600">{record.late_minutes} د</span>
                          ) : '-'}
                        </td>
                        <td className="px-4 py-3">
                          {record.overtime_hours > 0 ? (
                            <span className="text-green-600">{record.overtime_hours} س</span>
                          ) : '-'}
                        </td>
                        <td className="px-4 py-3 text-muted-foreground">
                          {record.leave_type || '-'}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default AttendancePage;
