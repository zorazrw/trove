Your task is to use tools, i.e., Python functions, to reason over the image.
Write a program solution to the question by decomposing it into multiple steps. Then specify the tools used in each step by importing from the toolbox. Make sure that all tools used in the solution are defined in the toolbox. Do not use any undefined functions.
All images are presented as PIL.Image objects, you can use functions in PIL, cv2 if they help.

**Toolbox**
${toolbox}


**Question**
Who is carrying the umbrella?
**Image**
"./data/gqa/testdev_images/n100552.jpg"
**Solution**
```python
image_file = "./data/gqa/testdev_images/n100552.jpg"
image = Image.open(image_file).convert('RGB')

carry_boxes = locate_objects(image, "carry umbrella")
carry_region = crop_region(image, carry_boxes)
answer = visual_qa(image=carry_region, question="Who is carrying the umbrella?")

print(answer)
```
**Tools**
```python
from PIL import Image
from toolbox import visual_qa
from toolbox import locate_objects
from toolbox import crop_region
```


**Question**
Are there either any small refrigerators or microwaves in the picture?
**Image**
data/gqa/testdev_images/n579256.jpg
**Solution**
```python
image_file = "data/gqa/testdev_images/n579256.jpg"
image = Image.open(image_file).convert('RGB')

small_refrigerator_boxes = locate_objects(image, "small refrigerator")
microwave_boxes = locate_objects(image, "microwave")
if len(small_refrigerator_boxes) > 0 and len(microwave_boxes) > 0:
    any_exists = "yes"
else:
    any_exists = "no"

print(any_exists)
```
**Tools**
```python
from PIL import Image
from toolbox import locate_objects
```

**Question**
${question}
**Image**
${image}
**Solution**
