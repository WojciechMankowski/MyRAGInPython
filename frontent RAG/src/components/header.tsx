import Menu from './Menu'

export default function Header() {
	return (
		<header className="bg-white shadow-md p-4 flex items-center">
			{/* lewa strona */}
			<Menu user_id={1} />

			{/* środek – rośnie na całą szerokość i centruje napis */}
			<h1 className="flex-1 text-center text-xl font-bold">Baza wiedzy z AI</h1>
		</header>
	)
}
