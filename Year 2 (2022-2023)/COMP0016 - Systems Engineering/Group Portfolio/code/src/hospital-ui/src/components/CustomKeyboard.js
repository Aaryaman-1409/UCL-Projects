import { useRef, useEffect } from "react";
import Keyboard from "react-simple-keyboard";
import "react-simple-keyboard/build/css/index.css";
import "./InputKeyboard.css";

export default function CustomKeyboard({ inputState, setInputState }) {
  const keyboard = useRef();

  const onChangeAll = (inputs) => {
    setInputState({ ...inputState, inputs: inputs });
  };

  return (
    <Keyboard
      inputName={inputState.inputName}
      keyboardRef={(r) => (keyboard.current = r)}
      layoutName={"default"}
      onChangeAll={onChangeAll}
      useButtonTag={true}
      layout={{
        default: ["1 2 3", "4 5 6", "7 8 9", "- 0 {bksp}"],
      }}
    />
  );
}
