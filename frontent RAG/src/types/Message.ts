export type SenderType = 'user' | 'assistant' | 'system'

export interface Message {
	id: number | null
	session_id: number
	sender: SenderType
	content: string
	created_at: Date
	metadata?: Record<string, any> // jeśli metadata jest jsonb, to pasuje Record
}
