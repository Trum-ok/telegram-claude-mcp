from pydantic import BaseModel as PydanticBase


class BaseModel(PydanticBase):
    pass


class OkResponseSchema[T](BaseModel):
    status: str
    data: T


class ErrorResponseSchema[T](BaseModel):
    status: str
    message: str
    data: T
