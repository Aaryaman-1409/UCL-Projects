'''


Author: Carmen Meinson
'''

from typing import Type, Set, Optional

from .position import Position
from .raw_data import RawData


# tracks the positions of 1 body part throughout the frames
# notifies (through the model) necessary gesture factory instances whenever a primitive changes.

class PositionTracker:
    def __init__(self, name: str, position_class: Type[Position]) -> None:
        self._name = name  # name of the specific body part (eg Left/Right)
        self._current_position = None
        self._position_class = position_class

    def update(self, raw_data: RawData, used_primitives: Set[str] = None) -> Set[str]:
        """Creates a Position instance out of the provided RawData and compares the state of all the primitives to the previous Position. Returns the list of all the changed primitives.
        If there was no previous position (so if it is the first update() call or if the tracker has been reset) all primitives are considered to have changed.

        If used_primitives is not None the Position class may only calculate the primitives given. If it is None all primitives are calculated

        :param raw_data: RawData instance containing all the landmarks coordinates detected in the frame
        :type raw_data: RawData
        :param used_primitives: names of all the primitives that are currently used by the module
        :type used_primitives: Set[str]
        :return: set of changed primitives since the last update() call
        :rtype: Set[str]
        """
        raw_hand_data = raw_data.get_data(self._name)
        new_position = self._position_class(raw_hand_data, used_primitives)
        changed_primitives = self._compare_primitives(new_position)

        self._current_position = new_position
        return changed_primitives

    def get_name(self) -> str:
        """returns the name of the tracker thus also reflecting the name of the body part"""
        return self._name

    def get_current_position(self) -> Optional[Position]:
        """Returns the Position instance generated by the last update() call.
        If there has been no such call or if the tracker has been reset returns None

        :return: last Position instance
        :rtype: Optional[Position]
        """
        return self._current_position

    def reset(self) -> Set[str]:
        """Resets the Tracker instance to the initial state and returns all the changed primitives in doing so.
        Thus the current position is again None and by default all primitives are considered to have changed (unless the tracker was already in the reset state, in which case none of the primitives are considered to have changed)

        :return: set of changed primitives
        :rtype: Set[str]
        """
        changed_primitives = self._compare_primitives(None)
        self._current_position = None
        return changed_primitives

    def _compare_primitives(self, new_position: Position) -> Set[str]:
        if self._current_position is None and new_position is None: return set()
        # if just came into frame or left the frame then all primitives are considered to have changed
        if self._current_position is None: return new_position.get_primitives_names()
        if new_position is None: return self._current_position.get_primitives_names()

        changed_primitives = set()
        primitives_used_in_both = new_position.get_primitives_names() & self._current_position.get_primitives_names()
        for prim_name in primitives_used_in_both:
            # if the primitive changed since last frame
            if new_position.get_primitive(prim_name) != self._current_position.get_primitive(prim_name):
                changed_primitives.add(prim_name)

        # primitives only used by 1 of the position instances (e.g. happend when gestures had been added/removed) are changed by default
        primitives_used_in_one = (
                                             new_position.get_primitives_names() | self._current_position.get_primitives_names()) - primitives_used_in_both
        return changed_primitives | primitives_used_in_one
