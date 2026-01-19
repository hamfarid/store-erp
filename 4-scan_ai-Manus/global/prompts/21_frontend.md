# Frontend Development Guidelines (v26.0)

## 1. Architecture: The Nx Monorepo Standard
**For New Projects:** All frontend work must be structured within an **Nx Workspace**.
**Why?**
- **Scalability:** Supports multiple apps (Web, Mobile, Admin) in one repo.
- **Speed:** Computation caching (don't rebuild what hasn't changed).
- **Consistency:** Shared libraries for UI components (`libs/ui`).

### Directory Structure (Nx)
```
my-org/
├── apps/
│   ├── web/          (Next.js/React - Customer Facing)
│   ├── admin/        (React/Vite - Internal Dashboard)
│   └── mobile/       (React Native - Optional)
├── libs/
│   ├── ui/           (Shared Shadcn/UI components)
│   ├── util/         (Shared helper functions)
│   └── data-access/  (API hooks, Supabase client)
├── tools/
└── nx.json
```

---

## 2. The Modern UI Standard (Magic UI + Shadcn)
**Rule:** For all new frontend projects, you MUST use the following stack:
*   **Framework:** React 18+ (Next.js App Router or Vite).
*   **Styling:** Tailwind CSS.
*   **Components:** **Shadcn UI** (for functional components like Buttons, Inputs).
*   **Effects:** **Magic UI** (for visual "wow" factors like Marquees, Bento Grids, Animated Lists).
*   **State:** Zustand (Global), TanStack Query (Server).
*   **Forms:** React Hook Form + Zod.

### Why Magic UI?
To ensure the application feels "premium" and "modern" out of the box.

---

## 3. Legacy Support (Existing Projects)
If the project is **NOT** using the modern stack:
1.  **Respect the Architecture:** Do not force Nx on a simple `create-react-app` unless requested.
2.  **Incremental Adoption:**
    *   Add **Tailwind** if CSS is messy.
    *   Add **TanStack Query** if data fetching is chaotic.
    *   Add **Vitest** for unit testing.

---

## 4. Component Guidelines (The "Atomic" Way)
*   **Presentational vs. Container:** Keep logic separate from UI.
*   **Props:** Use TypeScript interfaces for all props.
*   **Accessibility:** All interactive elements must be keyboard accessible (use Radix/Headless UI).

### Example: Button Component
```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/libs/util"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```
