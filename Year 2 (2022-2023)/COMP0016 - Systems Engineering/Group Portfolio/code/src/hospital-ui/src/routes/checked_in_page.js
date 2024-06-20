import {
  Heading,
  Image,
  VStack,
  Card,
  Text,
  CardBody,
} from "@chakra-ui/react";
import logo from "./logo.png";
import CustomButton from "../components/CustomButton";

export default function CheckedInPage() {
  return (
    <VStack spacing={10} h={"100%"} justify={"center"}>
      <Image src={logo} maxH={"15%"} />
      <Heading fontSize={"5xl"} fontWeight={"bold"}>
        Thank You
      </Heading>
      <Card maxW="sm" align={"center"}>
        <CardBody>
          <VStack spacing="3">
            <Text align={"center"}>
              Check in completed successfully.
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
