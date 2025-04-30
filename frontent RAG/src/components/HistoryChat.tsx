import { useMessageContext } from '../context/MessagesContext'
import Markdown from 'react-markdown'

const HistoryChat = () => {
	const { sessions, setSessionID } = useMessageContext()
	const clickHistory = (sessionID: number) => {
		setSessionID(sessionID)
	}
	return (
		<section className="history-chat  overflow-auto p-4 bg-white rounded-lg shadow">
			<h2 className="text-xl font-semibold mb-4">Historia czatu</h2>
			{sessions.length === 0 ? (
				<p className="text-sm text-gray-500">Brak sesji do wyświetlenia</p>
			) : (
				sessions.map(session => (
					<div
						key={session.id}
						className="flex items-center justify-between p-2 hover:bg-gray-100 rounded transition-colors mb-2">
						<button onClick={() => clickHistory(session.id)}>
							<span className="text-sm text-gray-500">{new Date(session.created_at).toLocaleString()}</span>
							<span className="text-base text-gray-800">
								<Markdown>{session.title}</Markdown>
							</span>
						</button>
					</div>
				))
			)}
		</section>
	)
}

export default HistoryChat
