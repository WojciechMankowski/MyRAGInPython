import Chat from './components/Chat';
import Header from './components/header';
import './assets/css/main.css';

function App() {
  return (
    <>
      <Header />
      <main className="flex items-center justify-center min-h-screen bg-gray-100">
        <Chat />
      </main>
    </>
  );
}

export default App;
