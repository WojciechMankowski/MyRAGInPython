import { PropsMessage } from '../types/Props'
import React from 'react'
import Markdown from 'react-markdown'
import { InfoTooltip } from './InfoTooltip'
import CopyButton from './CopyButton'

const MessageCard: React.FC<PropsMessage> = ({ message, sender, info, title }) => {
	const isUser = sender === 'user'
	const userName = 'Wojtek'
	const source = [...new Set(info)]
	return (
		<div className={`w-full flex px-3.5 ${isUser ? 'justify-start' : 'justify-end'}`}>
			<div
				className={`
					mt-[20px] rounded-2xl shadow-md px-2 py-2
					// max-w-[40rem] 
					${isUser ? 'bg-blue-100 text-left' : 'bg-gray-100 text-right'}
				`}>
				<div className="flex justify-between items-center mb-2 text-sm">
					<span className={`${isUser ? 'text-blue-700' : 'text-gray-700'}`}>{isUser ? userName : 'Assistant'}</span>
					<span className="text-xs text-gray-500 ml-2">{new Date(message.created_at).toLocaleString()}</span>
				</div>

				<span
					className={`prose prose-sm break-words 
					${isUser ? 'text-blue-900' : 'text-gray-800 text-left'}`}>
					<Markdown>{message.content}</Markdown>
				</span>
				<div className="icon flex items-start pt-5">
					<span className="pr-2">
						<CopyButton text={message.content} title={title} />
					</span>
					{isUser ? '' : <InfoTooltip info={source} />}
				</div>
			</div>
		</div>
	)
}

export default MessageCard
