from scripts.core import Module

from .head_gesture import HeadGesture
from .head_landmark_detector import HeadLandmarkDetector
from .head_position import HeadPosition


class HeadModule(Module):
    _position_class = HeadPosition
    _gesture_class = HeadGesture
    _landmark_detector_class = HeadLandmarkDetector

    _tracker_names = {"head"}
