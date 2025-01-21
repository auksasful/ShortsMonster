from typing_extensions import TypedDict




class Scene(TypedDict):
    Scene: str
    Duration: int
    Text: str
    Visuals: str
    Hashtags: str
    Description: str

class Videos(TypedDict):
    Video: int
    Scenes: list[Scene]