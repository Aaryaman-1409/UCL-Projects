"""
Author: Radu-Bogdan Priboi
Contributors: Andrzej Szablewski
"""
from scripts.tools import Config
from .simple_gesture_event import SimpleGestureEvent


class MouthTriggerEvent(SimpleGestureEvent):
    """
    Left Clicking/Pressing when mouth is opened. Currently as there is no
    logic of how to decide if a press or a click should be started.
    Right Clicking is triggers by smiling and Double Clicking by
    raising eyebrows.

    [trigger types]:
        “click”: called once when the gesture of interest becomes active;
        “press”: called when the gesture of interest becomes
                 active IF the “click” trigger type was not defined;
        “release”: called when the gesture of interest becomes unactive
    [bodypart types]:
        "head"
    [gestures types]:
        "smiling_gesture" & "open_mouth_gesture" & "raise_eye_brow_gesture"
    """
    _event_trigger_types = {"click", "press", "release"}
    _bodypart_types = {"head"}

    def __init__(self, gesture_types) -> None:
        super().__init__(gesture_types,
                         MouthTriggerEvent._event_trigger_types,
                         MouthTriggerEvent._bodypart_types)
        self._click_held = False
        config = Config()
        self._frames_for_press = config.get_data(
            "events/mouth_events/frames_for_press")
        self.trigger_count = config.get_data(
            "events/mouth_events/trigger_count")
        self.current_count = 0
        self._already_triggered = False
        if len(self._gesture_types) != 1:
            raise RuntimeError(
                "invalid _gesture_types given to "
                "the child class of the MouthTriggerEvent")
        self._gesture_type = next(iter(self._gesture_types))

    def _check_state(self) -> None:
        self._state = (
            self._gestures["head"][self._gesture_type] is not None
        ) or self._click_held

    def update(self):
        if self._state and not self._click_held:
            self.current_count = self.current_count + 1
            if self.current_count == self.trigger_count:
                self._click_held = True
                # trigger the click
                if self._event_triggers["click"] is not None:
                    self._event_triggers["click"]()  # TODO: PRESS&CLICK LOGIC
                elif self._event_triggers["press"] is not None:
                    self._event_triggers["press"]()
        if self._click_held:
            if self._gestures["head"][self._gesture_type] is None:
                self._click_held = False
                self._state = False
                self.current_count = 0
                if self._event_triggers["release"] is not None:
                    self._event_triggers["release"]()


class SmilingEvent(MouthTriggerEvent):
    _gesture_types = {"smiling_gesture"}

    def __init__(self, key=None) -> None:
        self._key = key
        self._gestures = {"head": {"smiling_gesture": None}}
        super().__init__(SmilingEvent._gesture_types)


class FishFaceEvent(MouthTriggerEvent):
    _gesture_types = {"fish_face_gesture"}

    def __init__(self, key=None) -> None:
        self._key = key
        self._gestures = {"head": {"fish_face_gesture": None}}
        super().__init__(FishFaceEvent._gesture_types)


class OpenMouthEvent(MouthTriggerEvent):
    _gesture_types = {"open_mouth_gesture"}

    def __init__(self, key=None) -> None:
        self._key = key
        self._gestures = {"head": {"open_mouth_gesture": None}}
        super().__init__(OpenMouthEvent._gesture_types)


class RaiseEyeBrowEvent(MouthTriggerEvent):
    _gesture_types = {"raise_eye_brow_gesture"}

    def __init__(self, key=None) -> None:
        self._key = key
        self._gestures = {"head": {"raise_eye_brow_gesture": None}}
        super().__init__(RaiseEyeBrowEvent._gesture_types)


class FishFaceEvent(MouthTriggerEvent):
    _gesture_types = {"fish_face_gesture"}

    def __init__(self, key=None) -> None:
        self._key = key
        self._gestures = {"head": {"fish_face_gesture": None}}
        super().__init__(FishFaceEvent._gesture_types)

class RotationLeftEvent(MouthTriggerEvent):
    _gesture_types = {"left_rotation_gesture"}

    def __init__(self, key=None) -> None:
        self._key = key
        self._gestures = {"head": {"left_rotation_gesture": None}}
        super().__init__(RotationLeftEvent._gesture_types)

class RotationRightEvent(MouthTriggerEvent):
    _gesture_types = {"right_rotation_gesture"}

    def __init__(self, key=None) -> None:
        self._key = key
        self._gestures = {"head": {"right_rotation_gesture": None}}
        super().__init__(RotationRightEvent._gesture_types)