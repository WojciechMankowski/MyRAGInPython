import { Button } from "./ui/button";
import {Input} from "./ui/input";

export const InputUser = () => {
  return (
    <div className="flex items-center gap-2 w-full">
      <Input
        type="text"
        placeholder="Wpisz coś..."
        className="flex-1"
      />
      <Button>
        Wyślij
      </Button>
    </div>
  );
};
