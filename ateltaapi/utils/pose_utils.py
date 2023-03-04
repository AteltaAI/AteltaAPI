from typing import Any, Dict, List, Union

import numpy as np
import ateltasdk as asdk
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


def find_angle(arr: np.ndarray) -> np.ndarray:
    """Finds the angles between the pose joints
    args:
        arr : (np.ndarray) : Numpy array which must contains the [x, y, z] co-ordinates.  
    returns:
        int : angle between the single joint of the points 
    """

    radians = np.arctan2(arr[2][1] - arr[1][1], arr[2][0] - arr[1][0]) - np.arctan2(
        arr[0][1] - arr[1][1], arr[0][0] - arr[1][0]
    )
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def get_angle(keypoints: np.ndarray):
    """Gets angle of all the joints
    args:
        np.ndarray:  (np.ndarray) : Numpy array which must contains the [x, y, z] co-ordinates.
    returns:
        np.ndarray : The normalised angles between of all the provided joints 
    """

    keypoints_positions = [
        [16, 14, 12],
        [14, 12, 24],
        [12, 24, 26],
        [24, 26, 28],
        [26, 28, 32],
        [15, 13, 11],
        [13, 11, 23],
        [11, 23, 25],
        [23, 25, 27],
        [25, 27, 31],
    ]

    angles = []

    for pos in keypoints_positions:
        angles.append(find_angle(keypoints[pos]))
    return np.array(angles) / np.linalg.norm(angles)


def pose_matching_fastdtw(
    instructor_angles: Union[List[float], np.ndarray],
    student_angles: Union[List[float], np.ndarray],
    fastdtw_evaluation_threshold: float = 2.5,
) -> Dict[str, Any]:

    """Pose matching between two incoming poses using Fast Dynamic Wraping method
    args:
        instructor_angles : Union[List[float], np.ndarray] : The angles of each joint of the instructor joints 
        student_angles : Union[List[float], np.ndarray] : The angles of each joint of the student joints 
        fastdtw_evaluation_threshold : float : The threshold to check whether those poses are similar or not
    
    Here in the FastDTW algorithm, the size of the array depends on the size of window taken by the user. 
    It has been seen that, taking a window size of 5-6 provides better results and also is fast. 

    returns:
        Dict : Evaluation results which contains the following metrics:
        {
            "distance" : float, 
            "match" : bool, 
            "color" : str (green -> Pose matches and red -> Pose does't matches)
        }
    """

    if instructor_angles is None or student_angles is None:
        return {
            "distance": 0, 
            "match": True,
            "color": "white"
        }


    if type(instructor_angles) != np.array:
        instructor_angles = np.array(instructor_angles, dtype=np.float32)

    if type(student_angles) != np.ndarray:
        student_angles = np.array(student_angles, dtype=np.float32)

    distance, _ = fastdtw(instructor_angles, student_angles, dist=euclidean)
    match = distance < fastdtw_evaluation_threshold
    node_color =  "green" if match else "red"
    # might be another parameter to consider : Whether to take screen shot or not 
    return {"distance": distance, "match": match, "color": node_color}