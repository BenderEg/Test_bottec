from pydantic import BaseModel, ConfigDict

class ItemOut(BaseModel):

    model_config = ConfigDict(from_attributes=True,
                              extra='ignore')

    id: str
    name: str
    description: str
    image_path: str
