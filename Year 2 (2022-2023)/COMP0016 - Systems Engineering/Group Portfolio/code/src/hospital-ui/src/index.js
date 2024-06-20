import React from "react";
import ReactDOM from "react-dom/client";
import { ChakraProvider } from "@chakra-ui/react";
import SpatialNavigation from "./spatial_navigation";
import "@fontsource/fira-sans";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import theme from "./theme";
import Root from "./routes/root";
import StartPage from "./routes/start_page";
import LoginPage from "./routes/login_page";
import AppointmentTypePage from "./routes/appointment_type_page";
import WalkInPage from "./routes/walk_in_page";
import PrebookedPage from "./routes/prebooked_page";
import CheckedInPage from "./routes/checked_in_page";
import './index.css'

window.addEventListener("load", function () {
  // Initialize
  SpatialNavigation.init();

  // Define navigable elements (elements with "focusable" class).
  SpatialNavigation.add({
    selector: "a, .focusable, button, input",
  });

  // Make the *currently existing* navigable elements focusable.
  SpatialNavigation.makeFocusable();

  // Focus the first navigable element.
  SpatialNavigation.focus();
});

// Janky solution to press virtual keyboard buttons on enter. The onpointerdown and onpointerup functions
// are used normally when clicking the virtual keyboard buttons, so we just make use of them when pressing enter
document.addEventListener("keyup", (e) => {
  if (
    e.key === "Enter" &&
    document.activeElement.classList.contains("hg-button")
  ) {
    document.activeElement.onpointerdown();
    document.activeElement.onpointerup();
  }
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        index: true,
        element: <StartPage />,
      },
      {
        path: "/login",
        element: <LoginPage />,
      },
      {
        path: "/appointmenttype",
        element: <AppointmentTypePage />,
      },
      {
        path: "/walkin",
        element: <WalkInPage />,
      },
      {
        path: "/prebooked",
        element: <PrebookedPage />,
      },
      {
        path: "/checkedin",
        element: <CheckedInPage />,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <RouterProvider router={router} />
    </ChakraProvider>
  </React.StrictMode>
);
