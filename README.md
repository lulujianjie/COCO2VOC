# COCO2VOC
An implementation of converting COCO format to VOC format

## Usage

```python
coco2voc.py [-h] [-input_json INPUT_JSON]
                   [-input_img_dir INPUT_IMG_DIR] [-output_dir OUTPUT_DIR]
```

For example:
```python
coco2voc.py -input_json ./train.json -input_img_dir /datasets/images -output_dir ./Annotations
```

