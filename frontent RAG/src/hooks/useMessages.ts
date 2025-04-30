import React, { useEffect, useState, createContext } from 'react'
import { ChatSession } from '../types/ChatSession'
import { Message } from '../types/Message'
import { api } from '../api/clientAPI'

const fetchSessions = async (): Promise<ChatSession[]> => {
	try {
		const res = await api.get<{ data: ChatSession[] }>('/sessions/1')
		return res.data.data
	} catch (error) {
		console.error('Error fetching sessions:', error)
		return []
	}
}

type MContext = {
	sessions: ChatSession[]
	setSessions: React.Dispatch<React.SetStateAction<ChatSession[]>>
	messages: Message[]
	setMessages: React.Dispatch<React.SetStateAction<Message[]>>
	sessionID: number
	setSessionID: React.Dispatch<React.SetStateAction<number>>
}

export const MessageContext = createContext<MContext>({
	sessions: [],
	setSessions: () => {}, // no-op
	messages: [],
	setMessages: () => {}, // no-op
	sessionID: 0,
	setSessionID: () => {}, // no-op
})

export const useMessages = () => {
	const [sessionID, setSessionID] = useState<number>(11)
	const [sessions, setSessions] = useState<ChatSession[]>([])
	const [messages, setMessages] = useState<Message[]>([])

	useEffect(() => {
		let isMounted = true
		;(async () => {
			const data = await fetchSessions()
			if (isMounted) setSessions(data)
		})()
		return () => {
			isMounted = false
		}
	}, [])

	return {
		sessionID,
		setSessionID,
		sessions,
		setSessions,
		messages,
		setMessages,
	}
}
