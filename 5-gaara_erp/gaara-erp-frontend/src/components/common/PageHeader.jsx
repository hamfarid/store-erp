import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

/**
 * PageHeader Component
 * A reusable page header with title, description, and actions
 */
export function PageHeader({
  title,
  description,
  icon: Icon,
  actions,
  className,
  children,
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn("flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6", className)}
    >
      <div className="flex items-center gap-3">
        {Icon && (
          <div className="p-2 rounded-lg bg-primary/10">
            <Icon className="w-6 h-6 text-primary" />
          </div>
        )}
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white">{title}</h1>
          {description && (
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">{description}</p>
          )}
        </div>
      </div>

      {actions && (
        <div className="flex items-center gap-2 flex-wrap">
          {Array.isArray(actions) ? (
            actions.map((action, index) => (
              <Button
                key={index}
                variant={action.variant || "default"}
                size={action.size || "default"}
                onClick={action.onClick}
                disabled={action.disabled}
                className={action.className}
              >
                {action.icon && <action.icon className="w-4 h-4 ml-2" />}
                {action.label}
              </Button>
            ))
          ) : (
            actions
          )}
        </div>
      )}

      {children}
    </motion.div>
  )
}
