"""
Author: Andrzej Szablewski
Author: Rakshita Kumar
Partially based on the Head module in the MotionInput v2 code
"""

from typing import Dict, Optional, Set

import numpy as np

from scripts.core import Position
from scripts.head_module.head_biometrics import HeadBiometrics
from scripts.tools import Config


# TODO: the current methods for calculating primitives are kinda messed up :)
# TODO: should we add palm tap primitive?


class HeadPosition(Position):
    CALIBRATION = False

    def __init__(self, raw_data: Dict[str, np.ndarray],
                 used_primitives: Set[str] = None) -> None:
        self._landmarks = raw_data
        # TODO add calculating only used primitives
        self._used_primitives = used_primitives
        self._primitives = {}
        self._biometrics = {}
        self._config = Config()

        # Default calibration metrics (dev)
        self._calibration_metrics = self._config.get_data("modules/head")

        # TODO can't open file every frame - need to be changed somehow.
        #  EDIT: idea is to use config for this!
        # if self.CALIBRATION:
        #     a_file = open("scripts" + os.path.sep + "head_module" +
        #                   os.path.sep + "calibration-data.pkl", "rb")
        #     output = pickle.load(a_file)
        #     self._calibration_metrics = output

        # firstly calculate biometrics, then calculate primitives
        if self._landmarks is not None:
            self._biometrics = HeadBiometrics(self._landmarks).get_biometrics()
            self._calculate_primitives()

    def get_primitives_names(self) -> Set[str]:
        return self._used_primitives

    def get_primitive(self, name: str) -> Optional[bool]:
        """Returns the state of the given primitive in the Position if it has
         been calculated. Returns None If the primitive has not been
         calculated, hence if it either is not defined for current module
         or landmarks needed to calculate it were not provided.

        :param name: name of the primitive (e.g. "palm_facing_camera"
            or "index_pinched")
        :type name: str
        :return: state of the primitive
        :rtype: Optional[bool]
        """
        if name not in self._primitives:
            return None
        return self._primitives[name]

    def get_landmark(self, name: str) -> Optional[np.ndarray]:
        """Returns the coordinates of the landmark.
        Returns None if the landmarks was not provided to
        the Position on initialization

        :param name: name of the landmark (e.g. "index_tip" or "wrist")
        :type name: str
        :return: coordinates of the landmark
        :rtype: Optional[np.ndarray]
        """
        if name not in self._landmarks:
            return None
        return self._landmarks[name]

    def _calculate_smiling(self):
        smile_ratio = self._biometrics["mouth_width_ratio"]
        mar = self._biometrics["mar"]

        if smile_ratio >= self._calibration_metrics["smiling"] and \
                mar <= self._calibration_metrics["open_mouth"]:
            self._primitives["smiling"] = True
        else:
            self._primitives["smiling"] = False

    def _calculate_fish_face(self):
        smile_ratio = self._biometrics["mouth_width_ratio"]
        if smile_ratio <= self._calibration_metrics["fish_face"]:
            self._primitives["fish_face"] = True
        else:
            self._primitives["fish_face"] = False

    def _calculate_open_mouth(self):
        mar = self._biometrics["mar"]
        if mar >= self._calibration_metrics["open_mouth"]:
            self._primitives["open_mouth"] = True
        else:
            self._primitives["open_mouth"] = False

    def _calculate_eye_brow(self):
        eye_to_eyebrow_ratio = self._biometrics["distance_bw_eye_and_eyebrows"]
        if eye_to_eyebrow_ratio >= self._calibration_metrics["raise_eyebrow"]:
            self._primitives["raise_eye_brow"] = True
        else:
            self._primitives["raise_eye_brow"] = False

    def _calculate_eye_close(self):
        ear = self._biometrics["ear"]
        if ear <= self._calibration_metrics["eyes_close"]:
            self._primitives["eyes_close"] = True
        else:
            self._primitives["eyes_close"] = False

    def _calculate_head_rotation(self):

        leftDepth, rightDepth = self._landmarks["normalised-left-right-depths"]

        depthDelta = leftDepth - rightDepth

        turningLeft = False
        turningRight = False
        if abs(depthDelta) > self._calibration_metrics["min_rotation_delta"]:

            if depthDelta > 0:

                turningLeft = True

            else:

                turningRight = True

        self._primitives["rotate_left"] = turningLeft
        self._primitives["rotate_right"] = turningRight


    def _calculate_nose_point(self):
        self._primitives["nose_point"] = True

    def _calculate_nose_rlup(self) -> None:
        nose_position = self._landmarks["nose_point"]
        nose_box_percentage_size = self._config.get_data("events/nose_tracking/nose_box_percentage_size")
        nose_box_centre_X = self._config.get_data("events/nose_tracking/nose_box_centre_X")
        nose_box_centre_Y = self._config.get_data("events/nose_tracking/nose_box_centre_Y")

        self._primitives["nose_right"] = nose_position[0] < nose_box_centre_X - nose_box_percentage_size
        self._primitives["nose_left"] = nose_position[0] > nose_box_centre_X + nose_box_percentage_size
        self._primitives["nose_up"] = nose_position[1] < nose_box_centre_Y - nose_box_percentage_size
        self._primitives["nose_down"] = nose_position[1] > nose_box_centre_Y + nose_box_percentage_size

    def _calculate_primitives(self):

        self._calculate_smiling()
        self._calculate_fish_face()
        self._calculate_open_mouth()
        self._calculate_eye_brow()

        self._calculate_eye_close()

        self._calculate_head_rotation()

        self._calculate_nose_point()
        self._calculate_nose_rlup()
        
