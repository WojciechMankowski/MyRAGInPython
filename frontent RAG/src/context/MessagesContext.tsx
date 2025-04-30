import React, { createContext, useContext } from 'react'
import { ChatSession } from '../types/ChatSession'
import { Message } from '../types/Message'

export type MessageContextType = {
	sessions: ChatSession[]
	setSessions: React.Dispatch<React.SetStateAction<ChatSession[]>>
	messages: Message[]
	setMessages: React.Dispatch<React.SetStateAction<Message[]>>
	sessionID: number
	setSessionID: React.Dispatch<React.SetStateAction<number>>
}

const noop = () => {}

export const MessageContext = createContext<MessageContextType>({
	sessions: [],
	setSessions: noop,
	messages: [],
	setMessages: noop,
	sessionID: 0,
	setSessionID: noop,
})

export const useMessageContext = (): MessageContextType => {
	const ctx = useContext(MessageContext)
	// console.log(ctx.messages)
	return ctx
}
