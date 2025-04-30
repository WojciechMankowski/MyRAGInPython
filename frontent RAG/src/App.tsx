import React, { useState, useEffect } from 'react'
import Chat from './components/Chat'
import Header from './components/header'
import HistoryChat from './components/HistoryChat'
import './assets/css/main.css'
import { MessageContext } from './context/MessagesContext'
import { ChatSession } from './types/ChatSession'
import { Message } from './types/Message'
import { fetchMessages } from './api/chatAPI'
import { fetchSessions } from './api/chatAPI'

const App: React.FC = () => {
	const [sessions, setSessions] = useState<ChatSession[]>([])
	const [messages, setMessages] = useState<Message[]>([])
	const [sessionID, setSessionID] = useState<number>(11)

	useEffect(() => {
		const fetch = async () => {
			const res = await fetchMessages(sessionID)
			setMessages(res)
		}
		fetch()
	}, [sessionID])

	useEffect(() => {
		const fetch = async () => {
			const res = await fetchSessions()
			setSessions(res)
		}
		fetch()
	}, [sessionID])
	
	messages.sort((a, b) => {
		const date_a = new Date(a.created_at).getTime()
		const date_b = new Date(b.created_at).getTime()
		return date_a - date_b
	})
	
	return (
		<MessageContext.Provider
			value={{
				sessions,
				setSessions,
				messages,
				setMessages,
				sessionID,
				setSessionID,
			}}>
			<div className="flex h-screen flex-col">
				<Header />
				<h2>Aktywna sesja: {sessionID}</h2>
				<div className="flex flex-1 overflow-hidden">
					<aside className="w-1/4 bg-white p-4 overflow-auto shadow-lg">
						<HistoryChat />
					</aside>
					<main className="flex-1 p-4 bg-gray-100 overflow-auto">
						<Chat />
					</main>
				</div>
			</div>
		</MessageContext.Provider>
	)
}

export default App
