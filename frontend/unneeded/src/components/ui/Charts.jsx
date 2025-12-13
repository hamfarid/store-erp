import React from 'react'
import { TrendingUp, TrendingDown } from 'lucide-react'

// مكون الرسم البياني الأساسي
const ChartContainer = ({ title, children, className = "" }) => (
  <div className={`bg-white rounded-lg shadow-sm border border-border p-6 ${className}`}>
    {title && (
      <h3 className="text-lg font-semibold text-foreground mb-4">{title}</h3>
    )}
    {children}
  </div>
)

// رسم بياني خطي بسيط
const LineChart = ({ data, title, color = "blue" }) => {
  const maxValue = Math.max(...data.map(item => item.value))
  
  return (
    <ChartContainer title={title}>
      <div className="relative h-64">
        <div className="absolute inset-0 flex items-end justify-between">
          {data.map((item, index) => {
            const height = (item.value / maxValue) * 100
            return (
              <div key={index} className="flex flex-col items-center">
                <div className="text-xs text-muted-foreground mb-1">
                  {item.value.toLocaleString()}
                </div>
                <div 
                  className={`w-8 bg-${color}-500 rounded-t transition-all duration-500 hover:bg-${color}-600`}
                  style={{ height: `${height}%` }}
                />
                <div className="text-xs text-gray-500 mt-2 transform -rotate-45 origin-left">
                  {item.label}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </ChartContainer>
  )
}

// رسم بياني دائري بسيط
const PieChartComponent = ({ data, title }) => {
  const total = data.reduce((sum, item) => sum + item.value, 0)
  let currentAngle = 0
  
  const colors = [
    'bg-primary-500', 'bg-primary/100', 'bg-accent/100', 
    'bg-destructive/100', 'bg-purple-500', 'bg-secondary/100'
  ]
  
  return (
    <ChartContainer title={title}>
      <div className="flex items-center justify-center">
        <div className="relative w-48 h-48">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            {data.map((item, index) => {
              const percentage = (item.value / total) * 100
              const strokeDasharray = `${percentage} ${100 - percentage}`
              const strokeDashoffset = -currentAngle
              currentAngle += percentage
              
              return (
                <circle
                  key={index}
                  cx="50"
                  cy="50"
                  r="40"
                  fill="transparent"
                  stroke={`hsl(${index * 60}, 70%, 50%)`}
                  strokeWidth="8"
                  strokeDasharray={strokeDasharray}
                  strokeDashoffset={strokeDashoffset}
                  className="transition-all duration-500"
                />
              )
            })}
          </svg>
        </div>
        
        <div className="mr-6 space-y-2">
          {data.map((item, index) => (
            <div key={index} className="flex items-center">
              <div 
                className={`w-4 h-4 rounded-full mr-2`}
                style={{ backgroundColor: `hsl(${index * 60}, 70%, 50%)` }}
              />
              <span className="text-sm text-foreground">
                {item.label}: {item.value.toLocaleString()} ({((item.value / total) * 100).toFixed(1)}%)
              </span>
            </div>
          ))}
        </div>
      </div>
    </ChartContainer>
  )
}

// مكون إحصائيات سريعة
const StatCard = ({ title, value, change, icon: Icon, color = "blue" }) => {
  const isPositive = change >= 0
  const ChangeIcon = isPositive ? TrendingUp : TrendingDown
  
  return (
    <div className={`bg-gradient-to-r from-${color}-500 to-${color}-600 rounded-lg p-6 text-white`}>
      <div className="flex items-center justify-between">
        <div>
          <p className={`text-${color}-100 text-sm`}>{title}</p>
          <p className="text-2xl font-bold">{value}</p>
          {change !== undefined && (
            <div className="flex items-center mt-2">
              <ChangeIcon className="w-4 h-4 ml-1" />
              <span className="text-sm">
                {isPositive ? '+' : ''}{change}%
              </span>
            </div>
          )}
        </div>
        {Icon && <Icon className={`w-8 h-8 text-${color}-200`} />}
      </div>
    </div>
  )
}

// رسم بياني شريطي أفقي
const HorizontalBarChart = ({ data, title, color = "blue" }) => {
  const maxValue = Math.max(...data.map(item => item.value))
  
  return (
    <ChartContainer title={title}>
      <div className="space-y-4">
        {data.map((item, index) => {
          const width = (item.value / maxValue) * 100
          return (
            <div key={index} className="flex items-center">
              <div className="w-24 text-sm text-muted-foreground text-right ml-4">
                {item.label}
              </div>
              <div className="flex-1 bg-muted rounded-full h-6 relative">
                <div 
                  className={`bg-${color}-500 h-full rounded-full transition-all duration-500 flex items-center justify-end px-2`}
                  style={{ width: `${width}%` }}
                >
                  <span className="text-white text-xs font-medium">
                    {item.value.toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </ChartContainer>
  )
}

// مكون مقارنة الأرقام
const ComparisonChart = ({ data, title }) => {
  return (
    <ChartContainer title={title}>
      <div className="grid grid-cols-2 gap-6">
        {data.map((item, index) => (
          <div key={index} className="text-center">
            <div className={`text-3xl font-bold ${
              index === 0 ? 'text-primary-600' : 'text-primary'
            }`}>
              {item.value.toLocaleString()}
            </div>
            <div className="text-sm text-muted-foreground mt-1">{item.label}</div>
            {item.change && (
              <div className={`text-xs mt-1 ${
                item.change >= 0 ? 'text-primary' : 'text-destructive'
              }`}>
                {item.change >= 0 ? '+' : ''}{item.change}% من الشهر الماضي
              </div>
            )}
          </div>
        ))}
      </div>
    </ChartContainer>
  )
}

// مكون الاتجاهات
const TrendChart = ({ data, title, color = "blue" }) => {
  return (
    <ChartContainer title={title}>
      <div className="relative h-32">
        <svg className="w-full h-full" viewBox="0 0 400 100">
          <defs>
            <linearGradient id={`gradient-${color}`} x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor={`hsl(var(--${color}-500))`} stopOpacity="0.3" />
              <stop offset="100%" stopColor={`hsl(var(--${color}-500))`} stopOpacity="0" />
            </linearGradient>
          </defs>
          
          {/* خط الاتجاه */}
          <polyline
            fill="none"
            stroke={`hsl(var(--${color}-500))`}
            strokeWidth="2"
            points={data.map((item, index) => 
              `${(index / (data.length - 1)) * 380 + 10},${90 - (item.value / Math.max(...data.map(d => d.value))) * 70}`
            ).join(' ')}
          />
          
          {/* منطقة مملوءة */}
          <polygon
            fill={`url(#gradient-${color})`}
            points={`10,90 ${data.map((item, index) => 
              `${(index / (data.length - 1)) * 380 + 10},${90 - (item.value / Math.max(...data.map(d => d.value))) * 70}`
            ).join(' ')} 390,90`}
          />
          
          {/* نقاط البيانات */}
          {data.map((item, index) => (
            <circle
              key={index}
              cx={(index / (data.length - 1)) * 380 + 10}
              cy={90 - (item.value / Math.max(...data.map(d => d.value))) * 70}
              r="3"
              fill={`hsl(var(--${color}-500))`}
              className="hover:r-5 transition-all"
            />
          ))}
        </svg>
        
        {/* تسميات المحاور */}
        <div className="flex justify-between mt-2 text-xs text-gray-500">
          {data.map((item, index) => (
            <span key={index}>{item.label}</span>
          ))}
        </div>
      </div>
    </ChartContainer>
  )
}

// مكون مؤشر دائري
const CircularProgress = ({ percentage, title, color = "blue" }) => {
  const radius = 45
  const circumference = 2 * Math.PI * radius
  const strokeDasharray = circumference
  const strokeDashoffset = circumference - (percentage / 100) * circumference
  
  return (
    <div className="flex flex-col items-center">
      <div className="relative w-32 h-32">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          {/* الدائرة الخلفية */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="transparent"
            stroke="currentColor"
            strokeWidth="8"
            className="text-gray-200"
          />
          
          {/* دائرة التقدم */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="transparent"
            stroke={`hsl(var(--${color}-500))`}
            strokeWidth="8"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-500"
          />
        </svg>
        
        {/* النسبة المئوية */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-xl font-bold text-foreground">{percentage}%</span>
        </div>
      </div>
      
      {title && (
        <h4 className="mt-2 text-sm font-medium text-foreground text-center">{title}</h4>
      )}
    </div>
  )
}

export {
  ChartContainer,
  LineChart,
  PieChartComponent as PieChart,
  StatCard,
  HorizontalBarChart,
  ComparisonChart,
  TrendChart,
  CircularProgress
}

