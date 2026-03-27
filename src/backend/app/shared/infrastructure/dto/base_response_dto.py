from pydantic import BaseModel


class BaseResponseDTO(BaseModel):
    code: str
    message: str
    success: bool
