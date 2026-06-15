from pydantic import BaseModel


class DSLRule(BaseModel):

    type: str

    left: str | None = None

    right: str | None = None

    value: float | int | None = None


class DSLResponse(BaseModel):

    rules: list[DSLRule]