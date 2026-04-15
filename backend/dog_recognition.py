from typing import List, Optional

from .cat_recognition import AnimalFaceRecognizer, AnimalType, convert_results, HybridAnimalRecognizer


class DogFaceRecognizer(AnimalFaceRecognizer):
    """Dog face recognizer - uses AnimalFaceRecognizer with DOG type."""

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
            animal_type=AnimalType.DOG,
            model_dir=model_dir,
            model_filename=model_filename,
            backbone_name=backbone_name,
            device=device,
            hash_length=hash_length,
            yolo_model_path=yolo_model_path,
            yolo_class_names=yolo_class_names or ["dog"],
        )


# ============================================================================
# CONVENIENCE FACTORY FUNCTIONS
# ============================================================================

def create_cat_dog_recognizers(
    cat_model_dir: str = "models/cat_face",
    cat_model_filename: str = "cat_resnet101_gpu_amp_final.pth",
    dog_model_dir: str = "models/dog_face",
    dog_model_filename: str = "dog_resnet101.pth",
    device: Optional[str] = None,
) -> tuple:
    """Create both cat and dog recognizers.
    
    Returns:
        Tuple of (cat_recognizer, dog_recognizer)
    """
    from .cat_recognition import CatFaceRecognizer
    
    cat_recognizer = CatFaceRecognizer(model_dir=cat_model_dir, model_filename=cat_model_filename, device=device)
    dog_recognizer = DogFaceRecognizer(model_dir=dog_model_dir, model_filename=dog_model_filename, device=device)
    return cat_recognizer, dog_recognizer


def create_hybrid_recognizer(
    cat_model_dir: str = "models/cat_face",
    cat_model_filename: str = "cat_resnet101_gpu_amp_final.pth",
    dog_model_dir: str = "models/dog_face",
    dog_model_filename: str = "dog_resnet101.pth",
    device: Optional[str] = None,
) -> HybridAnimalRecognizer:
    """Create a hybrid recognizer that handles both cats and dogs.
    
    Returns:
        HybridAnimalRecognizer instance ready for cross-animal recognition
    """
    from .cat_recognition import CatFaceRecognizer
    
    cat_recognizer = CatFaceRecognizer(model_dir=cat_model_dir, model_filename=cat_model_filename, device=device)
    dog_recognizer = DogFaceRecognizer(model_dir=dog_model_dir, model_filename=dog_model_filename, device=device)
    return HybridAnimalRecognizer(cat_recognizer, dog_recognizer)
