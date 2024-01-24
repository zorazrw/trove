Your task is to write the solution with high-level tools, i.e., Python functions, to reason over images.
Think about the potential program solution for this example, you can create high-level functions, that could be used to solve this example. For example, if the solution involves multiple actions that are always used together, it is more efficient to create and use the tool.

**Toolbox**
${toolbox}


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

**Question**
${question}
**Image**
${image}
**Solution**
