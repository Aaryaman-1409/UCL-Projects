import { Text, Input, VStack } from "@chakra-ui/react";
import "react-simple-keyboard/build/css/index.css";
import "./InputKeyboard.css";

export default function CustomInput({ text, inputState, onFocus, id }) {
  return (
    <>
      <VStack spacing={2}>
        <Text fontSize={"30px"} alignSelf={"start"}>
          {text}
        </Text>
        <Input
          onFocus={onFocus}
          id={id}
          value={inputState.inputs[id] || ""}
          htmlSize={15}
          width="auto"
          placeholder={text}
          bgColor={"white"}
          readOnly={true}
        />
      </VStack>
    </>
  );
}
