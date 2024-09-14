from roboflow import Roboflow
from dotenv import load_dotenv
import os
import requests
from pprint import pprint 
import cv2
from pathlib import Path
from typing import Union, List

load_dotenv()
API_KEY = os.environ.get('ROBOFLOW_API_KEY')
print(API_KEY)


def get_drug_info(query):
    url = f"https://drugapi.p.rapidapi.com/Drug/Summary/{query}"

    headers = {
    	"x-rapidapi-key": "5d53f0c48bmsh7b773967c027048p1e9882jsn9dd54bf50d87",
    	"x-rapidapi-host": "drugapi.p.rapidapi.com"
    }


    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        pprint(data)
    else:
        print(f"Request for drug info failed with status code {response.status_code}")

# 
def predict_pill(img_path_or_url):
    rf = Roboflow(api_key=API_KEY)
    project = rf.workspace().project("pill-recognition-oxvel")
    model = project.version(1).model
    if model is None:
        print("Model failed to load.")
    else:
        print("Model loaded successfully.")

    print(f"Model: {model}")
    print(f"Image Path: {img_path_or_url}")
    # infer on an image hosted elsewhere
    if model:
        result = model.predict(image_path=img_path_or_url, confidence=40, overlap=30).json()
        result.update({"info": get_drug_info(result['predictions'][0]['class'])})
    else:
        print("Model is None, cannot predict.")
    return None



def image_with_bboxes(frame: Union[Path, cv2.Mat], face_data: List[dict]) -> cv2.Mat:
    if isinstance(frame, Path):
        image = cv2.imread(str(frame))
    elif isinstance(frame, cv2.Mat):
        image = frame.copy()
    else:
        raise TypeError('frame type must be Path or cv2.Mat Object')

    boxes = [face['bbox'].values() for face in face_data]
    for (left, top, right, bottom) in boxes:
        cv2.rectangle(image, (left, top), (right, bottom), (0,255,0), 2)

    return image

pprint(predict_pill("PharmaVision-master\\uploads\\eliquis.jpg"), indent=4)
