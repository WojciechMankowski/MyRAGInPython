export interface PropsInputUser {
	sessionID: number
	userName: string
	loadingData: boolean
	setLoadingData: React.Dispatch<React.SetStateAction<boolean>>
}
import { Message } from './Message'
export interface PropsChat {
	data: Message[]
	loadingData: boolean
	setLoadingData: React.Dispatch<React.SetStateAction<boolean>>
}

export interface PropsMessage {
	message: Message
	sender: string
	info: string[]
	title: string | undefined | null
}
export interface PropsInputUser {
	sessionID: number
	userName: string
}

export interface PropsMenu {
	user_id: number
	setSessionID: React.Dispatch<React.SetStateAction<number>>
}
