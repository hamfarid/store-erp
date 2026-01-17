import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

/**
 * PageContainer Component
 * A consistent container wrapper for pages
 */
export function PageContainer({ children, className, maxWidth = "7xl" }) {
  const maxWidthClasses = {
    sm: "max-w-3xl",
    md: "max-w-5xl",
    lg: "max-w-6xl",
    xl: "max-w-7xl",
    "2xl": "max-w-screen-2xl",
    full: "max-w-full",
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn("mx-auto px-4 md:px-6", maxWidthClasses[maxWidth], className)}
    >
      {children}
    </motion.div>
  )
}
