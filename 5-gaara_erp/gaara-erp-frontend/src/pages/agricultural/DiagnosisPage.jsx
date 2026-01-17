/**
 * Plant Diagnosis Page - تشخيص الأمراض النباتية
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Stethoscope,
  Upload,
  Search,
  Camera,
  Leaf,
  Bug,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Image,
  FileText,
  Microscope,
  Sparkles,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const mockDiagnoses = [
  { id: 1, plant: "طماطم", disease: "اللفحة المتأخرة", confidence: 95, severity: "high", date: "2026-01-17", status: "confirmed", image: null },
  { id: 2, plant: "قمح", disease: "صدأ الساق", confidence: 88, severity: "medium", date: "2026-01-16", status: "confirmed", image: null },
  { id: 3, plant: "فلفل", disease: "فيروس تجعد الأوراق", confidence: 72, severity: "high", date: "2026-01-15", status: "pending", image: null },
  { id: 4, plant: "خيار", disease: "البياض الدقيقي", confidence: 91, severity: "low", date: "2026-01-14", status: "treated", image: null },
]

const severityConfig = {
  high: { label: "شديد", color: "destructive" },
  medium: { label: "متوسط", color: "secondary" },
  low: { label: "منخفض", color: "default" },
}

const statusConfig = {
  pending: { label: "قيد التحقق", icon: Clock },
  confirmed: { label: "مؤكد", icon: CheckCircle2 },
  treated: { label: "تم العلاج", icon: CheckCircle2 },
}

const DiagnosisPage = () => {
  const [diagnoses, setDiagnoses] = useState(mockDiagnoses)
  const [activeTab, setActiveTab] = useState("diagnose")
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleUpload = async () => {
    setIsAnalyzing(true)
    await new Promise(r => setTimeout(r, 2000))
    setIsAnalyzing(false)
    toast.success("تم تحليل الصورة بنجاح")
  }

  const stats = {
    total: diagnoses.length,
    confirmed: diagnoses.filter(d => d.status === "confirmed").length,
    treated: diagnoses.filter(d => d.status === "treated").length,
    highSeverity: diagnoses.filter(d => d.severity === "high").length,
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Stethoscope className="w-7 h-7 text-red-500" />
            تشخيص الأمراض النباتية
          </h1>
          <p className="text-slate-600 dark:text-slate-400">تحليل وتشخيص أمراض النباتات باستخدام الذكاء الاصطناعي</p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Microscope className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">تشخيص</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.treated}</p>
              <p className="text-sm text-muted-foreground">تم علاجها</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Bug className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.confirmed}</p>
              <p className="text-sm text-muted-foreground">مؤكد</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.highSeverity}</p>
              <p className="text-sm text-muted-foreground">شديد الخطورة</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="diagnose" className="gap-2">
            <Camera className="w-4 h-4" />
            تشخيص جديد
          </TabsTrigger>
          <TabsTrigger value="history" className="gap-2">
            <FileText className="w-4 h-4" />
            السجل
          </TabsTrigger>
        </TabsList>

        <TabsContent value="diagnose">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-500" />
                تشخيص بالذكاء الاصطناعي
              </CardTitle>
              <CardDescription>ارفع صورة النبات المصاب للحصول على تشخيص فوري</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="border-2 border-dashed rounded-lg p-12 text-center hover:border-primary transition-colors cursor-pointer">
                <div className="flex flex-col items-center gap-4">
                  <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
                    <Upload className="w-8 h-8 text-muted-foreground" />
                  </div>
                  <div>
                    <p className="font-medium">اسحب الصورة هنا أو اضغط للاختيار</p>
                    <p className="text-sm text-muted-foreground">PNG, JPG حتى 10MB</p>
                  </div>
                  <Button onClick={handleUpload} disabled={isAnalyzing}>
                    <Camera className="w-4 h-4 ml-2" />
                    {isAnalyzing ? "جاري التحليل..." : "اختيار صورة"}
                  </Button>
                </div>
              </div>

              {isAnalyzing && (
                <div className="p-6 bg-muted rounded-lg">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-10 h-10 rounded-full bg-purple-100 dark:bg-purple-900 flex items-center justify-center animate-pulse">
                      <Sparkles className="w-5 h-5 text-purple-500" />
                    </div>
                    <div>
                      <p className="font-medium">جاري تحليل الصورة...</p>
                      <p className="text-sm text-muted-foreground">يستخدم الذكاء الاصطناعي للكشف عن الأمراض</p>
                    </div>
                  </div>
                  <Progress value={60} className="h-2" />
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="history">
          <Card>
            <CardHeader>
              <CardTitle>سجل التشخيصات</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {diagnoses.map(diagnosis => {
                  const severityCfg = severityConfig[diagnosis.severity]
                  const statusCfg = statusConfig[diagnosis.status]
                  const StatusIcon = statusCfg.icon
                  return (
                    <div key={diagnosis.id} className="flex items-center gap-4 p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                      <div className="w-12 h-12 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
                        <Leaf className="w-6 h-6 text-green-600" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <p className="font-medium">{diagnosis.disease}</p>
                          <Badge variant={severityCfg.color}>{severityCfg.label}</Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">{diagnosis.plant} • {diagnosis.date}</p>
                      </div>
                      <div className="text-left">
                        <div className="flex items-center gap-1 text-sm">
                          <span className="text-muted-foreground">دقة:</span>
                          <span className="font-medium">{diagnosis.confidence}%</span>
                        </div>
                        <Badge variant="outline" className="mt-1">
                          <StatusIcon className="w-3 h-3 ml-1" />
                          {statusCfg.label}
                        </Badge>
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default DiagnosisPage
