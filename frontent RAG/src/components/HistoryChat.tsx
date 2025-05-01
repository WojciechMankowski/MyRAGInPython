import { useMessageContext } from '../context/MessagesContext'
import Markdown from 'react-markdown'

const HistoryChat = () => {
	const { sessions, sessionID, setSessionID } = useMessageContext()

	const clickHistory = (id: number) => setSessionID(id)

	return (
		<section className="history-chat overflow-auto p-4 bg-white rounded-lg shadow">
			<h2 className="text-xl font-semibold mb-4">Historia czatu</h2>

			{sessions.length === 0 ? (
				<p className="text-sm text-gray-500">Brak sesji do wyświetlenia</p>
			) : (
				sessions.map(session => (
					<div
						key={session.id}
						/* jasnoszare tło, gdy ta sesja jest wybrana */
						className={`flex items-center justify-between p-2 rounded transition-colors mb-2
              ${session.id === sessionID ? 'bg-gray-200' : 'hover:bg-gray-100'}`}>
						<button onClick={() => clickHistory(session.id)} className="text-left">
							<span className="block text-sm text-gray-500">{new Date(session.created_at).toLocaleString()}</span>
							<span className="block text-base text-gray-800">
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
