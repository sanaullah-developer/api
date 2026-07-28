# this is just a demo code of why pydantic is used, actually we will need
# a database but i dont want to make it complex so we will just use variable

# def insert_patient_data(name,age):
#     print(name)
#     print(age)
#     print("inserted into database")

# now there is a junior programmer who can only see the signature of the function
# he does not know what the datatypes actually required are
# so he just guess it
# insert_patient_data("sanaullah","thirty")

# here in age we hope to recieve an int in age but actually we got string
# this is python particular problem and in production it can be difficutl to maintain


# but we can write it like this but this is for information purposes for another programmer to use
# this will not generate error even if we pass wrong datatypes
# def insert_patient_data1(name: str,age: int):
#     print(name)
#     print(age)
#     print("inserted into database")

#insert_patient_data1("sanaullah","thirty")

# we can also try another thing by validating the datatypes with the help of if statements like following
# and if we pass wrong datatype then it will raise error
# def insert_patient_data2(name: str,age: int):
#     if type(name)==str and type(age)==int:
#         print(name)
#         print(age)
#         print("inserted into database")
#     else:
#         raise TypeError("Incorrect data type")

#insert_patient_data2("sanaullah",30)

# we can say that this approach is good but it is not scallable because our code become very messy if we do it
# accross multiple 

# now this is type validation but we also have to do data validation
# def insert_patient_data3(name: str,age: int):
#     if age < 0:
#         raise ValueError("Age can be negative")
#     if type(name)==str and type(age)==int:
#         print(name)
#         print(age)
#         print("inserted into database")
#     else:
#         raise TypeError("Incorrect data type")

# now we can see how messy it can become and this is exactly the problem that pydantice is solving and we 
# dont have to do all of that manually



#now lets do it in pydantic

from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional, Annotated
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title= 'name of patient', description = 'give the name of the patient in less than 50 chars')]
    age: int = Field(gt=0, lt=120)  # must be > 0 and < 120
    email: EmailStr # this is custom datatype from pydantic
    weight: float =70 # 70 will be default value of weight
    married: Optional[bool] #this will make this optional
    allergies: List[str]
    contact_details: Dict[str,str]

def insert_patient_data(patient: Patient):
    print("data saved into database")

# Usage:

patient1 = Patient(
    name="sanaullah",
    age=30,
    email="abc@gmail.com",
    weight=70,
    married=False,
    allergies=["pollen", "dust"],
    contact_details={
        "phone": "03123456789",
        "city": "Peshawar"
    }
)

insert_patient_data(patient1)

# = Patient(name="sanaullah", age="thirty")  # raises ValidationError automatically