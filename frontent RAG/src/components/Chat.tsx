import { useRef, useEffect, useState } from 'react'
import { InputUser } from './userInput'
import MessageCard from './messageUser'
import { useMessageContext } from '../context/MessagesContext' // <-- poprawne

const Chat = () => {
	const { messages } = useMessageContext()
	const containerRef = useRef<HTMLDivElement>(null)
	const [autoScroll, setAutoScroll] = useState(true)

	useEffect(() => {
		const c = containerRef.current
		if (c && autoScroll) {
			c.scrollTop = c.scrollHeight
		}
	}, [messages, autoScroll])

	const handleScroll = () => {
		const c = containerRef.current
		if (!c) return
		const isAtBottom = c.scrollHeight - c.scrollTop - c.clientHeight < 50
		setAutoScroll(isAtBottom)
	}

	return (
		<div className="max-w-4xl mx-auto h-full flex flex-col border border-gray-200 rounded-2xl shadow-lg bg-white overflow-hidden">
			{/* Scrollowalny kontener */}
			<div
				ref={containerRef}
				onScroll={handleScroll}
				className="flex-1 min-h-0 bg-gray-50 space-y-4 overflow-y-auto p-6">
				{messages.map((msg, i) => (
					<MessageCard key={msg.id ?? i} message={msg} sender={msg.sender} />
				))}
			</div>

			{/* Pole input */}
			<div className="p-4 bg-white border-t border-gray-200">
				<InputUser />
			</div>
		</div>
	)
}

export default Chat
