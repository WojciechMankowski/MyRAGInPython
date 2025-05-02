import React, { useState, useEffect } from 'react'
import { FiCopy } from 'react-icons/fi'

interface CopyButtonProps {
	/** Tekst do skopiowania */
	text: string
	title: string | undefined | null
}

const CopyButton: React.FC<CopyButtonProps> = ({ text, title }) => {
	const [copied, setCopied] = useState(false)
	const handleCopy = async () => {
		try {
			await navigator.clipboard.writeText(`Tytuł sesji: ${title}. Tekst: ${text}`)
			setCopied(true)
		} catch (err) {
			console.error('Nie udało się skopiować tekstu:', err)
		}
	}

	useEffect(() => {
		if (copied) {
			const timer = setTimeout(() => setCopied(false), 2000)
			return () => clearTimeout(timer)
		}
	}, [copied])

	return (
		<button onClick={handleCopy} className="relative text-gray-500 hover:text-gray-700" aria-label="Kopiuj">
			<FiCopy className="text-blue-500 w-5 h-5 cursor-copy" />
			{copied && (
				<span
					className="absolute -top-6 left-1/2 transform -translate-x-1/2
          bg-gray-800 text-white text-xs rounded px-2 py-1 whitespace-nowrap z-10">
					Skopiowano!
				</span>
			)}
		</button>
	)
}

export default CopyButton
