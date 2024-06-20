import { Text, VStack } from "@chakra-ui/react";
import { Link } from "react-router-dom";

export default function CustomButton({ href, bgGradient, text }) {
  return (
    <VStack
      as={Link}
      to={href}
      width={"15%"}
      height={"8%"}
      bgGradient={bgGradient}
      rounded={"4px"}
      justify={"center"}
    >
      <Text fontSize={"30px"} color={"white"}>
        {text}
      </Text>
    </VStack>
  );
}
