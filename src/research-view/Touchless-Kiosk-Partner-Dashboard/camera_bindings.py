"""Class to take the tracker listener from and determine the pinching status and the palm position. Start with:
\n
\n
\nimport pinching_at_location_example
\nfrom pinching_at_location_example import MyListener as Listener
\nimport leap
\n
\n
to reference this file.
"""

# this is gonna be a combination of both the pinching and the tracking palm example

import time
import leap
from leap import datatypes as ldt


def location_end_of_finger(hand: ldt.Hand, digit_idx: int) -> ldt.Vector:
    digit = hand.digits[digit_idx]
    return digit.distal.next_joint


def sub_vectors(v1: ldt.Vector, v2: ldt.Vector) -> list:
    return map(float.__sub__, v1, v2)


def fingers_pinching(thumb: ldt.Vector, index: ldt.Vector):
    diff = list(map(abs, sub_vectors(thumb, index)))

    if diff[0] < 20 and diff[1] < 20 and diff[2] < 20:
        return True, diff
    else:
        return False, diff


# class PinchingListener(leap.Listener):
#     def on_tracking_event(self, event):
#         if event.tracking_frame_id % 50 == 0:
#             for hand in event.hands:
#                 hand_type = "Left" if str(hand.type) == "HandType.Left" else "Right"

#                 thumb = location_end_of_finger(hand, 0)
#                 index = location_end_of_finger(hand, 1)

#                 pinching, array = fingers_pinching(thumb, index)
#                 pinching_str = "not pinching" if not pinching else "" + str("pinching")
#                 print(
#                     f"{hand_type} hand thumb and index {pinching_str} with position diff ({array[0]}, {array[1]}, {array[2]})."
#                 )


class MyListener(leap.Listener):
    previous_pinching_status = None
    palm_x = None
    palm_y = None
    palm_z = None
    current_pinching_status = False
    new_hand_type = "none"
    new_thumb = None
    new_index = None
    new_tracking_frame_id = None
    new_tracking_frame_id_synced = None
    tracking_frame_size = None

    def __init__(self):
        self.previous_pinching_status = None
        self.palm_x = 0
        self.palm_y = 0
        self.palm_z = 0
        self.new_thumb = None
        self.new_index = None
        self.new_tracking_frame_id = 0
        self.new_tracking_frame_id_synced = 0
        self.tracking_frame_size = 10


    def test_func(self):
        """Prints out something if you've done eveything right."""
        print("tested!! \n\n\n")
    
    def get_hand_type(self):
        """Returns 'left' or 'right' as last tracked hand type."""
        return 

    def get_palm_position(self) -> "tuple[float, float, float]":
        """Returns the x, y, z coordinates of the currently tracked palm (if there is one)
        \nx -> Left/Right
        \ny -> Close/Far
        \nz -> Up/Down"""
        return(self.palm_x, self.palm_y, self.palm_z)

    def is_pinching(self) -> bool:
        """Returns bool on whether the currently tracked hand is detected to be pinching (or not)."""
        return(self.current_pinching_status)
    
    def get_pinching_vectors(self) -> "tuple[float, float, float]":       # thumb: ldt.Vector, index: ldt.Vector):
        """Returns the difference between the x, y, z axes of the index and the thumb. Use for dragging, zooming, etc."""
        if self.new_index is not None and self.new_thumb is not None:
            diff = list(map(abs, sub_vectors(self.new_thumb, self.new_index)))
            return(diff[0], diff[1], diff[2])
        else:
            return(0, 0, 0)
        
    def get_tracking_frame_id(self) -> int:
        """Returns the current tracking frame ID."""
        return self.new_tracking_frame_id
    
    def get_tracking_frame_id_synced(self) -> int:
        """Returns the current tracking frame ID synced with the tracking frames."""
        return self.new_tracking_frame_id_synced

    def set_tracking_frame_size(self, frame_size: int):
        """Sets the tracking frame size. Smaller ints (>1) mean more granular tracking. Defined as the number of frames between each tracking update."""
        if frame_size >= 1:
            self.tracking_frame_size = round(frame_size)
    
    def get_tracking_frame_size(self) -> int:
        """Returns the tracking frame size. Defined as the number of frames between each tracking update."""
        return self.tracking_frame_size

    # -------------------------------------------------- #

    def on_connection_event(self, event):
        print("Connected")

    def on_device_event(self, event):
        try:
            with event.device.open():
                info = event.device.get_info()
        except leap.LeapCannotOpenDeviceError:
            info = event.device.get_info()

        print(f"Found device {info.serial}")

    def on_tracking_event(self, event): # pincher tracking thing integrated here
        # print(f"Frame {event.tracking_frame_id} with {len(event.hands)} hands.")
        # print("test")
        self.new_tracking_frame_id = event.tracking_frame_id
        if event.tracking_frame_id % self.tracking_frame_size == 0: # maybe set with variable?
            self.new_tracking_frame_id_synced = event.tracking_frame_id
            for hand in event.hands:
                self.palm_x, self.palm_y, self.palm_z = hand.palm.position.x, hand.palm.position.y, hand.palm.position.z # mention this in presentation
                # print(self.palm_x, self.palm_y, self.palm_z)
                hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
                self.new_hand_type = hand_type
                # print(
                #     f"Hand id {hand.id} is a {hand_type} hand with position ({hand.palm.position.x}, {hand.palm.position.y}, {hand.palm.position.z})."
                # )

                thumb = location_end_of_finger(hand, 0)
                index = location_end_of_finger(hand, 1)

                self.new_thumb = thumb
                self.new_index = index

                pinching, array = fingers_pinching(thumb, index)

                self.current_pinching_status = pinching
                
                if self.previous_pinching_status != pinching :
                    pinching_str = "not pinching" if not pinching else "" + str("pinching")
                    # print(f"{hand_type} at ({hand.palm.position.x}, {hand.palm.position.y}, {hand.palm.position.z}); hand.thumb + index {pinching_str} position diff ({array[0]}, {array[1]}, {array[2]}).")
                    self.previous_pinching_status = pinching

        
        # pincher tracking here
        # if event.tracking_frame_id % 50 == 0:
        #     # print("test")
        #     for hand in event.hands:
        #         hand_type = "Left" if str(hand.type) == "HandType.Left" else "Right"

                # thumb = location_end_of_finger(hand, 0)
                # index = location_end_of_finger(hand, 1)

                # pinching, array = fingers_pinching(thumb, index)
                # pinching_str = "not pinching" if not pinching else "" + str("pinching")
                # print(f"{hand_type} hand thumb and index {pinching_str} with position diff ({array[0]}, {array[1]}, {array[2]}).")


def main():

    position_listener = MyListener()

    connection = leap.Connection()
    connection.add_listener(position_listener)

    with connection.open():
        while True:
            time.sleep(1)



if __name__ == "__main__":
    main()