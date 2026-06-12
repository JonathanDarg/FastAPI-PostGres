from pydantic import BaseModel

# Add two numbers and return the result
class Numbers(BaseModel):
    a: int
    b: int

class Result(BaseModel):
    result: int


# Fist name and Last name and return the full name
class NameInput(BaseModel):
    first_name: str
    last_name: str

class NameResult(BaseModel):
    full_name: str