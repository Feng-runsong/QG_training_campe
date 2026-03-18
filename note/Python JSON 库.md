# Python JSON 库

## 1. 基本介绍
JSON (JavaScript Object Notation) 是一种轻量级的数据交换格式。Python 的 `json` 模块提供了JSON数据的编码和解码功能。

```python
import json
```

## 2. 主要函数

### 2.1 序列化 (Python → JSON)

| 函数                 | 描述                             | 返回值 |
| -------------------- | -------------------------------- | ------ |
| `json.dumps(obj)`    | 将Python对象转换为JSON字符串     | 字符串 |
| `json.dump(obj, fp)` | 将Python对象转换为JSON并写入文件 | None   |

### 2.2 反序列化 (JSON → Python)

| 函数              | 描述                             | 返回值     |
| ----------------- | -------------------------------- | ---------- |
| `json.loads(str)` | 将JSON字符串转换为Python对象     | Python对象 |
| `json.load(fp)`   | 从文件读取JSON并转换为Python对象 | Python对象 |

## 3. 类型转换对照表

### Python → JSON
| Python      | JSON   |
| ----------- | ------ |
| dict        | object |
| list, tuple | array  |
| str         | string |
| int, float  | number |
| True        | true   |
| False       | false  |
| None        | null   |

### JSON → Python
| JSON   | Python    |
| ------ | --------- |
| object | dict      |
| array  | list      |
| string | str       |
| number | int/float |
| true   | True      |
| false  | False     |
| null   | None      |

## 4. 基本使用示例

```python
import json

# 1. 序列化示例
data = {
    "name": "张三",
    "age": 25,
    "city": "北京",
    "hobbies": ["读书", "游泳"],
    "is_student": False,
    "scores": None
}

# 转换为JSON字符串
json_str = json.dumps(data)
print(json_str)  
# {"name": "\u5f20\u4e09", "age": 25, "city": "\u5317\u4eac", ...}

# 美化输出
json_str_pretty = json.dumps(data, indent=2, ensure_ascii=False)
print(json_str_pretty)

# 2. 反序列化示例
json_data = '{"name": "李四", "age": 30, "city": "上海"}'
python_obj = json.loads(json_data)
print(python_obj["name"])  # 李四
print(type(python_obj))    # <class 'dict'>

# 3. 文件操作示例
# 写入JSON文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 读取JSON文件
with open("data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(loaded_data)
```

## 5. 常用参数

```python
# indent: 缩进格式化
json.dumps(data, indent=4)

# separators: 自定义分隔符
json.dumps(data, separators=(',', ':'))  # 紧凑输出

# sort_keys: 按键排序
json.dumps(data, sort_keys=True)

# ensure_ascii: ASCII转义
json.dumps(data, ensure_ascii=False)  # 显示中文

# skipkeys: 跳过非基本类型的键
data = {("key",): "value"}
json.dumps(data, skipkeys=True)  # 跳过元组键
```

## 6. 处理自定义对象

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 方法1：自定义编码函数
def person_encoder(obj):
    if isinstance(obj, Person):
        return {"name": obj.name, "age": obj.age, "__class__": "Person"}
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

person = Person("王五", 28)
json_str = json.dumps(person, default=person_encoder)

# 方法2：继承JSONEncoder
class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)

json_str = json.dumps(person, cls=PersonEncoder)

# 方法3：自定义解码
def person_decoder(dct):
    if "__class__" in dct and dct["__class__"] == "Person":
        return Person(dct["name"], dct["age"])
    return dct

data = json.loads(json_str, object_hook=person_decoder)
```

## 7. 错误处理

```python
try:
    # 尝试解析无效JSON
    invalid_json = '{"name": "test",}'
    data = json.loads(invalid_json)
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
    print(f"错误位置: 第{e.lineno}行, 第{e.colno}列")
```

## 8. 高级特性

### 8.1 命令行工具
```bash
# 格式化JSON文件
python -m json.tool input.json output.json

# 美化输出
cat data.json | python -m json.tool
```

### 8.2 处理大文件
```python
# 使用ijson或逐行处理大文件
def read_large_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
```

### 8.3 自定义格式化
```python
class CustomEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def encode(self, obj):
        # 自定义编码逻辑
        return super().encode(obj)
    
    def iterencode(self, obj):
        # 自定义迭代编码
        return super().iterencode(obj)
```

## 9. 性能优化技巧

```python
# 1. 使用列表推导式批量处理
data_list = [json.loads(line) for line in json_lines]

# 2. 使用ujson（更快）
try:
    import ujson as json
except ImportError:
    import json

# 3. 复用编码器
encoder = json.JSONEncoder()
results = [encoder.encode(obj) for obj in large_data_list]
```

## 10. 常见问题与解决方案

### 10.1 处理特殊数据类型
```python
import datetime
import decimal

# 处理datetime对象
data = {
    "date": datetime.datetime.now(),
    "decimal": decimal.Decimal("10.5")
}

def custom_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

json_str = json.dumps(data, default=custom_handler)
```

### 10.2 处理循环引用
```python
from json import JSONEncoder

class SafeEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return {k: v for k, v in obj.__dict__.items() 
                    if not callable(v) and not k.startswith('_')}
        return super().default(obj)
```

## 11. 最佳实践

```python
# 1. 始终指定编码
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

# 2. 使用上下文管理器
def safe_json_load(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"读取JSON文件失败: {e}")
        return None

# 3. 验证JSON数据
def validate_json_schema(data, required_keys):
    return all(key in data for key in required_keys)

# 4. 使用dataclass配合JSON
from dataclasses import dataclass, asdict

@dataclass
class User:
    name: str
    age: int
    
    def to_json(self):
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)
```
