from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="id of the patient")]
    name: Annotated[str, Field(..., description= " nameo fthe patient")]
    city: Annotated[str, Field(..., description= "city where teh patient lives")]
    age : Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['Male','Female','Others'], Field(..., description= "Gender of the patient")]
    height: Annotated[float,Field(..., gt=0, description= 'Height of the patient in mtr')]
    weight: Annotated[float, Field(..., gt=0, description= "weight of patient in kgs")]

@computed_field
@property
def bmi(self) -> float:
    bmi = round(self.weight/(self.height**2),2)
    return bmi
    
@computed_field
@property
def verdict(self) -> str:

    if self.bmi < 18.5:
        return 'Underweight'
    elif self.bmi < 25:
        return 'Normal'
    elif self.bmi < 30:
        return 'Normal'
    else:
        return 'Obese'

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data
@app.get('/')
def hello():
    return {'message':'Patient management system API'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(..., description = 'Id of the patient in the database',example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code= 404, detail= 'Patient not found')

@app.get('/sort')
def sort_patient(
    sort_by: str = Query(..., description="sort on the basis of height, weight and bmi"),
    order: str = Query("asc", description='sort in ascending or descending order')
):
    pass
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400, detail=f"invalaid field, select from {valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code= 400, detail="invalaid order select between asc and desc")

    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data= sorted(data.values(), key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data