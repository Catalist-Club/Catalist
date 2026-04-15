# 🎯 快速参考卡

## 核心概念
```python
from backend.cat_recognition import (
    AnimalType,                # 枚举: CAT, DOG
    RecognitionResult,         # 通用结果类
    AnimalFaceRecognizer,      # 基础识别器类
    CatFaceRecognizer,         # 猫识别器
    convert_results,           # 批量转换函数
)
from backend.dog_recognition import (
    DogFaceRecognizer,         # 狗识别器
    create_hybrid_recognizer,  # 工厂函数
    create_cat_dog_recognizers,# 工厂函数
)
```

## 常见操作

### 创建识别器
```python
# 单个识别器
cat = CatFaceRecognizer()
dog = DogFaceRecognizer()

# 混合识别器（推荐）
from backend.dog_recognition import create_hybrid_recognizer
hybrid = create_hybrid_recognizer()
```

### 计算签名
```python
image_bytes = open("image.jpg", "rb").read()
embedding, hash_hex, bits = recognizer.compute_signature(image_bytes)
```

### 匹配搜索
```python
# 单物种搜索
results = recognizer.match_against(
    query_hash, query_embedding,
    references,  # Iterable[Tuple[int, Optional[int], np.ndarray, np.ndarray]]
    max_results=5,
    similarity_threshold=0.75
)

# 多物种搜索
results = hybrid.cross_animal_match(
    query_hash, query_embedding,
    references_by_type={
        AnimalType.CAT: cat_refs,
        AnimalType.DOG: dog_refs,
    }
)
```

### 类型转换
```python
# 单个结果
dog_result = cat_result.convert_to_animal(AnimalType.DOG)

# 批量转换
dog_results = convert_results(cat_results, AnimalType.DOG)
```

### 访问结果
```python
result.entity_id           # 通用字段
result.entity_name         # 通用字段
result.animal_type         # AnimalType.CAT 或 AnimalType.DOG
result.similarity          # 相似度 [0, 1]
result.hamming_distance    # 汉明距离
result.matched             # 是否匹配

# 向后兼容
result.cat_id              # = entity_id
result.cat_name            # = entity_name
result.dog_id              # = entity_id
result.dog_name            # = entity_name
```

### 序列化
```python
# 转换为字典
result_dict = result.to_dict()

# JSON 序列化
import json
json_str = json.dumps(result_dict)
```

## 字段对应表

| 新（推荐） | 旧（兼容） | 说明 |
|-----------|-----------|------|
| `entity_id` | `cat_id` | 实体ID |
| `entity_name` | `cat_name` | 实体名称 |
| `animal_type` | 无 | 动物类型（新增） |

## 常见错误与修复

### ❌ 创建 RecognitionResult 时忘记 animal_type
```python
# 错误
result = RecognitionResult(entity_id=42, ...)

# 正确
from backend.cat_recognition import AnimalType
result = RecognitionResult(
    entity_id=42,
    animal_type=AnimalType.CAT,
    ...
)
```

### ❌ 混淆了 cross_animal_match 的参数格式
```python
# 错误
results = hybrid.cross_animal_match(
    query_hash, query_embedding,
    [cat_refs, dog_refs]  # ❌ 列表格式
)

# 正确
results = hybrid.cross_animal_match(
    query_hash, query_embedding,
    references_by_type={
        AnimalType.CAT: cat_refs,
        AnimalType.DOG: dog_refs,
    }
)
```

## 性能提示

- `HybridAnimalRecognizer` 可复用实例，无需每次创建
- `cross_animal_match()` 内部会自动排序，无需手动合并
- 使用 `convert_results()` 进行批量转换，比逐个转换更高效

## 扩展新动物类型

1. 添加到枚举
2. 创建识别器类
3. 添加到 HybridAnimalRecognizer

```python
# 1. 扩展枚举
class AnimalType(str, Enum):
    CAT = "cat"
    DOG = "dog"
    BIRD = "bird"  # ← 新增

# 2. 创建识别器
class BirdFaceRecognizer(AnimalFaceRecognizer):
    def __init__(self, ...):
        super().__init__(
            animal_type=AnimalType.BIRD,
            model_dir="models/bird_face",
            ...
        )

# 3. 使用
hybrid.add_recognizer(AnimalType.BIRD, BirdFaceRecognizer())
```

## 版本兼容性
- ✅ Python 3.7+
- ✅ PyTorch + TorchVision
- ✅ OpenCV (可选，用于 YOLO)

---

**记住**: 所有旧代码继续工作。新代码应该使用 `entity_id` 和 `animal_type` 字段。
