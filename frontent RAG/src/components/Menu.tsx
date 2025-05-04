// Menu.tsx
import { PlusCircle, RefreshCw } from 'lucide-react'
import { api } from '../api/clientAPI'
import React, { useState } from 'react'
import { useMessageContext } from '../context/MessagesContext'

const Menu: React.FC<{ user_id: number }> = ({ user_id }) => {
	const { setSessionID } = useMessageContext()
	const [isHovered, setIsHovered] = useState(false)
	const colorIcon = isHovered ? 'white' : 'blue'
	const fontIcon = 48
	const fontIconHover = isHovered ? fontIcon * 0.25 + fontIcon : fontIcon

	const newSession = async () => {
		const res = await api.post(`/new/sessions/${user_id}`)
		const newId = res.data.data[0].id
		setSessionID(newId)
	}
	const refreshVectorDatabase = async () => {
		const res = await api.patch('/documents')
		console.log(res)
	}
	return (
		<nav className="shadow-md px-4 py-2 rounded-lg">
			<ul className="flex space-x-6">
				<li>
					<button
						onClick={newSession}
						className="flex items-center justify-center px-4 py-2  rounded-lg transition-transform transform hover:scale-110 hover:bg-blue-600 duration-200"
						onMouseEnter={() => setIsHovered(true)}
						onMouseLeave={() => setIsHovered(false)}>
						<PlusCircle className="w-5 h-5 mr-2" size={fontIconHover} color={colorIcon} />
					</button>
				</li>
				<li>
					<button
						className="flex items-center justify-center px-4 py-2  rounded-lg transition-transform transform hover:scale-110 hover:bg-blue-600 duration-200
					"
						onMouseEnter={() => setIsHovered(true)}
						onMouseLeave={() => setIsHovered(false)}
						onClick={refreshVectorDatabase}
						>
						<RefreshCw className="w-5 h-5 mr-2" size={fontIconHover} color={colorIcon} />
					</button>
				</li>
			</ul>
		</nav>
	)
}

export default Menu
