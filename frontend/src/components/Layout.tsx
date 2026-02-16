import { LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/ThemeToggle"

interface LayoutProps {
  children: React.ReactNode
  email?: string
  onSignOut?: () => void
}

export function Layout({ children, email, onSignOut }: LayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center mx-auto max-w-4xl px-4">
          <div className="mr-4 font-bold text-lg">Money Roundup</div>
          <div className="flex flex-1 items-center justify-end space-x-2">
            {email && (
              <span className="text-sm text-muted-foreground hidden sm:inline">
                {email}
              </span>
            )}
            <ThemeToggle />
            {onSignOut && (
              <Button variant="ghost" size="icon" onClick={onSignOut}>
                <LogOut className="h-5 w-5" />
                <span className="sr-only">Sign out</span>
              </Button>
            )}
          </div>
        </div>
      </header>
      <main className="container mx-auto max-w-4xl px-4 py-8">
        {children}
      </main>
    </div>
  )
}
