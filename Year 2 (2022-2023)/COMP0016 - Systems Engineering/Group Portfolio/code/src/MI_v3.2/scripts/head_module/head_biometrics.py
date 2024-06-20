"""
Author: Andrzej Szablewski
Author: Rakshita Kumar
Partially based on the Head module in the MotionInput v2 code

Migrated to mediapipe landmarks by Alex Clarke for v3.11.
"""
from typing import Dict

import numpy as np

# Avoid calculating the square root wherever possible - when done for all biometrics this is costly
# Often the actual distance is not needed - just the ratio between two distances.
def getSquaredDistance(distanceVector):
    return (distanceVector[0]**2 + distanceVector[1]**2)


# HeadBiometrics takes a Dictionary of landmark names
# and corresponding vectors and calculates biometrics.
# Made outside the head_position, so that all functions can be
# easily reached for the calibration code
class HeadBiometrics:
    def __init__(self, landmarks: Dict[str, np.ndarray]):
        """Initializes HeadBiometrics instance and calculates all biometrics.

        :param landmarks: dictionary containing landmarks names
            mapped to their coords
        :type landmarks: Dict[str, numpy.ndarray]
        """
        self._landmarks = landmarks
        self._biometrics = {}

        if self._landmarks is not None:
            self._calculate_biometrics()

    def _eye_aspect_ratio(self, eye: [str]) -> float:
        """Returns Eye Aspect Ratio given eye landmarks.
        Taken from: https://github.com/acl21/Mouse_Cursor_Control_Handsfree

        :param eye: array containing all landmarks for the given eye
        :type eye: numpy.ndarray
        :return: Eye Aspect Ratio (EAR)
        :rtype: float
        """
        a = getSquaredDistance(self._landmarks[eye[2]] - self._landmarks[eye[3]])
        b = getSquaredDistance(self._landmarks[eye[4]] - self._landmarks[eye[5]])
        c = getSquaredDistance(self._landmarks[eye[0]] - self._landmarks[eye[1]])

        ear = (a + b) / (2 * c)

        return ear

    def _add_jaw_mouth_width_ratio(self) -> None:
        """Calculates jaw width and mouth width ratio and store them
            in _biometrics dictionary.
        """
        jaw_width = getSquaredDistance(self._landmarks["left-cheek"] - self._landmarks["right-cheek"])
        mouth_width = getSquaredDistance(self._landmarks["lip-left"] - self._landmarks["lip-right"])

        mouth_width_ratio = mouth_width / jaw_width

        self._biometrics["jaw_width"] = jaw_width
        self._biometrics["mouth_width"] = mouth_width

        self._biometrics["mouth_width_ratio"] = mouth_width_ratio

    def _add_mar(self) -> None:
        """Calculates MAR value and stores it in _biometrics dictionary. 
        Taken from: https://github.com/acl21/Mouse_Cursor_Control_Handsfree

        Compare height and width of the mouth using various landmarks
        """

        leftHeight = getSquaredDistance(self._landmarks["lip-top-left"] - self._landmarks["lip-bottom-right"])
        centreHeight = getSquaredDistance(self._landmarks["lip-top"] - self._landmarks["lip-bottom"])
        rightHeight = getSquaredDistance(self._landmarks["lip-top-right"] - self._landmarks["lip-bottom-right"])

        mar = (leftHeight + centreHeight + rightHeight) / (2 * self._biometrics["mouth_width"])

        self._biometrics["mar"] = mar

    def _add_left_and_right_eye_brow_distance(self) -> None:
        """Calculates mean distance between eye and eyebrow
            (and normalizes it using jaw_width).
        The result is stored in the _biometrics dictionary.
        """
        left_eye_to_left_eyebrow_distance = (
            getSquaredDistance(self._landmarks["left-eyebrow-top-left"] - self._landmarks["left-eye-top-left"]) +
            getSquaredDistance(self._landmarks["left-eyebrow-top-right"] - self._landmarks["left-eye-top-right"])
        ) / 2

        right_eye_to_right_eyebrow_distance = (
            getSquaredDistance(self._landmarks["right-eyebrow-top-left"] - self._landmarks["right-eye-top-left"]) +
            getSquaredDistance(self._landmarks["right-eyebrow-top-right"] - self._landmarks["right-eye-top-right"])
        ) / 2

        jaw_width = self._biometrics["jaw_width"]
        left_eye_to_left_eyebrow_distance /= jaw_width
        right_eye_to_right_eyebrow_distance /= jaw_width

        mean_distance_bw_eye_and_eyebrows = np.mean(
            [left_eye_to_left_eyebrow_distance,
             right_eye_to_right_eyebrow_distance]
        )

        self._biometrics["distance_bw_eye_and_eyebrows"] = mean_distance_bw_eye_and_eyebrows

    def _add_ear(self) -> None:
        """Calculates EAR value and stores it in _biometrics dictionary. """

        # Flipped frame
        ear = np.mean([self._eye_aspect_ratio(["left-eye-left", "left-eye-right", "left-eye-top-left", "left-eye-bottom-left", "left-eye-top-right", "left-eye-bottom-right"]),
                       self._eye_aspect_ratio(["right-eye-left", "right-eye-right", "right-eye-top-left", "right-eye-bottom-left", "right-eye-top-right", "right-eye-bottom-right"])])

        self._biometrics["ear"] = ear



    def _add_head_turn_ratio(self) -> None:
        """Calculates head turn ratio and stores it in _biometrics dictionary.
         <1 - head turned left
         >1 - head turned right.
        """
        # Euclidean distance between nose tip and left cheek:
        point_distance_left = getSquaredDistance(
            self._landmarks["nose-tip"] - self._landmarks["left-cheek"]
        )
        # Euclidean distance between nose tip and right cheek:
        point_distance_right = getSquaredDistance(
            self._landmarks["nose-tip"] - self._landmarks["right-cheek"]
        )

        head_turn_ratio = point_distance_left / point_distance_right

        self._biometrics["head_turn_ratio"] = head_turn_ratio


    def _calculate_biometrics(self) -> None:
        
        """Calculates all head biometrics sequentially. """

        self._add_jaw_mouth_width_ratio()
        self._add_mar()
        self._add_left_and_right_eye_brow_distance()
        self._add_ear()
        self._add_head_turn_ratio()

    def get_biometrics(self) -> Dict[str, float]:
        """Returns dictionary containing calculated biometrics.

        :return: dictionary containing biometrics names mapped to
            calculated values
        :rtype: Dict[str, float]
        """

        return self._biometrics
