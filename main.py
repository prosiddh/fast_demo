from fastapi import FastAPI, File, UploadFile, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Set up templates directory
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploadfile/")
async def upload_file(id: str = Form(...), files: list[UploadFile] = File(...)):
    os.makedirs("temp_files", exist_ok=True)
    file_info_list = []

    for file in files:
        try:
            file_info = await process_file(file, id)
            file_info_list.append(file_info)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": str(e.detail)})

    return file_info_list

async def process_file(file: UploadFile, id: str):
    unique_filename = f"{id}_{file.filename}"
    file_location = os.path.join("temp_files", unique_filename)

    try:
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        print(f"File Saved : {file_location}")

        # Static JSON for testing purposes
        result = await static_response(file_location)
        os.remove(file_location)

        # Return the static result directly
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file {file.filename}: {str(e)}")

async def static_response(file_location: str):
    file_id = file_location[file_location.rfind('\\')+1:file_location.rfind('.')]
    
    # Static JSON response
    static_response = [
        {
            "file_id": file_id,
            "file_data": {
                "patient_details": [
                    {
                        "Patient Name": "MEHUL PARMAR",
                        "Age": "442 Years",
                        "Sex": "Male",
                        "Report Date": "07/02/2024"
                    }
                ],
                "tests": [
                    {
                        "testname": "CHOLESTEROL",
                        "value": "310.23 mg/ai",
                        "range": "High > 2400\nNormal , 150.0"
                    },
                    {
                        "testname": "TRIGLYCERIDE",
                        "value": "385.99 mg/dl",
                        "range": "Boderline High 151.0-199.0\nHigh 2000-499.0\nVery High > 500.0"
                    },
                    {
                        "testname": "HDL-CHOLESTEROL",
                        "value": "52.00 mg/di",
                        "range": "Near Optimal 40.0-60.0\nOptimal > 60.0\nLow < 40.0"
                    },
                    {
                        "testname": "VLDL:-CHOLESTEROL",
                        "value": "77.19 mg/di",
                        "range": "10 s 40\n(Calculated)"
                    },
                    {
                        "testname": "LDL CHOLESTEROL",
                        "value": "181.04 mg/dl",
                        "range": "Optimal <100.0\nNear Optimal : 100.0-1290\n(Calculated)\nBoderline High 130.0-159.0\nHigh > 160.0"
                    },
                    {
                        "testname": "MDLAHDL RATIO",
                        "value": "3.48",
                        "range": "UPTO3.2"
                    },
                    {
                        "testname": "CHOLHDL RATIO",
                        "value": "5.96",
                        "range": "UPTO 5.0"
                    }
                ]
            }
        },
        {
            "file_id": "4554_test_img_1",
            "file_data": {
                "Patient Details": [
                    {
                        "Name": "MRS. HEMLATABEN NITINBHAI D",
                        "Age": "50Y8 8M 6D",
                        "Sex": "Female",
                        "Report Date": "Mar 30 2024"
                    }
                ],
                "Tests": [
                    {
                        "testname": "RAI FACTORLatex agglutination)",
                        "value": "NEGATIVE",
                        "range": "<8",
                        "units": "IU/ml"
                    },
                    {
                        "testname": "CRP (C-REACTIVE PROTEIN)",
                        "value": "NEGATIVE",
                        "range": "<6",
                        "units": "mg/l (Turbidimetric)"
                    },
                    {
                        "testname": "NA",
                        "value": "NA",
                        "range": "NA",
                        "units": "NA"
                    }
                ]
            }
        }
    ]
    
    return static_response[0]  # Return the first static entry for simplicity

