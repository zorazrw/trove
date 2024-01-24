You task is to write Python program solutions to the given questions about images.


## Example
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


## Example
**Question**
${question}
**Image**
${image}

**Solution**
