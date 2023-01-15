import {Component, ReactElement} from 'react'
import AccountItem from "./AccountItem"
import { AccountItemType } from './AppTypes'

interface Props {
    accounts: any[]
    toggleActive?: Function
}


export default function AccountItemList({accounts, toggleActive}: Props){

    return (
        <>
            {accounts.map((accountItem, index) => {
                return <AccountItem key={index} name={accountItem.name} />
            })}
        </>
        
    )
}