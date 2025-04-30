import { useState, KeyboardEvent } from 'react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { api } from '../api/clientAPI'
import { useMessageContext } from '../context/MessagesContext'

export const InputUser = () => {
	const [inputValue, setInputValue] = useState('')
	const [sending, setSending] = useState(false)
	const { sessionID } = useMessageContext()

	const askQuestion = async () => {
		const question = inputValue.trim()
		if (!question || sending) return

		setSending(true)
		try {
			await api.post('/ask/', { question, session: sessionID })
			setInputValue('')
			// po wysłaniu pobieramy nowe wiadomości
			// await refreshMessages()
		} catch (e) {
			console.error('Błąd zapytania:', e)
		} finally {
			setSending(false)
		}
	}

	const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
		if (e.key === 'Enter') {
			e.preventDefault()
			askQuestion()
		}
	}

	return (
		<div className="flex items-center gap-2 w-full">
			<Input
				type="text"
				placeholder="Wpisz coś..."
				className="flex-1"
				value={inputValue}
				onChange={e => setInputValue(e.target.value)}
				onKeyDown={handleKeyDown}
				disabled={sending}
			/>
			<Button onClick={askQuestion} disabled={sending || inputValue.trim() === ''}>
				{sending ? 'Wysyłanie…' : 'Wyślij'}
			</Button>
		</div>
	)
}
