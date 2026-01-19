/**
 * AI Assistant Page - المساعد الذكي
 * Gaara ERP v12
 *
 * AI-powered assistant for help, queries, and automation.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useRef, useEffect } from "react"
import { toast } from "sonner"
import {
  Bot,
  Send,
  Mic,
  MicOff,
  Paperclip,
  Image,
  FileText,
  Settings,
  RefreshCw,
  Sparkles,
  MessageSquare,
  History,
  Lightbulb,
  HelpCircle,
  ChevronRight,
  Copy,
  ThumbsUp,
  ThumbsDown,
  MoreVertical,
  Trash2,
  Download,
  Volume2,
  Loader2,
  Zap,
  Brain,
  Search,
  BarChart3,
  Calendar,
  Users,
  FileSpreadsheet,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Textarea } from "@/components/ui/textarea"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Suggested prompts
const suggestedPrompts = [
  { icon: BarChart3, text: "أظهر لي تقرير المبيعات لهذا الشهر", category: "reports" },
  { icon: Users, text: "كم عدد العملاء النشطين؟", category: "analytics" },
  { icon: Calendar, text: "ما هي المهام المستحقة اليوم؟", category: "tasks" },
  { icon: FileSpreadsheet, text: "أنشئ فاتورة جديدة للعميل أحمد", category: "actions" },
  { icon: Search, text: "ابحث عن المنتجات التي نفدت من المخزون", category: "search" },
  { icon: Lightbulb, text: "اقترح طرق لتحسين المبيعات", category: "insights" },
]

// Mock chat history
const mockChatHistory = [
  {
    id: 1,
    role: "assistant",
    content: "مرحباً! أنا المساعد الذكي لنظام Gaara ERP. كيف يمكنني مساعدتك اليوم؟",
    timestamp: "14:30",
  },
]

// Quick actions
const quickActions = [
  { icon: BarChart3, label: "تقرير المبيعات", action: "sales_report" },
  { icon: FileSpreadsheet, label: "فاتورة جديدة", action: "new_invoice" },
  { icon: Users, label: "إضافة عميل", action: "add_customer" },
  { icon: Calendar, label: "جدولة موعد", action: "schedule" },
]

const AIAssistantPage = () => {
  // State
  const [messages, setMessages] = useState(mockChatHistory)
  const [inputValue, setInputValue] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [activeTab, setActiveTab] = useState("chat")
  const [chatHistory, setChatHistory] = useState([
    { id: 1, title: "محادثة المبيعات", date: "اليوم", preview: "تقرير المبيعات الشهري..." },
    { id: 2, title: "استفسار عن المخزون", date: "أمس", preview: "المنتجات منخفضة المخزون..." },
    { id: 3, title: "مساعدة في الفواتير", date: "أمس", preview: "كيفية إنشاء فاتورة..." },
  ])

  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Handlers
  const handleSend = async () => {
    if (!inputValue.trim()) return

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: inputValue,
      timestamp: new Date().toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' }),
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue("")
    setIsTyping(true)

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        "بناءً على تحليل البيانات، إليك النتائج المطلوبة...",
        "تم العثور على المعلومات التي طلبتها. هل تريد مزيداً من التفاصيل؟",
        "أفهم استفسارك. دعني أساعدك في ذلك...",
        "تم تنفيذ الإجراء المطلوب بنجاح.",
      ]

      const aiMessage = {
        id: Date.now(),
        role: "assistant",
        content: responses[Math.floor(Math.random() * responses.length)],
        timestamp: new Date().toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' }),
        data: inputValue.includes("تقرير") ? {
          type: "chart",
          title: "ملخص المبيعات",
          values: [
            { label: "يناير", value: 45000 },
            { label: "فبراير", value: 52000 },
            { label: "مارس", value: 48000 },
          ]
        } : null
      }

      setMessages(prev => [...prev, aiMessage])
      setIsTyping(false)
    }, 1500)
  }

  const handlePromptClick = (prompt) => {
    setInputValue(prompt.text)
    inputRef.current?.focus()
  }

  const handleQuickAction = (action) => {
    toast.info(`جاري تنفيذ: ${action}`)
  }

  const handleCopyMessage = (content) => {
    navigator.clipboard.writeText(content)
    toast.success("تم نسخ الرسالة")
  }

  const toggleListening = () => {
    if (isListening) {
      setIsListening(false)
      toast.info("تم إيقاف التسجيل الصوتي")
    } else {
      setIsListening(true)
      toast.info("جاري الاستماع...")
      // Simulate voice input
      setTimeout(() => {
        setInputValue("أظهر لي ملخص المبيعات اليوم")
        setIsListening(false)
      }, 2000)
    }
  }

  const startNewChat = () => {
    setMessages([mockChatHistory[0]])
    toast.success("تم بدء محادثة جديدة")
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Bot className="w-7 h-7 text-violet-500" />
            المساعد الذكي
          </h1>
          <p className="text-slate-600 dark:text-slate-400">مساعدك الشخصي المدعوم بالذكاء الاصطناعي</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={startNewChat}>
            <RefreshCw className="w-4 h-4 ml-2" />محادثة جديدة
          </Button>
          <Button variant="outline" onClick={() => toast.info("جاري فتح الإعدادات...")}>
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 grid lg:grid-cols-4 gap-4 overflow-hidden">
        {/* Sidebar */}
        <div className="hidden lg:flex flex-col space-y-4">
          {/* Quick Actions */}
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm flex items-center gap-2">
                <Zap className="w-4 h-4" />إجراءات سريعة
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-2">
                {quickActions.map((action, idx) => (
                  <Button 
                    key={idx}
                    variant="outline" 
                    className="h-auto py-2 flex-col gap-1"
                    onClick={() => handleQuickAction(action.action)}
                  >
                    <action.icon className="w-4 h-4" />
                    <span className="text-xs">{action.label}</span>
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Chat History */}
          <Card className="flex-1">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm flex items-center gap-2">
                <History className="w-4 h-4" />المحادثات السابقة
              </CardTitle>
            </CardHeader>
            <CardContent className="p-2">
              <ScrollArea className="h-[300px]">
                <div className="space-y-2">
                  {chatHistory.map((chat) => (
                    <div 
                      key={chat.id}
                      className="p-2 rounded-lg hover:bg-muted cursor-pointer"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-sm">{chat.title}</span>
                        <span className="text-xs text-muted-foreground">{chat.date}</span>
                      </div>
                      <p className="text-xs text-muted-foreground truncate">{chat.preview}</p>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        {/* Chat Area */}
        <Card className="lg:col-span-3 flex flex-col overflow-hidden">
          <CardContent className="flex-1 flex flex-col p-0 overflow-hidden">
            {/* Messages */}
            <ScrollArea className="flex-1 p-4">
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 ${message.role === "user" ? "flex-row-reverse" : ""}`}
                  >
                    <Avatar className={`w-8 h-8 ${message.role === "user" ? "bg-primary" : "bg-violet-100"}`}>
                      <AvatarFallback className={message.role === "user" ? "text-primary-foreground" : "text-violet-600"}>
                        {message.role === "user" ? "أنت" : <Bot className="w-4 h-4" />}
                      </AvatarFallback>
                    </Avatar>
                    <div className={`flex-1 max-w-[80%] ${message.role === "user" ? "text-right" : ""}`}>
                      <div 
                        className={`inline-block p-3 rounded-lg ${
                          message.role === "user" 
                            ? "bg-primary text-primary-foreground" 
                            : "bg-muted"
                        }`}
                      >
                        <p className="text-sm">{message.content}</p>
                        
                        {/* Data visualization */}
                        {message.data && message.data.type === "chart" && (
                          <div className="mt-3 p-3 bg-white dark:bg-slate-800 rounded-lg">
                            <p className="text-xs font-medium mb-2 text-slate-700 dark:text-slate-300">{message.data.title}</p>
                            <div className="space-y-2">
                              {message.data.values.map((item, idx) => (
                                <div key={idx} className="flex items-center gap-2">
                                  <span className="text-xs w-16 text-slate-600 dark:text-slate-400">{item.label}</span>
                                  <div className="flex-1 bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                                    <div 
                                      className="bg-violet-500 h-2 rounded-full" 
                                      style={{ width: `${(item.value / 60000) * 100}%` }}
                                    />
                                  </div>
                                  <span className="text-xs text-slate-600 dark:text-slate-400">{item.value.toLocaleString()}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                      <div className={`flex items-center gap-2 mt-1 ${message.role === "user" ? "justify-end" : ""}`}>
                        <span className="text-xs text-muted-foreground">{message.timestamp}</span>
                        {message.role === "assistant" && (
                          <div className="flex gap-1">
                            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => handleCopyMessage(message.content)}>
                              <Copy className="w-3 h-3" />
                            </Button>
                            <Button variant="ghost" size="icon" className="h-6 w-6">
                              <ThumbsUp className="w-3 h-3" />
                            </Button>
                            <Button variant="ghost" size="icon" className="h-6 w-6">
                              <ThumbsDown className="w-3 h-3" />
                            </Button>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}

                {/* Typing indicator */}
                {isTyping && (
                  <div className="flex gap-3">
                    <Avatar className="w-8 h-8 bg-violet-100">
                      <AvatarFallback className="text-violet-600">
                        <Bot className="w-4 h-4" />
                      </AvatarFallback>
                    </Avatar>
                    <div className="bg-muted p-3 rounded-lg">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            </ScrollArea>

            {/* Suggested Prompts */}
            {messages.length <= 1 && (
              <div className="p-4 border-t">
                <p className="text-sm text-muted-foreground mb-3 flex items-center gap-2">
                  <Sparkles className="w-4 h-4" />
                  جرب هذه الاقتراحات:
                </p>
                <div className="flex flex-wrap gap-2">
                  {suggestedPrompts.map((prompt, idx) => (
                    <Button
                      key={idx}
                      variant="outline"
                      size="sm"
                      className="flex items-center gap-2"
                      onClick={() => handlePromptClick(prompt)}
                    >
                      <prompt.icon className="w-4 h-4" />
                      {prompt.text}
                    </Button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Area */}
            <div className="p-4 border-t">
              <div className="flex gap-2">
                <div className="flex-1 relative">
                  <Textarea
                    ref={inputRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault()
                        handleSend()
                      }
                    }}
                    placeholder="اكتب رسالتك هنا..."
                    className="resize-none pr-12"
                    rows={1}
                  />
                  <div className="absolute left-2 top-1/2 -translate-y-1/2 flex gap-1">
                    <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => toast.info("جاري رفع الملف...")}>
                      <Paperclip className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
                <Button 
                  variant={isListening ? "destructive" : "outline"}
                  size="icon"
                  onClick={toggleListening}
                >
                  {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                </Button>
                <Button onClick={handleSend} disabled={!inputValue.trim() || isTyping}>
                  {isTyping ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Send className="w-4 h-4" />
                  )}
                </Button>
              </div>
              <p className="text-xs text-muted-foreground mt-2 text-center">
                المساعد الذكي قد يخطئ أحياناً. يرجى التحقق من المعلومات المهمة.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default AIAssistantPage
