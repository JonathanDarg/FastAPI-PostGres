from pydantic import BaseModel

# Add two numbers and return the result
class Numbers(BaseModel):
    a: int
    b: int

class Result(BaseModel):
    result: int


# First name and Last name and return the full name from different pages 
class NameInput(BaseModel):
    first_name: str
    last_name: str

class NameResult(BaseModel):
    full_name: str