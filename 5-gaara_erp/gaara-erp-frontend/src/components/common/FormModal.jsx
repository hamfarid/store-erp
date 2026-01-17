import { motion } from "framer-motion"
import { X, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

const FormModal = ({
  open,
  onOpenChange,
  title,
  description,
  children,
  onSubmit,
  submitText = "حفظ",
  cancelText = "إلغاء",
  isLoading = false,
  size = "default", // default, lg, xl, full
}) => {
  const sizeClasses = {
    default: "sm:max-w-md",
    lg: "sm:max-w-lg",
    xl: "sm:max-w-2xl",
    full: "sm:max-w-4xl",
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit?.(e)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className={sizeClasses[size]}>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>

        <form onSubmit={handleSubmit}>
          <div className="py-4 max-h-[60vh] overflow-y-auto">{children}</div>

          <DialogFooter className="gap-2 sm:gap-0">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={isLoading}
            >
              {cancelText}
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 ml-2 animate-spin" />
                  جاري الحفظ...
                </>
              ) : (
                submitText
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export default FormModal
