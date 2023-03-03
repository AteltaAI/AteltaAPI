from datetime import datetime
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, List, Optional, Union, List, Dict


class ContentRequest(BaseModel):
    """This is the basemodel for the all the incoming API requests"""

    instructor_video : str = Field(default='default', title="The name of the video that the user has chosen ti yu")
    frame_num: int = Field(default=None, title="The name of the frame")
    #contains_result: bool = Field(..., title="Whether the request contains pose results or not")
    frame_height: int
    frame_width: int
    keypoints: Union[None, Dict[str, List[float]]] = Field(
        ..., title="keypoints of the pose for a particular frame recieved from the webcam side"
    )

class ContentResponse(BaseModel):
    """Basemodel for the API response for a particular request"""
    response_status : int 
    frame_num : int 
    score : int 
    node_color : str 
    accomplishment : str 