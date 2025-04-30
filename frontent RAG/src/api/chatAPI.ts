import { api } from './clientAPI'
import { ChatSession } from '../types/ChatSession'
import { Message } from '../types/Message'

export const fetchSessions = async (): Promise<ChatSession[]> => {
	try {
		const res = await api.get<{ data: ChatSession[] }>('/sessions/1')
		return res.data.data
	} catch (error) {
		console.error('Error fetching sessions:', error)
		return []
	}
}

export const fetchMessages = async (sessionID: number): Promise<Message[]> => {
	try {
		const res = await api.get<{ data: Message[] }>(`/messages/${sessionID}/`)
		return res.data.data
	} catch (error) {
		console.error('Error fetching messages:', error)
		return []
	}
}
