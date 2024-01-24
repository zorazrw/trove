# %% Import PIL.Image
from PIL import Image


# %% Locate object bounding boxes in the image
import requests
from PIL import Image

def locate_objects(image: str | Image.Image, object_name: str) -> list:
    """Load object bounding boxes in the image.
    Args:
        image: str, file name of the image
        object: str, natural language description of the object
    Rets:
        selected_boxes: box regions of the found object(s)
    """
    params = {"object_name": object_name}

    if not isinstance(image, str):
        image.save("tmp.jpg")
        params["image_name"] = "tmp.jpg"
    else:
        params["image_name"] = image

    r = requests.get(
        "http://127.0.0.1:8000/loc", params=params
    )
    return r.json()["boxes"] 


# %% Answering basic visual question with neural models
import requests
from PIL import Image

def visual_qa(image: str | Image.Image, question: str) -> str:
    """Answering basic visual question with neural models.
    Args:
        image: str, file name of the image
        question: str, question about the image
    Rets:
        answer: str, model response to the question
    """
    params = {"question": question}

    if not isinstance(image, str):
        image.save("tmp.jpg")
        params["image_name"] = "tmp.jpg"
    else:
        params["image_name"] = image

    r = requests.get("http://127.0.0.1:8000/vqa", params=params)
    return r.json()["answer"]


# %% Crop the specified box region from the image
import PIL
def crop_region(image: PIL.Image, boxes: list) -> PIL.Image:
    """Crop the specified box region from the image
    Args:
        image: PIL.Image object, contains pixel values of the image
        box: list, boxes of segmented regions
    Rets:
        cropped_image: PIL.Image object, cropped image
    """
    if len(boxes) > 0:
        box = boxes[0]
        
        W,H = image.size
        factor = 1.5
        x1,y1,x2,y2 = box
        dw = int(factor*(x2-x1)/2)
        dh = int(factor*(y2-y1)/2)
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        x1 = max(0,cx - dw)
        x2 = min(cx + dw,W)
        y1 = max(0,cy - dh)
        y2 = min(cy + dh,H)
        box = [x1,y1,x2,y2]

        cropped_image = image.crop(box)
    else:
        cropped_image = image
    return cropped_image

