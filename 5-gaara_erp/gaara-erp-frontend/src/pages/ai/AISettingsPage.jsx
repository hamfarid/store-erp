/**
 * AI Settings Page - إعدادات الذكاء الاصطناعي
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Settings,
  Brain,
  Cpu,
  Zap,
  Key,
  Eye,
  EyeOff,
  CheckCircle2,
  AlertTriangle,
  Gauge,
  Database,
  Globe,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const AISettingsPage = () => {
  const [showApiKey, setShowApiKey] = useState(false)
  const [settings, setSettings] = useState({
    provider: "openai",
    model: "gpt-4",
    apiKey: "sk-xxxxxxxxxxxxxxxxxxxx",
    maxTokens: 4096,
    temperature: 0.7,
    enabled: true,
    autoFallback: true,
    cacheEnabled: true,
    cacheTTL: 3600,
    rateLimit: 100,
    quotaLimit: 10000,
    quotaUsed: 5420,
  })

  const models = [
    { id: "gpt-4", name: "GPT-4", provider: "openai" },
    { id: "gpt-3.5-turbo", name: "GPT-3.5 Turbo", provider: "openai" },
    { id: "claude-3", name: "Claude 3", provider: "anthropic" },
    { id: "gemini-pro", name: "Gemini Pro", provider: "google" },
  ]

  const handleSave = () => {
    toast.success("تم حفظ الإعدادات بنجاح")
  }

  const handleTestConnection = async () => {
    toast.loading("جاري اختبار الاتصال...")
    await new Promise(r => setTimeout(r, 1500))
    toast.success("الاتصال يعمل بشكل صحيح")
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Settings className="w-7 h-7 text-gray-500" />
            إعدادات الذكاء الاصطناعي
          </h1>
          <p className="text-slate-600 dark:text-slate-400">تكوين وإدارة خدمات الذكاء الاصطناعي</p>
        </div>
        <Button onClick={handleSave}>
          <CheckCircle2 className="w-4 h-4 ml-2" />
          حفظ الإعدادات
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Brain className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">الحالة</p>
              <Badge variant={settings.enabled ? "default" : "secondary"}>
                {settings.enabled ? "مفعل" : "معطل"}
              </Badge>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Cpu className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">النموذج</p>
              <p className="font-medium">{settings.model}</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Gauge className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">الاستخدام</p>
              <p className="font-medium">{Math.round((settings.quotaUsed / settings.quotaLimit) * 100)}%</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900 flex items-center justify-center">
              <Zap className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">الطلبات/دقيقة</p>
              <p className="font-medium">{settings.rateLimit}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="general">
        <TabsList>
          <TabsTrigger value="general">عام</TabsTrigger>
          <TabsTrigger value="models">النماذج</TabsTrigger>
          <TabsTrigger value="quota">الحصص</TabsTrigger>
          <TabsTrigger value="cache">التخزين المؤقت</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>الإعدادات الأساسية</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <Label>تفعيل الذكاء الاصطناعي</Label>
                  <p className="text-sm text-muted-foreground">تمكين ميزات الذكاء الاصطناعي في النظام</p>
                </div>
                <Switch checked={settings.enabled} onCheckedChange={(v) => setSettings({ ...settings, enabled: v })} />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <Label>التراجع التلقائي</Label>
                  <p className="text-sm text-muted-foreground">التحول لنموذج بديل عند الفشل</p>
                </div>
                <Switch checked={settings.autoFallback} onCheckedChange={(v) => setSettings({ ...settings, autoFallback: v })} />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>مفتاح API</CardTitle>
              <CardDescription>مفتاح الوصول للخدمة</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label>مزود الخدمة</Label>
                <Select value={settings.provider} onValueChange={(v) => setSettings({ ...settings, provider: v })}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="openai">OpenAI</SelectItem>
                    <SelectItem value="anthropic">Anthropic</SelectItem>
                    <SelectItem value="google">Google</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>مفتاح API</Label>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      type={showApiKey ? "text" : "password"}
                      value={settings.apiKey}
                      onChange={(e) => setSettings({ ...settings, apiKey: e.target.value })}
                      dir="ltr"
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      className="absolute left-1 top-1/2 -translate-y-1/2"
                      onClick={() => setShowApiKey(!showApiKey)}
                    >
                      {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </Button>
                  </div>
                  <Button variant="outline" onClick={handleTestConnection}>اختبار</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="models">
          <Card>
            <CardHeader>
              <CardTitle>إعدادات النموذج</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <Label>النموذج</Label>
                <Select value={settings.model} onValueChange={(v) => setSettings({ ...settings, model: v })}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {models.map(m => (
                      <SelectItem key={m.id} value={m.id}>{m.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>الحد الأقصى للتوكنات</Label>
                <Slider
                  value={[settings.maxTokens]}
                  onValueChange={([v]) => setSettings({ ...settings, maxTokens: v })}
                  max={8192}
                  min={256}
                  step={256}
                />
                <p className="text-sm text-muted-foreground mt-1">{settings.maxTokens} توكن</p>
              </div>
              <div>
                <Label>درجة الحرارة (Temperature)</Label>
                <Slider
                  value={[settings.temperature * 100]}
                  onValueChange={([v]) => setSettings({ ...settings, temperature: v / 100 })}
                  max={100}
                  min={0}
                  step={5}
                />
                <p className="text-sm text-muted-foreground mt-1">{settings.temperature}</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="quota">
          <Card>
            <CardHeader>
              <CardTitle>الحصص والحدود</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <div className="flex justify-between mb-2">
                  <Label>الحصة الشهرية</Label>
                  <span>{settings.quotaUsed.toLocaleString()} / {settings.quotaLimit.toLocaleString()}</span>
                </div>
                <Progress value={(settings.quotaUsed / settings.quotaLimit) * 100} />
              </div>
              <div>
                <Label>حد الطلبات بالدقيقة</Label>
                <Input type="number" value={settings.rateLimit} onChange={(e) => setSettings({ ...settings, rateLimit: parseInt(e.target.value) })} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="cache">
          <Card>
            <CardHeader>
              <CardTitle>التخزين المؤقت</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label>تفعيل التخزين المؤقت</Label>
                  <p className="text-sm text-muted-foreground">تخزين الردود لتسريع الاستجابة</p>
                </div>
                <Switch checked={settings.cacheEnabled} onCheckedChange={(v) => setSettings({ ...settings, cacheEnabled: v })} />
              </div>
              <div>
                <Label>مدة صلاحية الكاش (ثانية)</Label>
                <Input type="number" value={settings.cacheTTL} onChange={(e) => setSettings({ ...settings, cacheTTL: parseInt(e.target.value) })} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AISettingsPage
