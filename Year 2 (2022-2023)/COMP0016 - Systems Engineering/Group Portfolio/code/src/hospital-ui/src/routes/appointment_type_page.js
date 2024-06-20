import { Heading, Image, VStack } from "@chakra-ui/react";
import logo from "./logo.png";
import CustomButton from "../components/CustomButton";

export default function AppointmentTypePage() {
  return (
      <VStack spacing={10} h={"100%"} justify={"center"}>
        <Image src={logo} maxH={"15%"} />
        <Heading fontSize={"5xl"} fontWeight={"bold"}>
          Appointment Type
        </Heading>
        <CustomButton
          href="/prebooked"
          bgGradient="linear(to-b, blue.600, blue.700)"
          text="Pre-Booked"
        />
        <CustomButton
          href="/walkin"
          bgGradient="linear(to-b, blue.600, blue.700)"
          text="Walk In"
        />
      </VStack>
  );
}
