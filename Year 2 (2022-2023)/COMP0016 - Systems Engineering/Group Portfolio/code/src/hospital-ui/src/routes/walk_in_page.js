import {
  Heading,
  Icon,
  Image,
  VStack,
  Card,
  Text,
  CardBody,
} from "@chakra-ui/react";
import logo from "./logo.png";
import CustomButton from "../components/CustomButton";
import { MdReceipt } from "react-icons/md";

export default function WalkInPage() {
  return (
    <VStack spacing={10} h={"100%"} justify={"center"}>
      <Image src={logo} maxH={"15%"} />
      <Heading fontSize={"5xl"} fontWeight={"bold"}>
        Thank You
      </Heading>
      <Card maxW="sm" align={"center"}>
        <CardBody>
          <VStack mt="6" spacing="3">
            <Icon as={MdReceipt} w={"30%"} h={"auto"} color={"blue.700"} />
            <Heading color="blue.600" size="lg">
              Reference Number: {Math.floor(Math.random() * 100)}
            </Heading>
            <Text align={"center"}>
              Your walk-in appointment booking is almost complete. To continue,
              please go to a free counter at the reception and give them this
              reference number
            </Text>
          </VStack>
        </CardBody>
      </Card>
      <CustomButton
        href="/"
        bgGradient="linear(to-b, green.600, green.700)"
        text="Home"
      />
    </VStack>
  );
}
