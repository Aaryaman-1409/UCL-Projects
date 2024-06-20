import { Heading, Image, VStack } from "@chakra-ui/react";
import logo from "./logo.png";
import CustomButton from "../components/CustomButton";

export default function StartPage() {
  return (
    <>
      <VStack spacing={10} h={"100%"} justify={"center"}>
        <Image src={logo} maxH={"15%"} />
        <Heading fontSize={"7xl"} fontWeight={"bold"}>
          Self Check-in
        </Heading>
        <CustomButton
          href="/login"
          bgGradient="linear(to-b, blue.600, blue.700)"
          text="Start"
        />
      </VStack>
    </>
  );
}
