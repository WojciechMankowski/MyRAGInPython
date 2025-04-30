import Menu from './Menu'
interface Props {
	setSessionID: React.Dispatch<React.SetStateAction<number>>
}

export default function Header() {
	return (
		<header className="bg-white shadow-md p-4 flex items-center justify-between">
			<Menu user_id={1}  />
			<div className="text-xl font-bold">Baza wiedzy z AI</div>
		</header>
	)
}
