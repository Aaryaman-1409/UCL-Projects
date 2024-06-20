import { useState } from "react";
import { Heading, Image, HStack, VStack } from "@chakra-ui/react";
import logo from "./logo.png";
import CustomButton from "../components/CustomButton";
import CustomInput from "../components/CustomInput";
import CustomKeyboard from "../components/CustomKeyboard";

export default function LoginPage() {
  const [inputState, setInputState] = useState({
    inputName: "",
    inputs: {},
  });

  const onFocus = (event) => {
    setInputState({ ...inputState, inputName: event.target.id });
  };

  return (
    <>
      <VStack spacing={10} h={"100%"} justify={"center"}>
        <Image src={logo} maxH={"15%"} />
        <Heading fontSize={"5xl"} fontWeight={"bold"}>
          Account Information
        </Heading>
        <HStack spacing={8}>
          <CustomInput
            id="Userid"
            text="User ID"
            inputState={inputState}
            onFocus={onFocus}
          />
          <CustomInput
            id="Pin"
            text="Pin"
            inputState={inputState}
            onFocus={onFocus}
          />
        </HStack>
        <CustomKeyboard inputState={inputState} setInputState={setInputState} />
        <CustomButton
          href="/appointmenttype"
          bgGradient="linear(to-b, blue.600, blue.700)"
          text="Log In"
        />
      </VStack>
    </>
  );
}
