import React, { useRef, useEffect, useState, useCallback } from 'react'
import { InputUser } from './userInput'
import MessageCard from './messageUser'
import { useMessageContext } from '../context/MessagesContext'

const SCROLL_THRESHOLD = 50

const Chat: React.FC = () => {
	const { messages, sessions, sessionID } = useMessageContext()
	const containerRef = useRef<HTMLDivElement>(null)
	const [autoScroll, setAutoScroll] = useState(true)
	let title: string | undefined | null = ''

	if (sessionID !== 0) {
		const session = sessions.find(s => s.id === sessionID)
		title = session?.title // jeśli nie ma takiej sesji, title będzie undefined
	}
	// Scroll to bottom when new messages arrive
	useEffect(() => {
		const container = containerRef.current
		if (container && autoScroll) {
			container.scrollTop = container.scrollHeight
		}
	}, [messages, autoScroll])

	// Detect user's manual scrolling
	const handleScroll = useCallback(() => {
		const container = containerRef.current
		if (!container) return
		const distanceFromBottom = container.scrollHeight - container.scrollTop - container.clientHeight
		setAutoScroll(distanceFromBottom < SCROLL_THRESHOLD)
	}, [])

	return (
		<div className="h-full flex flex-col border border-gray-200 rounded-2xl shadow-lg bg-white overflow-hidden">
			{/* Scrollable messages container */}
			<div
				ref={containerRef}
				onScroll={handleScroll}
				className="flex-1 min-h-0 bg-gray-50 space-y-4 overflow-y-auto p-6">
				{messages.map((msg, index) => (
					<MessageCard
						key={msg.id ?? index}
						message={msg}
						sender={msg.sender}
						info={msg.metadata?.file_names ?? []}
						title={title}
					/>
				))}
			</div>

			{/* Input field */}
			<div className="p-4 bg-white border-t border-gray-200">
				<InputUser />
			</div>
		</div>
	)
}

export default Chat
