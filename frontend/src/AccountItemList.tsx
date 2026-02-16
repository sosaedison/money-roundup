import AccountItem from "./AccountItem"

interface Props {
  accounts: { name: string }[]
}

export default function AccountItemList({ accounts }: Props) {
  return (
    <div className="space-y-3">
      {accounts.map((accountItem, index) => (
        <AccountItem key={index} name={accountItem.name} />
      ))}
    </div>
  )
}
