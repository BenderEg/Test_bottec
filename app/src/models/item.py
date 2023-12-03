from pydantic import BaseModel, ConfigDict, Field

class ItemOut(BaseModel):

    model_config = ConfigDict(from_attributes=True,
                              extra='ignore')

    id: str
    name: str
    description: str
    image_path: str


class Digit(BaseModel):

    value: int = Field(ge=1)