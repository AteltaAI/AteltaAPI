import os
import json
import queue
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from ateltaapi.models.content import ContentRequest, ContentResponse
from ateltaapi.utils.pose_utils import get_angle, pose_matching_fastdtw

STUDENT_BATCH = []
INSTRUCTOR_BATCH = []

BATCHLIMIT = 6

BATCHQUEUE = queue.Queue()  # to be implemented in later versions
router = APIRouter()
ANNOTATION_PARENT_DIR = "/home/anindya/workspace/AteltaHQ/AteltaAI-labs/annotations" # This is to be provided in the configuration


@router.get("/")
async def root():
    return {"Status": 200, "Current": "evaluate/"}


# some set of assumption that are taken in the first version of batcing
# here we are assuming that, both the actor and the teacher are starting from time step 0
# which means there is no functionality that will be capture frame (from teacher) in an async manner

"""

The updated json of the videos must contain
'frame num' :{
    'keypoints' : [{}, {}, ...], 
    'angle' : [...]
}
"""


@router.post("/calculate")  # Add later: response_model=List[ContentResponse]
async def calculate(request_body: ContentRequest):
    DOING_GOOD_COUNTER = 0 # ask this thing about chatGPT in order to maintain the API standards 
    accomplishment = [
        "Great start",
        "That's some dope moves",
        "Doing great, Less goo",
    ]  # right now this is just some sample accomplishments. But this needs to be changed in future PRs.

    instructor_video_name = request_body.instructor_video
    instructor_video_path = os.path.join(ANNOTATION_PARENT_DIR, f"{instructor_video_name}.json")
    instructor_annotations = json.load(open(instructor_video_path))

    frame_num = request_body.frame_num
    frame_height, frame_width = request_body.frame_height, request_body.frame_width
    keypoints = request_body.keypoints

    keypoints_arr = np.array(list(keypoints.values())).reshape(33, 3)
    joint_angles = get_angle(keypoints_arr)

    # A very naive solution

    STUDENT_BATCH.append(joint_angles.tolist())
    INSTRUCTOR_BATCH.append(instructor_annotations[str(frame_num)]["angle"])

    if len(STUDENT_BATCH) == BATCHLIMIT:
        student_angles = STUDENT_BATCH.copy()
        instructor_angles = INSTRUCTOR_BATCH.copy()

        STUDENT_BATCH.clear()
        INSTRUCTOR_BATCH.clear()
        evaluation_match_results = pose_matching_fastdtw(
            instructor_angles=instructor_angles, 
            student_angles=student_angles
        )

        score, is_matched, node_color = list(evaluation_match_results.values())
        
        # we did not set up any optimised way to set up reward methadology. This is just some random positive and negative rewards
        if is_matched:
            DOING_GOOD_COUNTER += 1
        else:
            DOING_GOOD_COUNTER -= 10
        
        if DOING_GOOD_COUNTER < 500 and DOING_GOOD_COUNTER > 100:
            title = accomplishment[0]
        elif DOING_GOOD_COUNTER > 500:
            title = accomplishment[1]
        elif DOING_GOOD_COUNTER < 100:
            title = ""
        else:
            title = accomplishment[2]

        response = {
            "response_status": 200,
            "frame_num": frame_num,
            "score" : DOING_GOOD_COUNTER, 
            "node_color" : node_color, 
            "accomplishment": title

        }

        print(score)
        print(response)
        print("\n")

        return response
    else:
        return {
            "response_status" : 102, 
            "message": "Did not received enough number of keypoints to calcuate"
        }


if __name__ == "__main__":
    print("=> Ok")
