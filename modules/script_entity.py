from typing_extensions import TypedDict




class Scene(TypedDict):
    # Duration: int
    What_Speaker_Says_In_First_Person: str
    Visuals: str
    # Hashtags: str
    # Description: str

class Videos(TypedDict):
    Video: int
    Scenes: list[Scene]