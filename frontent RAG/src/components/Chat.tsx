import { InputUser } from "./userInput";

const Chat = () => {
  return (
    <div className="w-3xl mx-auto min-h-[650px] h-[800px] flex flex-col border rounded-2xl shadow-lg overflow-hidden p-3">
      <div className="flex-1 p-4 space-y-2 overflow-y-auto bg-gray-50">
        <div className="self-start bg-white px-4 py-2 rounded-xl shadow text-sm max-w-xs">
          Cześć! Jak mogę pomóc?
        </div>
        <div className="self-end bg-blue-500 text-white px-4 py-2 rounded-xl shadow text-sm max-w-xs ml-auto">
          Hej, mam pytanie.
        </div>
      </div>
      
      {/* Sekcja inputu */}
      <div className="border-t p-3 bg-white">
        <InputUser />
      </div>
    </div>
  );
};

export default Chat;
