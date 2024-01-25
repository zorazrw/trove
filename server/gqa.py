from fastapi import FastAPI
app = FastAPI()

# %% Utilities

from PIL import Image
def load_image(image_name: str):
    # image_path = os.path.join("data", "gqa", "testdev_images", image_name)
    return Image.open(image_name)


def load_hf_model(hf_name: str, processor_class, model_class) -> tuple:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = processor_class.from_pretrained(hf_name)
    model = model_class.from_pretrained(hf_name).to(device)
    model.eval()
    return (model, processor)


# Non-max Suppression Algorithm.
import numpy as np
def nms(bounding_boxes: list[list[float]], confidence_score: list[float], threshold: float) -> tuple[list[list[float]], list[float]]:
    """Non-max Suppression Algorithm.
    Args:
        bounding_boxes: list, Object candidate bounding boxes
        confidence_score: list[float], Confidence score of bounding boxes
        threshold: float, IoU threshold
    Rets:
        Rest boxes after nms operation
    """
    # If no bounding boxes, return empty list
    if len(bounding_boxes) == 0:
        return [], []

    # Bounding boxes
    boxes = np.array(bounding_boxes)

    # coordinates of bounding boxes
    start_x = boxes[:, 0]
    start_y = boxes[:, 1]
    end_x = boxes[:, 2]
    end_y = boxes[:, 3]

    # Confidence scores of bounding boxes
    score = np.array(confidence_score)

    # Picked bounding boxes
    picked_boxes = []
    picked_score = []

    # Compute areas of bounding boxes
    areas = (end_x - start_x + 1) * (end_y - start_y + 1)

    # Sort by confidence score of bounding boxes
    order = np.argsort(score)

    # Iterate bounding boxes
    while order.size > 0:
        # The index of largest confidence score
        index = order[-1]

        # Pick the bounding box with largest confidence score
        picked_boxes.append(bounding_boxes[index])
        picked_score.append(confidence_score[index])

        # Compute ordinates of intersection-over-union(IOU)
        x1 = np.maximum(start_x[index], start_x[order[:-1]])
        x2 = np.minimum(end_x[index], end_x[order[:-1]])
        y1 = np.maximum(start_y[index], start_y[order[:-1]])
        y2 = np.minimum(end_y[index], end_y[order[:-1]])

        # Compute areas of intersection-over-union
        w = np.maximum(0.0, x2 - x1 + 1)
        h = np.maximum(0.0, y2 - y1 + 1)
        intersection = w * h

        # Compute the ratio between intersection and union
        ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)

        left = np.where(ratio < threshold)
        order = order[left]

    return picked_boxes, picked_score


# Normalize the coordinates of the bounding box.

def normalize_coord(bbox: list[float], img_size: list[int | float]) -> list[int | float]:
    """Normalize the coordinates of the bounding box.
    Args:
        bbox: list[float], bounding box coordinates
        img_size: list[int | float], image size in (width, height)
    Rets:
        list[int | float], normalized bounding box coordinates
    """
    w,h = img_size
    x1,y1,x2,y2 = [int(v) for v in bbox]
    x1 = max(0,x1)
    y1 = max(0,y1)
    x2 = min(x2,w-1)
    y2 = min(y2,h-1)
    return [x1,y1,x2,y2]


# %% Model Loading 
import torch

from transformers import AutoProcessor, BlipForQuestionAnswering
vqa_hf_name = "Salesforce/blip-vqa-base"  # "Salesforce/blip-vqa-capfilt-large"
vqa_model, vqa_processor = load_hf_model(vqa_hf_name, AutoProcessor, BlipForQuestionAnswering)

from transformers import OwlViTProcessor, OwlViTForObjectDetection
loc_hf_name = "google/owlvit-base-patch16"  # "google/owlvit-large-patch14"
loc_model, loc_processor = load_hf_model(loc_hf_name, OwlViTProcessor, OwlViTForObjectDetection)



# %% APIs

# visual question answering
def visual_qa(image_name: str, question: str) -> str:
    image = load_image(image_name)
    encoding = vqa_processor(image, question, return_tensors='pt')
    encoding = {k:v.to(vqa_model.device) for k,v in encoding.items()}
    with torch.no_grad(): outputs = vqa_model.generate(**encoding)
    answer = vqa_processor.decode(outputs[0], skip_special_tokens=True)
    return answer


@app.get("/vqa")
def visual_qa_api(image_name: str, question: str) -> dict[str, str]:
    return {
        "image_name": image_name, "question": question,
        "model_name": vqa_hf_name, "answer": visual_qa(image_name, question)
    }


# object detection
def locate_objects(
    image_name: str, object_name: str, 
    threshold: float = 0.1, nms_threshold: float = 0.5,
) -> list[list[float]]:
    image = load_image(image_name)
    encoding = loc_processor(
        text=[[f"a photo of {object_name}"]],
        images=image,
        return_tensors='pt'
    )
    encoding = {k:v.to(loc_model.device) for k,v in encoding.items()}
    with torch.no_grad(): outputs = loc_model(**encoding)
    target_sizes = torch.Tensor([image.size[::-1]]).to(loc_model.device)
    results = loc_processor.post_process_object_detection(
        outputs=outputs, threshold=threshold, target_sizes=target_sizes
    )
    boxes, scores = results[0]["boxes"], results[0]["scores"]
    boxes = boxes.cpu().detach().numpy().tolist()
    scores = scores.cpu().detach().numpy().tolist()
    if len(boxes)==0: return []

    boxes, scores = zip(*sorted(zip(boxes,scores),key=lambda x: x[1],reverse=True))
    selected_boxes = []
    selected_scores = []
    for i in range(len(scores)):
        if scores[i] > threshold:
            coord = normalize_coord(boxes[i], image.size)
            selected_boxes.append(coord)
            selected_scores.append(scores[i])

    selected_boxes, selected_scores = nms(selected_boxes,selected_scores,nms_threshold)
    return selected_boxes 


@app.get("/loc")
def locate_objects_api(image_name: str, object_name: str) -> dict[str, str | list[list[float]]]:
    return {
        "image_name": image_name, "object_name": object_name,
        "model_name": loc_hf_name, "boxes": locate_objects(image_name, object_name)
    }


# %% Example Usage

# loc
# res = requests.get(f"http://127.0.0.1:8000/loc", params={"image_name": image_name, "object_name": "elephant"})
# res.json() == {"image_name":"n100552.jpg","object_name":"elephant","model_name":"google/owlvit-base-patch16","boxes":[[43.0,98.0,577.0,470.0]]}

# vqa
# res = requests.get(f"http://127.0.0.1:8000/vqa", params={"image_name": image_name, "question": "How many legs does the animal has?"})
# res.json() == {"image_name":"n100552.jpg","question":"How many legs does the animal has?","model_name":"Salesforce/blip-vqa-base","answer":"4"}'
