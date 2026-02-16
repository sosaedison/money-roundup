import { Card, CardContent } from "@/components/ui/card"

interface Props {
  name: string
}

export default function AccountItem({ name }: Props) {
  return (
    <Card>
      <CardContent className="flex items-center p-4">
        <span className="font-medium">{name}</span>
      </CardContent>
    </Card>
  )
}
