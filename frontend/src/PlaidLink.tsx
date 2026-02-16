import { Plus } from "lucide-react"
import { Button } from "@/components/ui/button"

interface Props {
  open: Function
  ready: boolean
}

export default function PlaidLink({ open, ready }: Props) {
  return (
    <Button onClick={() => open()} disabled={!ready}>
      <Plus className="mr-2 h-4 w-4" />
      Link account
    </Button>
  )
}
