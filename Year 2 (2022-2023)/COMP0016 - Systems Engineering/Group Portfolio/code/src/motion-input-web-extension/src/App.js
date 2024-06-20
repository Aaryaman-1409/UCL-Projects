import React, {
  useRef,
  useEffect,
  useState,
  useContext,
  useCallback,
} from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import styled from "styled-components";
import * as Chakra from "@chakra-ui/react";
import emoji_left_src from "./emoji_left.png";

const WebsocketContext = React.createContext(null);

function App() {
  const socketUrl = "ws://localhost:5786";
  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(
    socketUrl,
    {
      onOpen: () => console.log("opened"),
      shouldReconnect: (closeEvent) => true,
    }
  );

  return (
    <WebsocketContext.Provider
      value={{ sendJsonMessage, lastJsonMessage, readyState }}
    >
      <Chakra.Card>
        <Chakra.CardBody>
          <PreviewCanvas />
        </Chakra.CardBody>
        <Chakra.Divider />
        <Chakra.CardBody>
          <SensitivitySlider />
        </Chakra.CardBody>
        <Chakra.Divider />
        <Chakra.CardBody>
          <StatusInfo />
        </Chakra.CardBody>
      </Chakra.Card>
    </WebsocketContext.Provider>
  );
}

const PreviewWindowStyle = styled.div`
  background-color: ${(props) => props.bgColor};
  position: relative;
  box-sizing: border-box;
  width: ${(props) => props.width};
  aspect-ratio: ${(props) => props.aspectRatio};
  overflow: hidden;
`;

const PreviewWindowBorderTop = styled.div`
  position: absolute;
  top: 0%;
  left: 0%;
  width: 100%;
  height: ${props => props.threshold};
  background-color: ${(props) => props.bgColor};
  transition: background-color 0.5s linear;
`;

const PreviewWindowBorderBottom = styled.div`
  position: absolute;
  bottom: 0%;
  left: 0%;
  width: 100%;
  height: ${props => props.threshold};
  background-color: ${(props) => props.bgColor};
  transition: background-color 0.5s linear;
`;

const PreviewWindowBorderLeft = styled.div`
  position: absolute;
  top: 0%;
  left: 0%;
  width: ${props => props.threshold};
  height: 100%;
  background-color: ${(props) => props.bgColor};
  transition: background-color 0.5s linear;
`;

const PreviewWindowBorderRight = styled.div`
  position: absolute;
  top: 0%;
  right: 0%;
  width: ${props => props.threshold};
  height: 100%;
  background-color: ${(props) => props.bgColor};
  transition: background-color 0.5s linear;
`;

const EmojiHand = styled.img`
  position: absolute;
  src: ${(props) => props.src};
  width: auto;
  height: ${(props) => props.height};
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
`;

function PreviewCanvas() {
  const { lastJsonMessage } = useContext(WebsocketContext);
  const previewWindow = useRef();
  const emojiHand = useRef();
  const [threshold, setThreshold] = useState('0%'); //sensitivity divided by 2 in percentage. Used for preview window edges
  const baseColor = "#b6edb6"
  const highlightColor = "#77dd77"
  const [edgeColors, setEdgeColors] = useState({top: baseColor, bottom: baseColor, left: baseColor, right: baseColor})
  const aspectRatio = 4 / 3; // width divided by height of previewWindow. Represents aspect ratio of camera frame

  // using useCallback so that the function doesn't have to be defined again on rerenders
  // Draws the emoji on the previewwindow div using absolute positioning
  const drawEmoji = useCallback(({ x, y, depth, orientation }) => {
    const emoji = emojiHand.current;
    emoji.style.top = y * 100 + "%";
    emoji.style.left = x * 100 + "%";
    emoji.style.height = depth * 100 + "%";

    if (orientation === "Right") {
      emoji.style.transform = "translate(-50%, -50%) scaleX(-1)";
    } else if (orientation === "Left") {
      emoji.style.transform = "translate(-50%, -50%) scaleX(1)";
    }
  }, []);

  // using useCallback so that the function doesn't have to be defined again on rerenders
  // This function draws the detection edges, from where a swipe is registered. Uses box-shadows with transitions to simulate a highlight effect
  // whenever a direction is sent from MotionInput
  const drawThreshold = useCallback(({ x, y, sensitivity, direction}) => {

    const new_colors = {...edgeColors}
    for (const color in new_colors){
      new_colors[color] = baseColor
    }
    let elem;

    switch(direction){
      case "up":
        new_colors["top"] = highlightColor
        elem = document.getElementById("top")
        elem.parentNode.appendChild(elem)
        break;
      case "down":
        new_colors["bottom"] = highlightColor
        elem = document.getElementById("bottom")
        elem.parentNode.appendChild(elem)
        break
      case "left":
        new_colors["left"] = highlightColor
        elem = document.getElementById("left")
        elem.parentNode.appendChild(elem)
        break
      case "right":
        new_colors["right"] = highlightColor
        elem = document.getElementById("right")
        elem.parentNode.appendChild(elem)
        break;
      default:
        break
    }
    setEdgeColors(new_colors)
    setThreshold(`${Math.floor(sensitivity / 2 * 100)}%`)
  }, [edgeColors]);

  useEffect(() => {
    if (lastJsonMessage !== null && "mi_update" in lastJsonMessage.type) {
      const update_message = lastJsonMessage.type.mi_update;
      drawEmoji(update_message);
      drawThreshold(update_message);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lastJsonMessage]);


  return (
    <PreviewWindowStyle
      width={"100%"}
      aspectRatio={aspectRatio}
      bgColor="#f1f1f1"
      ref={previewWindow}
    >
      <PreviewWindowBorderTop bgColor={edgeColors.top} threshold={threshold} id="top"/>
      <PreviewWindowBorderBottom bgColor={edgeColors.bottom} threshold={threshold} id="bottom"/>
      <PreviewWindowBorderLeft bgColor={edgeColors.left} threshold={threshold} id="left"/>
      <PreviewWindowBorderRight bgColor={edgeColors.right} threshold={threshold} id="right"/>
      <EmojiHand src={emoji_left_src} height={"100%"} ref={emojiHand} />
    </PreviewWindowStyle>
  );
}

function SensitivitySlider() {
  const { lastJsonMessage, sendJsonMessage } = useContext(WebsocketContext);
  const [sliderSensitivity, setSliderSensitivity] = useState(60);
  const [showTooltip, setShowTooltip] = React.useState(false);
  const sliderRef = useRef();

  function sendSensitivityJson(val) {
    setSliderSensitivity(val);
    const sensitivity_decimal = val / 100;
    sendJsonMessage({
      type: {
        mi_config: { kiosk_swipe: { swipe_sensitivity: sensitivity_decimal } },
      },
    });
  }

  useEffect(() => {
    if (lastJsonMessage !== null && "mi_update" in lastJsonMessage.type) {
      const { sensitivity } = lastJsonMessage.type.mi_update;
      setSliderSensitivity(Math.floor(sensitivity * 100));
      sliderRef.current.value = sliderSensitivity;
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lastJsonMessage]);

  return (
    <Chakra.VStack>
      <Chakra.Slider
        ref={sliderRef}
        aria-label="slider-ex-6"
        defaultValue={sliderSensitivity}
        min={0}
        max={100}
        onChangeEnd={(val) => sendSensitivityJson(val)}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
      >
        <Chakra.SliderTrack>
          <Chakra.SliderFilledTrack />
        </Chakra.SliderTrack>
        <Chakra.Tooltip
          hasArrow
          bg="blue.500"
          color="white"
          placement="top"
          isOpen={showTooltip}
          label={`${sliderSensitivity}%`}
        >
          <Chakra.SliderThumb />
        </Chakra.Tooltip>
      </Chakra.Slider>
      <Chakra.Text>Set swipe sensitivity</Chakra.Text>
    </Chakra.VStack>
  );
}

function StatusInfo() {
  const { readyState, lastJsonMessage, sendJsonMessage } =
    useContext(WebsocketContext);

  const [motionInputConnected, setMotionInputConnected] = useState(false);

  const connectionStatus = {
    [ReadyState.CONNECTING]: "connecting",
    [ReadyState.OPEN]: "connected",
    [ReadyState.CLOSING]: "closing",
    [ReadyState.CLOSED]: "closed",
    [ReadyState.UNINSTANTIATED]: "uninstantiated",
  }[readyState];

  useEffect(() => {
    if (lastJsonMessage !== null && "mi_status" in lastJsonMessage.type) {
      // if message type is not mi_status, this will still work since
      // lastJsonMessage.type.mi_status will return undefined and trigger the else condition
      if (lastJsonMessage.type.mi_status === "disconnected") {
        console.log("disconnected");
        setMotionInputConnected(false);
      } else {
        console.log("connected");
        setMotionInputConnected(true);
      }
    }
  }, [lastJsonMessage]);

  const handleClickRelaunch = () => {
    sendJsonMessage({ type: { command: "Relaunch MotionInput" } });
  };

  return (
    <Chakra.VStack align="stretch">
      <Chakra.Alert status="info">
        <Chakra.AlertIcon />
        The WebSocket is currently {connectionStatus}
      </Chakra.Alert>
      <Chakra.Alert status="info">
        <Chakra.AlertIcon />
        MotionInput is currently{" "}
        {motionInputConnected && connectionStatus === "connected"
          ? "connected"
          : "disconnected"}
      </Chakra.Alert>
      <Chakra.Button
        variant="solid"
        colorScheme="blue"
        onClick={handleClickRelaunch}
        isLoading={readyState !== ReadyState.OPEN}
      >
        Relaunch MotionInput
      </Chakra.Button>
    </Chakra.VStack>
  );
}

export default App;
