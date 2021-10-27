from Invoice import *
from fastapi import FastAPI, File, UploadFile
import shutil
from pdf2jpg import pdf2jpg
import pytesseract as tess
from PIL import Image
import re

def pdf_img(inputpath,outputpath,fname):
    result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, dpi=300, pages="ALL")
    img = Image.open(outputpath + f"{fname}" + ".pdf_dir" + "/0_" + f"{fname}" + ".pdf.jpg")
    text = tess.image_to_string(img)
    text = text.replace(',','')
    temp = re.findall(r'[+-]?[0-9]+\.[0-9]+', text)
    return max(float(i) for i in temp)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    with open("test.pdf","wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    loc = "/home/smit/DATA SCIENCE/test.pdf"
    outputloc = "/home/smit/DATA SCIENCE/TEST FOLDER/"
    a = pdf_img(loc , outputloc,"test")
    return {"Data": a}


@app.get('/convert-pdf-2-image/{file}')
def convert(file : str):
    inputpath=file
    temp = inputpath.split('\\')
    temp = temp[len(temp) - 1]

    return{"Data":temp}


