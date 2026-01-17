import { motion } from "framer-motion"
import { ArrowUpRight, ArrowDownRight } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { cn, formatNumber, formatCurrency, formatPercent } from "@/lib/utils"

const StatsCard = ({
  title,
  value,
  change,
  changeLabel = "من الشهر الماضي",
  icon: Icon,
  color = "primary",
  format = "number", // number, currency, percent
  delay = 0,
}) => {
  const isPositive = change >= 0

  const colorClasses = {
    primary: "bg-primary/10 text-primary",
    emerald: "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400",
    blue: "bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400",
    purple: "bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400",
    orange: "bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400",
    red: "bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400",
    amber: "bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400",
    cyan: "bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400",
  }

  const formatValue = (val) => {
    switch (format) {
      case "currency":
        return formatCurrency(val)
      case "percent":
        return formatPercent(val)
      default:
        return formatNumber(val)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
    >
      <Card className="hover:shadow-lg transition-shadow duration-300">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">{title}</p>
              <p className="text-2xl font-bold">{formatValue(value)}</p>
              {change !== undefined && (
                <div
                  className={cn(
                    "flex items-center gap-1 text-sm",
                    isPositive ? "text-emerald-600" : "text-red-600"
                  )}
                >
                  {isPositive ? (
                    <ArrowUpRight className="w-4 h-4" />
                  ) : (
                    <ArrowDownRight className="w-4 h-4" />
                  )}
                  <span>{formatPercent(Math.abs(change))}</span>
                  <span className="text-muted-foreground">{changeLabel}</span>
                </div>
              )}
            </div>
            {Icon && (
              <div className={cn("p-3 rounded-xl", colorClasses[color])}>
                <Icon className="w-6 h-6" />
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default StatsCard
