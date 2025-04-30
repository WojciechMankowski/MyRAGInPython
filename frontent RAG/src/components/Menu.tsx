// Menu.tsx
import { PlusCircle } from 'lucide-react'
import { api } from '../api/clientAPI'
import React from 'react'
import { useMessageContext } from '../context/MessagesContext'
// import { useMessagesContext } from '../context/MessagesContext'

const Menu: React.FC<{ user_id: number }> = ({ user_id }) => {
	const { setSessionID } = useMessageContext()

	const newSession = async () => {
		const res = await api.post(`/new/sessions/${user_id}`)
		const newId = res.data.data[0].id
		setSessionID(newId)
		// po setSessionId hook kontekstowy zrobi refresh i Chat przeładuje wiadomości
	}

	return (
		<nav className="shadow-md px-4 py-2 rounded-lg">
			<ul className="flex space-x-4">
				<li>
					<button onClick={newSession} className="flex items-center px-3 py-2 text-white rounded-lg transition">
						<PlusCircle className="w-5 h-5 mr-2" size={48} color="blue" />
					</button>
				</li>
			</ul>
		</nav>
	)
}

export default Menu
