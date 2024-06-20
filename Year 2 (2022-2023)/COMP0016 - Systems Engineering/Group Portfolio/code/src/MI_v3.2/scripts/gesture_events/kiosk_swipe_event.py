"""
Author: Aaryaman Sharma
Contributors: Aryan Agarwal
"""
from scripts.tools.config import Config
from scripts.tools import zeromq_client, ModeEditor
from .simple_gesture_event import SimpleGestureEvent
import json
import numpy as np

class KioskSwipeEvent(SimpleGestureEvent):
    _event_trigger_types = {"press"}
    _bodypart_types = {"hand"}

    def __init__(self):
        self._config = Config()
        self._mode_editor = ModeEditor()
        self._gesture_types = {"kiosk_swipe"}
        self._gestures = {}
        self.initialise_gestures()
        super().__init__(
            self._gesture_types,
            KioskSwipeEvent._event_trigger_types,
            KioskSwipeEvent._bodypart_types,
        )

        # Used to treat (0.5, 0.5), which is the geometric centre, as the origin rather than the
        # traditional top left. Makes calculations simpler.
        self._midpoint_coords = np.repeat(0.5, 2)

        # only start gesture when previous direction was centre
        self._prev_direction = "centre"

        # Only register click if hand is opened then closed
        self._prev_hand_closed = False

        # how far the hands needs to travel to register a swipe, on a scale of 0-1. Higher sensitivity means the hand needs to travel less to register a swipe.
        self._sensitivity = self._config.get_data("events/kiosk_swipe/swipe_sensitivity")

    def initialise_gestures(self) -> None:
        for hand in self._bodypart_types:
            self._gestures[hand] = {}
            for gesture in self._gesture_types:
                self._gestures[hand][gesture] = None

    def _receive_from_website(self):
        message = zeromq_client.receive_from_website()
        if message is None:
            return
        print(message)
        sensitivity = message.get("type", {}).get("mi_config", {}).get("kiosk_swipe", {}).get("swipe_sensitivity", None)
        if sensitivity is not None:
            self._sensitivity = float(sensitivity)
            print(self._sensitivity)

    def update(self):
        if self._state:
            self._receive_from_website()
            hand_position = self._gestures["hand"]["kiosk_swipe"].get_last_position()
            depth = hand_position.get_palm_height() * 2
            hand_closed = hand_position.get_primitive('index_folded')
            
            if hand_closed and not self._prev_hand_closed:
                self._event_triggers["press"]("enter")
            
            hand_coords = np.array(hand_position.get_landmark("middle_base"))[:-1]
            hand_orientation = "Left" if "left" in self._mode_editor.get_data("current_mode") else "Right"

            hand_position_json = json.dumps(
                {
                    "type": {
                        "mi_update": {
                            "x": hand_coords[0],
                            "y": hand_coords[1],
                            "depth": depth,
                            "sensitivity": self._sensitivity,
                            "orientation": hand_orientation,
                            "direction": self._prev_direction
                        }
                    }
                }
            )
            zeromq_client.send_to_website(hand_position_json)

            if self._check_in_centre(hand_coords):
                direction = "centre"
            else:
                direction = self._get_main_direction(hand_coords)

            # Press direction key only if hand was in the centre on the previous frame
            if self._prev_direction == "centre" and direction != "centre":
                self._event_triggers["press"](direction)

            self._prev_direction = direction
            self._prev_hand_closed = hand_closed

    def _check_in_centre(self, coords):
        # sensitivity ranges from 0-1, while the distance from midpoint ranges from 0-0.5, so we scale the threshold by dividing by 2. We also subtract by 1 initially, since threshold
        # is the opposite of sensitivity, i.e, 0 sensitivity should be 0.5 threshold, while 1 sensitivity should be 0 threshold
        threshold = (1 - self._sensitivity) / 2
        dist_from_midpoint = np.linalg.norm(coords - self._midpoint_coords)
        if dist_from_midpoint < threshold:
            return True
        return False

    def _get_main_direction(self, coords):
        direction_vector = coords - self._midpoint_coords
        # Negates y coords, so that y coordinates higher than midpoint are positive,
        # and ones lower than midpoint are negative.
        direction_vector[1] = -direction_vector[1]

        # retain the vector component with the highest absolute value, but make everything else 0.
        # Represents the direction with the largest movement.
        max_idx = np.argmax(np.abs(direction_vector))
        max_val = direction_vector[max_idx]
        direction_vector_normalized = np.zeros_like(direction_vector)
        direction_vector_normalized[max_idx] = np.sign(max_val)

        named_direction = self._named_direction_from_vector(direction_vector_normalized)

        return named_direction

    def _named_direction_from_vector(self, v):
        # order of directions corresponds to unit circle. As the we keep rotating by pi/2 radians, the arrow directions follow this order
        directions = ["right", "up", "left", "down"]

        # find the angle in radians between the direction_vector and the x axis, i.e. the angle in a unit circle
        angle = np.arctan2(*np.flip(v))

        # Finds how many times we rotated by pi/2 to get our angle. This directly corresponds to the index in the directions array, which represents consecutive pi/2 rotations
        direction_index = int(angle / (np.pi / 2))

        return directions[direction_index]

    def _check_state(self) -> None:
        self._state = self._gestures["hand"]["kiosk_swipe"] is not None
