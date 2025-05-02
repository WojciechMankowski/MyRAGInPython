import React, { useState, useEffect } from 'react'
import Chat from './components/Chat'
import Header from './components/header'
import HistoryChat from './components/HistoryChat'
import './assets/css/main.css'
import { MessageContext } from './context/MessagesContext'
import { ChatSession } from './types/ChatSession'
import { Message } from './types/Message'
import { fetchMessages, fetchSessions } from './api/chatAPI'

const App: React.FC = () => {
	const [sessions, setSessions] = useState<ChatSession[]>([])
	const [messages, setMessages] = useState<Message[]>([])
	const [sessionID, setSessionID] = useState<number>(0)

	// loading & error states
	const [loadingMessages, setLoadingMessages] = useState<boolean>(false)
	const [loadingSessions, setLoadingSessions] = useState<boolean>(false)
	const [errorMessages, setErrorMessages] = useState<string | null>(null)
	const [errorSessions, setErrorSessions] = useState<string | null>(null)

	useEffect(() => {
		const loadMessages = async () => {
			setErrorMessages(null)
			setLoadingMessages(true)
			try {
				const res = await fetchMessages(sessionID)
				setMessages(res)
			} catch (err: any) {
				setErrorMessages(err.message ?? 'Błąd pobierania wiadomości')
			} finally {
				setLoadingMessages(false)
			}
		}
		loadMessages()
	}, [sessionID])

	useEffect(() => {
		const loadSessions = async () => {
			setErrorSessions(null)
			setLoadingSessions(true)
			try {
				const res = await fetchSessions()
				setSessions(res)
			} catch (err: any) {
				setErrorSessions(err.message ?? 'Błąd pobierania sesji')
			} finally {
				setLoadingSessions(false)
			}
		}
		loadSessions()
	}, [sessionID])

	// sort messages chronologically
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

				<aside className="p-4">
					{loadingSessions && <p>Ładowanie sesji…</p>}
					{errorSessions && <p className="text-red-600">{errorSessions}</p>}
					<h2>Aktywna sesja: {sessionID}</h2>
				</aside>

				<div className="flex flex-1 overflow-hidden">
					<aside className="w-1/4 bg-white p-4 overflow-auto shadow-lg">
						<HistoryChat />
					</aside>
					<main className="flex-1 p-4 bg-gray-100 overflow-auto w-5/6">
						{loadingMessages && <p>Ładowanie wiadomości…</p>}
						{errorMessages && <p className="text-red-600">{errorMessages}</p>}
						{!loadingMessages && !errorMessages && <Chat />}
					</main>
				</div>
			</div>
		</MessageContext.Provider>
	)
}

export default App
