from pydantic import BaseModel

class ThreadDeleteResponse(BaseModel):
    message: str
    status: bool
    status_code: int
    payload: dict
