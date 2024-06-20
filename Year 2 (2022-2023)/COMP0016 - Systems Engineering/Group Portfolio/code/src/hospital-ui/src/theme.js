import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  shadows: { outline: "0 0 0 3px var(--chakra-colors-green-500)" },
  fonts: {
    heading: `Fira Sans`,
    body: `Fira Sans`,
  },
  styles: {
    global: () => ({
      body: {
        bgGradient: "linear(to-t, blue.100, white)",
        color: "blue.600",
      },
    }),
  },
});

export default theme;
