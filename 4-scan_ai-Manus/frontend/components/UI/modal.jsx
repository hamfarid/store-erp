/**
 * Enhanced Modal/Dialog Component with Radix + shadcn/ui
 * @file components/UI/modal.jsx
 */

import * as React from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import { cn } from "../../lib/utils";
import { Button } from "./button";

const Dialog = DialogPrimitive.Root;
const DialogTrigger = DialogPrimitive.Trigger;
const DialogPortal = DialogPrimitive.Portal;
const DialogClose = DialogPrimitive.Close;

const DialogOverlay = React.forwardRef(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/50 backdrop-blur-sm",
      "data-[state=open]:animate-in data-[state=closed]:animate-out",
      "data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
  />
));
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

const DialogContent = React.forwardRef(({ className, children, showClose = true, size = "default", ...props }, ref) => {
  const sizes = {
    sm: "max-w-md",
    default: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl",
    full: "max-w-[90vw]",
  };

  return (
    <DialogPortal>
      <DialogOverlay />
      <DialogPrimitive.Content
        ref={ref}
        className={cn(
          "fixed left-[50%] top-[50%] z-50 w-full translate-x-[-50%] translate-y-[-50%]",
          "bg-white dark:bg-gray-900 rounded-2xl shadow-2xl",
          "border border-gray-200 dark:border-gray-700",
          "data-[state=open]:animate-in data-[state=closed]:animate-out",
          "data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
          "data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95",
          "data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%]",
          "data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]",
          "duration-200",
          sizes[size],
          className
        )}
        {...props}
      >
        {children}
        {showClose && (
          <DialogPrimitive.Close className="absolute left-4 top-4 rounded-lg p-2 opacity-70 ring-offset-white transition-opacity hover:opacity-100 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:pointer-events-none">
            <X className="h-5 w-5" />
            <span className="sr-only">إغلاق</span>
          </DialogPrimitive.Close>
        )}
      </DialogPrimitive.Content>
    </DialogPortal>
  );
});
DialogContent.displayName = DialogPrimitive.Content.displayName;

const DialogHeader = ({ className, ...props }) => (
  <div
    className={cn(
      "flex flex-col space-y-2 p-6 pb-4 border-b border-gray-100 dark:border-gray-800",
      className
    )}
    {...props}
  />
);
DialogHeader.displayName = "DialogHeader";

const DialogFooter = ({ className, ...props }) => (
  <div
    className={cn(
      "flex flex-col-reverse sm:flex-row sm:justify-start gap-2 p-6 pt-4 border-t border-gray-100 dark:border-gray-800",
      className
    )}
    {...props}
  />
);
DialogFooter.displayName = "DialogFooter";

const DialogTitle = React.forwardRef(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn(
      "text-xl font-semibold text-gray-900 dark:text-gray-100",
      className
    )}
    {...props}
  />
));
DialogTitle.displayName = DialogPrimitive.Title.displayName;

const DialogDescription = React.forwardRef(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-gray-500 dark:text-gray-400", className)}
    {...props}
  />
));
DialogDescription.displayName = DialogPrimitive.Description.displayName;

const DialogBody = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("p-6 overflow-y-auto max-h-[60vh]", className)}
    {...props}
  />
));
DialogBody.displayName = "DialogBody";

// Confirmation Dialog Component
const ConfirmDialog = ({
  open,
  onOpenChange,
  title = "تأكيد",
  description = "هل أنت متأكد من هذا الإجراء؟",
  confirmText = "تأكيد",
  cancelText = "إلغاء",
  onConfirm,
  onCancel,
  variant = "destructive",
  loading = false,
}) => (
  <Dialog open={open} onOpenChange={onOpenChange}>
    <DialogContent size="sm" showClose={false}>
      <DialogHeader>
        <DialogTitle>{title}</DialogTitle>
        <DialogDescription>{description}</DialogDescription>
      </DialogHeader>
      <DialogFooter>
        <Button
          variant="secondary"
          onClick={() => {
            onCancel?.();
            onOpenChange?.(false);
          }}
          disabled={loading}
        >
          {cancelText}
        </Button>
        <Button
          variant={variant}
          onClick={async () => {
            await onConfirm?.();
            onOpenChange?.(false);
          }}
          loading={loading}
        >
          {confirmText}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
);

// Form Dialog Component
const FormDialog = ({
  open,
  onOpenChange,
  title,
  description,
  children,
  onSubmit,
  submitText = "حفظ",
  cancelText = "إلغاء",
  loading = false,
  size = "default",
}) => {
  const handleSubmit = async (e) => {
    e.preventDefault();
    await onSubmit?.(e);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent size={size}>
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            {description && <DialogDescription>{description}</DialogDescription>}
          </DialogHeader>
          <DialogBody>{children}</DialogBody>
          <DialogFooter>
            <Button
              type="button"
              variant="secondary"
              onClick={() => onOpenChange?.(false)}
              disabled={loading}
            >
              {cancelText}
            </Button>
            <Button type="submit" loading={loading}>
              {submitText}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogClose,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
  DialogBody,
  ConfirmDialog,
  FormDialog,
};

