import { Heading, Image, VStack } from "@chakra-ui/react";
import logo from "./logo.png";
import CustomButton from "../components/CustomButton";
import CustomRadio from "../components/CustomRadio";

export default function PrebookedPage() {
  
  const bookings = [
    { key: 0, date: 'Fri Jan 20, 2023', time: '12:30PM'},
    { key: 1, date: 'Tue Mar 12, 2023', time: '05:45PM'},
    { key: 2, date: 'Sun Jun 09, 2023', time: '08:00AM'},
  ];

  return (
    <VStack spacing={10} h={"100%"} justify={"center"}>
      <Image src={logo} maxH={"15%"} />
      <Heading fontSize={"5xl"} fontWeight={"bold"}>
        Choose Bookings
      </Heading>
        <VStack>
          {bookings.map((booking) => {
            return(
            <CustomRadio
              name='Jane Doe'
              phone='xxxxxxx-6987'
              {...booking}
            />
            )
          })}
        </VStack>
      <CustomButton
        href="/checkedin"
        bgGradient="linear(to-b, blue.600, blue.700)"
        text="Check in"
      />
    </VStack>
  );
}
