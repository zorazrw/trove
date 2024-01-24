You task is to write Python program solutions to the given questions about images.
You should also create Python functions that can be used by your solution, if you believe the function can be reused to solve other questions.


## Example
**Question**
Who is carrying the umbrella?
**Image**
"./data/gqa/testdev_images/n100552.jpg"

**Solution**
```python
from PIL import Image
image_file = "./data/gqa/testdev_images/n100552.jpg"
image = Image.open(image_file).convert('RGB')

carry_region = get_object_region(image, "carry umbrella")
answer = visual_qa(image=carry_region, question="Who is carrying the umbrella?")

print(answer)
```
**Tools**
```python
from PIL import Image
from toolbox import locate_objects
from toolbox import crop_region

def get_object_region(image: str | Image.Image, object_name: str) -> Image.Image:
    """Locate the crop the image of the object."""
    boxes = locate_objects(image=image, object_name=object_name)
    if isinstance(image, str):
        image = Image.open(image).convert('RGB')
    object_image = crop_region(image=image, boxes=boxes)
    return object_image
```


## Example
**Question**
Are both small refrigerators and microwaves in the picture?
**Image**
data/gqa/testdev_images/n579256.jpg
**Solution**
```python
from PIL import Image
image_file = "data/gqa/testdev_images/n579256.jpg"
image = Image.open(image_file).convert('RGB')

any_exists = check_exists(image, ["small refrigerator", "microwave"])

print(any_exists)
```
**Tools**
```python
from PIL import Image
from toolbox import locate_objects
def check_exists(image: str | Image.Image, object_list: list[str]) -> str:
    """Check if all objects exist in the image."""
    for object_name in object_list:
        boxes = locate_objects(image=image, object_name=object_name)
        if len(boxes) == 0: return "no"
    return "yes"
```


## Example
**Question**
${question}
**Image**
${image}

**Solution**
