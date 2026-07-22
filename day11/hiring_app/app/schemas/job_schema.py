from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    description: str
    salary: float
    company: str
    
class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    title:str | None = None
    description:str | None = None
    salary:float | None = None
    company:str | None = None
    
class JobResponse(JobBase):
    id:int
    
    class Config:
        form_attributes = True

'''
JobBase - Contains the common fields shared by all job schemas.
JobCreate - Used when creating a new job (POST /jobs).
JobUpdate - Used when updating a job (PUT or PATCH). 
All fields are optional.
JobResponse - Used when sending job details back to the client. 
Includes the generated id.

'''