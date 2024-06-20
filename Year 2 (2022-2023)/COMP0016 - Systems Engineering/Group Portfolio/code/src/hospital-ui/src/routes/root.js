import { Box, Flex } from "@chakra-ui/react";
import { useEffect } from 'react';
import { Outlet, useLocation } from "react-router-dom";
import { HomeIcon, BackIcon } from "../components/MenuBarIcon";
import SpatialNavigation from "../spatial_navigation";

function Navbar() {
  return (
    <Box p={5} h={"10%"}>
      <Flex
        direction="row"
        gap={8}
        alignItems={"center"}
        justify={"end"}
        h={"100%"}
      >
        <HomeIcon />
        <BackIcon />
      </Flex>
    </Box>
  );
}

export default function Root() {
  const location = useLocation();

  useEffect(()=>{
    // Focus the first navigable element.
    SpatialNavigation.focus();
    console.log("Route Changed");
  }, [location])

  return (
    <>
      <Box h={"100vh"}>
        <Navbar />
        <Box p={4} h={"90%"}>
          <Outlet />
        </Box>
      </Box>
    </>
  );
}
