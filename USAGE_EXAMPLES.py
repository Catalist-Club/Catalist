"""
Practical examples for using the refactored cat/dog recognition system.

This file demonstrates the new features and improved API after the refactoring.
"""

# ============================================================================
# EXAMPLE 1: Basic Usage (Backward Compatible)
# ============================================================================

def example_basic_usage():
    """Traditional usage with CatFaceRecognizer and DogFaceRecognizer."""
    from backend.cat_recognition import CatFaceRecognizer
    from backend.dog_recognition import DogFaceRecognizer
    
    # Create recognizers (works as before)
    cat_recognizer = CatFaceRecognizer()
    dog_recognizer = DogFaceRecognizer()
    
    # Compute signatures (works as before)
    cat_image_bytes = open("cat.jpg", "rb").read()
    cat_embedding, cat_hash, cat_bits = cat_recognizer.compute_signature(cat_image_bytes)
    
    dog_image_bytes = open("dog.jpg", "rb").read()
    dog_embedding, dog_hash, dog_bits = dog_recognizer.compute_signature(dog_image_bytes)
    
    print(f"Cat embedding shape: {cat_embedding.shape}")
    print(f"Dog embedding shape: {dog_embedding.shape}")


# ============================================================================
# EXAMPLE 2: Converting Between Animal Types
# ============================================================================

def example_convert_results():
    """Convert recognition results between animal types."""
    from backend.cat_recognition import RecognitionResult, AnimalType
    
    # Create a result for a cat
    cat_result = RecognitionResult(
        entity_id=42,
        entity_name="Whiskers",
        similarity=0.92,
        hamming_distance=8,
        reference_image_id=100,
        reference_hash_length=256,
        matched=True,
        metadata={"confidence": 0.95},
        animal_type=AnimalType.CAT
    )
    
    print(f"Original cat result: {cat_result.animal_type}")
    print(f"  - ID: {cat_result.entity_id}, Name: {cat_result.entity_name}")
    
    # Convert to dog type (keeps all data, just changes type)
    dog_result = cat_result.convert_to_animal(AnimalType.DOG)
    
    print(f"\nConverted dog result: {dog_result.animal_type}")
    print(f"  - ID: {dog_result.entity_id}, Name: {dog_result.entity_name}")
    print(f"  - Similarity preserved: {dog_result.similarity}")


# ============================================================================
# EXAMPLE 3: Using the Hybrid Recognizer
# ============================================================================

def example_hybrid_recognizer():
    """Use HybridAnimalRecognizer for handling both cats and dogs."""
    from backend.dog_recognition import create_hybrid_recognizer
    from backend.cat_recognition import AnimalType
    import numpy as np
    
    # Create hybrid recognizer with one line
    hybrid = create_hybrid_recognizer()
    
    # Optionally load different models
    hybrid.get_recognizer(AnimalType.CAT).set_model_weights("models/cat_face/custom_cat_model.pth")
    hybrid.get_recognizer(AnimalType.DOG).set_model_weights("models/dog_face/custom_dog_model.pth")
    
    # Create mock data
    query_hash = np.random.randn(256)
    query_embedding = np.random.randn(512)
    
    cat_ref1 = (1, 10, np.random.randn(256), np.random.randn(512))
    cat_ref2 = (2, 20, np.random.randn(256), np.random.randn(512))
    
    dog_ref1 = (3, 30, np.random.randn(256), np.random.randn(512))
    dog_ref2 = (4, 40, np.random.randn(256), np.random.randn(512))
    
    # Match against cats only
    cat_matches = hybrid.match_against(
        query_hash, query_embedding,
        [cat_ref1, cat_ref2],
        AnimalType.CAT,
        max_results=5,
        similarity_threshold=0.7
    )
    
    # Match against dogs only
    dog_matches = hybrid.match_against(
        query_hash, query_embedding,
        [dog_ref1, dog_ref2],
        AnimalType.DOG,
        max_results=5,
        similarity_threshold=0.7
    )
    
    print(f"Found {len(cat_matches)} cat matches")
    print(f"Found {len(dog_matches)} dog matches")


# ============================================================================
# EXAMPLE 4: Cross-Animal Matching (Advanced Feature)
# ============================================================================

def example_cross_animal_match():
    """Advanced: Match query across both cats and dogs simultaneously."""
    from backend.dog_recognition import create_hybrid_recognizer
    from backend.cat_recognition import AnimalType
    import numpy as np
    
    hybrid = create_hybrid_recognizer()
    
    # Create mock data
    query_hash = np.random.randn(256)
    query_embedding = np.random.randn(512)
    
    cat_refs = [
        (1, 10, np.random.randn(256), np.random.randn(512)),
        (2, 20, np.random.randn(256), np.random.randn(512)),
    ]
    
    dog_refs = [
        (3, 30, np.random.randn(256), np.random.randn(512)),
        (4, 40, np.random.randn(256), np.random.randn(512)),
    ]
    
    # Cross-animal matching: search across both types simultaneously
    combined_results = hybrid.cross_animal_match(
        query_hash, query_embedding,
        references_by_type={
            AnimalType.CAT: cat_refs,
            AnimalType.DOG: dog_refs,
        },
        max_results=5,
        similarity_threshold=0.7
    )
    
    print(f"Cross-animal match found {len(combined_results)} total matches:")
    for result in combined_results:
        print(f"  - [{result.animal_type.value}] ID: {result.entity_id}, Similarity: {result.similarity:.3f}")


# ============================================================================
# EXAMPLE 5: Backward Compatibility - Old API Still Works
# ============================================================================

def example_backward_compatibility():
    """Show that old property names still work."""
    from backend.cat_recognition import RecognitionResult, AnimalType
    
    result = RecognitionResult(
        entity_id=123,
        entity_name="Fluffy",
        similarity=0.95,
        hamming_distance=5,
        reference_image_id=456,
        reference_hash_length=256,
        matched=True,
        metadata={},
        animal_type=AnimalType.CAT
    )
    
    # Old property names still work (backward compatibility)
    print(f"Using old property names:")
    print(f"  - result.cat_id: {result.cat_id}")           # Works!
    print(f"  - result.cat_name: {result.cat_name}")       # Works!
    print(f"  - result.dog_id: {result.dog_id}")           # Works! (alias to entity_id)
    print(f"  - result.dog_name: {result.dog_name}")       # Works! (alias to entity_name)
    
    # New property names for explicit type
    print(f"\nUsing new property names:")
    print(f"  - result.entity_id: {result.entity_id}")
    print(f"  - result.entity_name: {result.entity_name}")
    print(f"  - result.animal_type: {result.animal_type}")


# ============================================================================
# EXAMPLE 6: Batch Conversion
# ============================================================================

def example_batch_conversion():
    """Convert a list of results from one animal type to another."""
    from backend.cat_recognition import (
        RecognitionResult, AnimalType, convert_results
    )
    
    # Create list of cat results
    cat_results = [
        RecognitionResult(
            entity_id=i, entity_name=f"Cat{i}",
            similarity=0.9 - i*0.01, hamming_distance=i,
            reference_image_id=100+i, reference_hash_length=256,
            matched=True, metadata={},
            animal_type=AnimalType.CAT
        )
        for i in range(3)
    ]
    
    print(f"Original {len(cat_results)} cat results:")
    for r in cat_results:
        print(f"  - {r.animal_type}: {r.entity_name}")
    
    # Convert all to dog type
    dog_results = convert_results(cat_results, AnimalType.DOG)
    
    print(f"\nConverted to {len(dog_results)} dog results:")
    for r in dog_results:
        print(f"  - {r.animal_type}: {r.entity_name}")


# ============================================================================
# EXAMPLE 7: Serialize Results to JSON/Dict
# ============================================================================

def example_serialize_results():
    """Convert results to dictionaries (useful for JSON APIs)."""
    from backend.cat_recognition import RecognitionResult, AnimalType
    import json
    
    cat_result = RecognitionResult(
        entity_id=42,
        entity_name="Whiskers",
        similarity=0.92,
        hamming_distance=8,
        reference_image_id=100,
        reference_hash_length=256,
        matched=True,
        metadata={"confidence": 0.95, "breed_score": 0.88},
        animal_type=AnimalType.CAT
    )
    
    # Convert to dictionary
    result_dict = cat_result.to_dict()
    
    print("Result as dictionary:")
    print(json.dumps(result_dict, indent=2))
    
    # Useful for API responses
    return result_dict


# ============================================================================
# EXAMPLE 8: Custom Animal Type Labels (Future Extensibility)
# ============================================================================

def example_enum_usage():
    """Show how the AnimalType enum works."""
    from backend.cat_recognition import AnimalType
    
    # Access enum values
    for animal in AnimalType:
        print(f"Animal type: {animal.name} = '{animal.value}'")
    
    # Convert string to enum
    animal_str = "cat"
    animal_type = AnimalType(animal_str)
    print(f"\nConverted '{animal_str}' to enum: {animal_type}")
    
    # Check enum types
    print(f"Is cat? {AnimalType.CAT == AnimalType.CAT}")
    print(f"Is dog? {AnimalType.CAT == AnimalType.DOG}")


if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 2: Converting Between Animal Types")
    print("=" * 70)
    example_convert_results()
    
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Backward Compatibility")
    print("=" * 70)
    example_backward_compatibility()
    
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Batch Conversion")
    print("=" * 70)
    example_batch_conversion()
    
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Serialize Results")
    print("=" * 70)
    example_serialize_results()
    
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Enum Usage")
    print("=" * 70)
    example_enum_usage()
