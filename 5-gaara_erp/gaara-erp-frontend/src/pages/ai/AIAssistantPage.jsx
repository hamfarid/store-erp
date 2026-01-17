/**
 * AI Assistant Page - المساعد الذكي
 * Gaara ERP v12
 */

import { useState, useRef, useEffect } from "react"
import { toast } from "sonner"
import {
  Bot,
  Send,
  Sparkles,
  User,
  RefreshCw,
  Copy,
  ThumbsUp,
  ThumbsDown,
  Trash2,
  MessageSquare,
  Zap,
  Clock,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

const AIAssistantPage = () => {
  const [messages, setMessages] = useState([
    { id: 1, role: "assistant", content: "مرحباً! أنا مساعدك الذكي في نظام Gaara ERP. كيف يمكنني مساعدتك اليوم؟", timestamp: new Date() }
  ])
  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const scrollRef = useRef(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const suggestions = [
    "ما هو رصيد المخزون الحالي؟",
    "أظهر تقرير المبيعات لهذا الشهر",
    "كيف أضيف منتج جديد؟",
    "ما هي المهام المعلقة؟",
  ]

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage = { id: Date.now(), role: "user", content: input, timestamp: new Date() }
    setMessages(prev => [...prev, userMessage])
    setInput("")
    setIsTyping(true)

    // Simulate AI response
    await new Promise(r => setTimeout(r, 1500))
    
    const aiMessage = {
      id: Date.now() + 1,
      role: "assistant",
      content: `شكراً لسؤالك عن "${input}". يمكنني مساعدتك في ذلك. هل تريد المزيد من التفاصيل؟`,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, aiMessage])
    setIsTyping(false)
  }

  const handleCopy = (content) => {
    navigator.clipboard.writeText(content)
    toast.success("تم النسخ")
  }

  const stats = {
    conversations: 156,
    responses: 1250,
    avgTime: "2.3s",
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Bot className="w-7 h-7 text-purple-500" />
            المساعد الذكي
          </h1>
          <p className="text-slate-600 dark:text-slate-400">تفاعل مع مساعد الذكاء الاصطناعي</p>
        </div>
        <Button variant="outline" onClick={() => setMessages([messages[0]])}>
          <Trash2 className="w-4 h-4 ml-2" />
          محادثة جديدة
        </Button>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.conversations}</p>
              <p className="text-sm text-muted-foreground">محادثة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Zap className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.responses}</p>
              <p className="text-sm text-muted-foreground">رد</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Clock className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.avgTime}</p>
              <p className="text-sm text-muted-foreground">متوسط الرد</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="h-[600px] flex flex-col">
        <CardHeader className="border-b">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <CardTitle className="text-lg">Gaara AI</CardTitle>
              <p className="text-sm text-muted-foreground">مساعد ذكي • متصل</p>
            </div>
            <Badge className="mr-auto">GPT-4</Badge>
          </div>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col p-0">
          <ScrollArea className="flex-1 p-4" ref={scrollRef}>
            <div className="space-y-4">
              {messages.map(message => (
                <div key={message.id} className={`flex gap-3 ${message.role === "user" ? "flex-row-reverse" : ""}`}>
                  <Avatar className={message.role === "user" ? "bg-blue-500" : "bg-purple-500"}>
                    <AvatarFallback>
                      {message.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                    </AvatarFallback>
                  </Avatar>
                  <div className={`max-w-[70%] ${message.role === "user" ? "text-left" : ""}`}>
                    <div className={`p-3 rounded-lg ${
                      message.role === "user" 
                        ? "bg-blue-500 text-white" 
                        : "bg-muted"
                    }`}>
                      {message.content}
                    </div>
                    <div className={`flex items-center gap-2 mt-1 ${message.role === "user" ? "justify-start" : ""}`}>
                      <span className="text-xs text-muted-foreground">
                        {message.timestamp.toLocaleTimeString("ar-SA", { hour: "2-digit", minute: "2-digit" })}
                      </span>
                      {message.role === "assistant" && (
                        <div className="flex gap-1">
                          <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={() => handleCopy(message.content)}>
                            <Copy className="w-3 h-3" />
                          </Button>
                          <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                            <ThumbsUp className="w-3 h-3" />
                          </Button>
                          <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                            <ThumbsDown className="w-3 h-3" />
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex gap-3">
                  <Avatar className="bg-purple-500">
                    <AvatarFallback><Bot className="w-4 h-4" /></AvatarFallback>
                  </Avatar>
                  <div className="p-3 bg-muted rounded-lg">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          <div className="p-4 border-t">
            <div className="flex gap-2 mb-3 flex-wrap">
              {suggestions.map((suggestion, i) => (
                <Button key={i} variant="outline" size="sm" onClick={() => setInput(suggestion)} className="text-xs">
                  {suggestion}
                </Button>
              ))}
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="اكتب رسالتك..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSend()}
                className="flex-1"
              />
              <Button onClick={handleSend} disabled={isTyping || !input.trim()}>
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default AIAssistantPage
