from typing import List, Optional

from .cat_recognition import CatFaceRecognizer


class DogFaceRecognizer(CatFaceRecognizer):
    def __init__(
        self,
        model_dir: str = "models/dog_face",
        model_filename: str = "dog_resnet101.pth",
        backbone_name: str = "resnet101",
        device: Optional[str] = None,
        hash_length: Optional[int] = None,
        yolo_model_path: Optional[str] = None,
        yolo_class_names: Optional[List[str]] = None,
    ):
        super().__init__(
            model_dir=model_dir,
            model_filename=model_filename,
            backbone_name=backbone_name,
            device=device,
            hash_length=hash_length,
            yolo_model_path=yolo_model_path,
            yolo_class_names=yolo_class_names or ["dog"],
        )
