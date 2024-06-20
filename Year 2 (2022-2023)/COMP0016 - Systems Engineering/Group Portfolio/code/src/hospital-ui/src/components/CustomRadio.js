import { useState } from "react";
import { Text, HStack, Box } from "@chakra-ui/react";

export default function CustomRadio({ date, time, name, phone}) {
  const [selected, setSelected] = useState(false);

  const handleClick = () => {
    setSelected(!selected)
  }

  return (
    <Box as="button" bg={selected ? "blue.600" : 'white'} color={selected ? "white" : 'blue.600'} p={4} w={"100%"} onClick={handleClick}>
      <HStack spacing={10} h={"5vh"}>
        <Text>{name}</Text>
        <Text>{phone}</Text>
        <Text>{date}</Text>
        <Text>{time}</Text>
      </HStack>
    </Box>
  );
}
