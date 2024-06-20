import { Box, Icon } from "@chakra-ui/react";
import { useNavigate, useLocation } from "react-router-dom";
import { MdHome, MdArrowCircleLeft } from "react-icons/md";


export function HomeIcon() {
  const navigate = useNavigate();
  return (
    <Box
      as={"button"}
      height={"100%"}
      bgColor={"white"}
      rounded={"full"}
      type="button"
      onClick={() => {
        navigate("/");
      }}
    >
      <Icon as={MdHome} w={"auto"} h={"100%"} color={"blue.700"} />
    </Box>
  );
}

export function BackIcon() {
  const navigate = useNavigate();
  const location = useLocation();
  return (
    <Box
      as={"button"}
      height={"100%"}
      bgColor={"gray.100"}
      rounded={"full"}
      type="button"
      onClick={() => {
        navigate(location.pathname === "/" ? "/" : -1);
      }}
    >
      <Icon as={MdArrowCircleLeft} w={"auto"} h={"100%"} color={"blue.700"} />
    </Box>
  );
}
