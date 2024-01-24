You task is to write Python program solutions to the given questions about images.
The toolbox section lists all the available functions that can be used in your solution.


## Example
**Question**
Who is carrying the umbrella?
**Image**
"./data/gqa/testdev_images/n100552.jpg"

**Toolbox**
```python
# Import PIL.Image
from PIL import Image
```
```python
# Locate and crop the region of the object
get_object_region(image: str | Image.Image, object_name: str)
```
```python
# Crop the specified box region from the image
crop_region(image: PIL.Image, boxes: list)
```

**Solution**
```python
image_file = "./data/gqa/testdev_images/n100552.jpg"
image = Image.open(image_file).convert('RGB')

carry_region = get_object_region(image, "carry umbrella")
answer = visual_qa(image=carry_region, question="Who is carrying the umbrella?")

print(answer)
```
**Tools**
```python
from PIL import Image
from toolbox import get_object_region
from toolbox import crop_region
```


## Example
**Question**
${question}
**Image**
${image}

**Toolbox**
${toolbox}

**Solution**
