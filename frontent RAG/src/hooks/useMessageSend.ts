import { useState } from 'react'
import { Message } from '../types/Message'
import { api } from '../api/clientAPI'

export const useMessageSend = (message: Message) => {
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)

	const sendMessge = async () => {
		setLoading(true)
		setError(null)

		try {
			const res = await api.post(`ask/${message.content}/${message.session_id}}`)
			const create = res.data[0]
			return create
		} catch (error) {
			console.error(error)
			setError('Nie udało się wysłać wiadomości')
		} finally {
			setLoading(false)
		}
	}

	return [sendMessge, loading, error]
}
