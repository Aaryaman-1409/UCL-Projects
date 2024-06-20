"""
Author: Alex Clarke

Migration to mediapipe facial mesh ML model for MotionInput 3.12.
https://google.github.io/mediapipe/solutions/face_mesh

Prior dlib landmark detector implemented by Andrzej Szablewski and Rakshita Kumar.
"""

import os

import cv2
import mediapipe as mp
import numpy as np

from numpy import ndarray

from scripts.core import LandmarkDetector
from scripts.core import RawData
from scripts.tools import Config

# Unfortunately, no convenient definitions for the mediapipe face mesh vertices
EXPORTED_LANDMARKS = {"nose-tip": 4,
    "left-eyebrow-top-left": 63, "left-eyebrow-top-right": 66,
    "left-eye-top-left": 160, "left-eye-top-right": 158,
    "left-eye-left": 33, "left-eye-right": 173,
    "left-eye-bottom-left": 144, "left-eye-bottom-right": 153,
    "right-eyebrow-top-left": 296, "right-eyebrow-top-right": 293,
    "right-eye-top-left": 385, "right-eye-top-right": 387,
    "right-eye-left": 398, "right-eye-right": 263,
    "right-eye-bottom-left": 380, "right-eye-bottom-right": 373,
    "lip-top": 13, "lip-bottom": 14, "lip-left": 78, "lip-right": 308,
    "lip-top-left": 81, "lip-bottom-left": 178, "lip-top-right": 311, "lip-bottom-right": 402,
    "left-cheek": 132, "right-cheek": 361 }

class HeadLandmarkDetector(LandmarkDetector):

    def __init__(self) -> None:

        # initialize camera size
        config = Config()

        self.tracker = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            refine_landmarks=False,
            min_detection_confidence=config.get_data("modules/head/min_detection_confidence"),
            min_tracking_confidence=config.get_data("modules/head/min_tracking_confidence"),
            max_num_faces=config.get_data("modules/head/max_face_count")
        )

    def _add_normalized_nose_point(self, raw_data: RawData, landmarks: dict) -> None:
        
        raw_data.add_landmark(
            "head",
            "nose_point",
            landmarks["nose-tip"]
        )

    def _process_frame(self, frame: np.ndarray) -> tuple:

        # Prepare image array for mediapipe model.
        # See mediapipe demo on their website, setting writeable flags improves performance

        frame.flags.writeable = False

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.tracker.process(frame)

        frame.flags.writeable = True

        # Extract landmarks from mediapipe datatypes
        faces = []

        if results.multi_face_landmarks:

            # For efficiency, and the sake of integrating with existing code,
            # compute the depth-based parameters here, and then chuck the z component away.
            # "normalised-left-right-depths" is not really a landmark, but is needed to calculate head rotation
            for face_landmarks in results.multi_face_landmarks:

                depths = {"left": [], "right": [], "all": []}
                face = {}
                for lm_name, lm_index in EXPORTED_LANDMARKS.items():
                    
                    landmark = face_landmarks.landmark[lm_index]
                    face[lm_name] = np.array([landmark.x, landmark.y])

                    if lm_name.startswith("left"):
                        depths["left"].append(landmark.z)

                    elif lm_name.startswith("right"):
                        depths["right"].append(landmark.z)

                    depths["all"].append(landmark.z)


                avgDepth = sum(depths["all"]) / len(depths["all"])

                leftDepth = sum(depths["left"]) / len(depths["left"])
                rightDepth = sum(depths["right"]) / len(depths["right"])

                leftDepth -= avgDepth
                rightDepth -= avgDepth

                face["normalised-left-right-depths"] = np.array([leftDepth, rightDepth])

                faces.append(face)

        return frame, faces

    def get_raw_data(self, raw_data: RawData, image: ndarray) -> None:

        processed_image, tracked_faces = self._process_frame(image)

       
        if len(tracked_faces) > 0:

            landmarks = tracked_faces[0]  # The rest of this module currently expects just one tracked face

            # Add useful landmarks to raw_data, using their names as the key field
            for lm_name, lm_pos in landmarks.items():

                raw_data.add_landmark("head", lm_name, lm_pos)

            self._add_normalized_nose_point(raw_data, landmarks)