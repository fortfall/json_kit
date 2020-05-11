### Usage
* Use EasyJSONEncoder to deserialize Enum and customized class
```python
from enum import Enum
from json_encoders import EasyJSONEncoder
class Job(Enum):
    Teacher = 0
    Engineer = 1
    Doctor = 2

hobbies = ["Swimming", "Video Games", "Fishing"]

# If reference keeping is not required, no need to impl __hash__, __eq__
class Person:
    def __init__(self, name, age, job, hobbies):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies

jack = Person('Jack', 33, Job.Teacher)
with open(json_path, 'w') as fp:
    json.dump(jack, fp, cls=EasyJSONEncoder)

# output string
# {"name": "Jack", "age": 33, "job": 0, "hobbies": ["Swimming", "Video Games", "Fishing"]}
```

* Use RefJSONEncoder to deserialize and preserve customized class reference
  * implement \_\_hash\_\_ and \_\_eq\_\_ for class to preserve its references
  * built-in collecionts such list/dict/set/tuple's references are not preserved
```python
from json_encoders import RefJSONEncoder, is_custom_class, hashable, to_hashable
# Should implement __hash__ and __eq__ for certain custom class
# if its reference keeping is intended;
# and don't impl both __hash__ and __eq__ for classes 
# if reference keeping is not intended (when using RefJSONEncoder or AllRefJSONEncoder)
class Person:
    def __init__(self, name, age, job, hobbies):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies
    
    def __hash__(self):
        data = [(k, v) if hashable(v) else (k, to_hashable(v)) for k, v in self.__dict__.items()]
        data.sort(key=lambda x: x[0])
        data = tuple(data)
        return hash(data)
    
    def __eq__(self, other):
        if not is_custom_class(other) or not hashable(other):
            return False
        return self.__class__ == other.__class__ and self.__hash__() == other.__hash__()
        
jack = Person('Jack', 33, Job.Doctor)
another_jack = Person('Jack', 33, Job.Doctor)
jacks = [jack, another_jack]

with open(json_path, 'w') as fp:
    json.dump(jacks, fp, cls=RefJSONEncoder)
# output string:
# [{"$id": "1", "$values": ["Swimming", "Video Games", "Fishing"]}, {"$ref": "1"}]
```
* Use AllRefJSONEncoder to deserialize and preserve references of customized class, list(set/tuple), dict
  * implement \_\_hash\_\_ and \_\_eq\_\_ for class to preserve its references
  * built-in collecionts such list/dict/set/tuple's references are preserved
```python
from json_encoders import RefJSONEncoder, is_custom_class, hashable, to_hashable
# Should implement __hash__ and __eq__ for certain custom class
# if its reference keeping is intended
class Person:
    def __init__(self, name, age, job, hobbies):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies
    
    def __hash__(self):
        data = [(k, v) if hashable(v) else (k, id(v)) for k, v in self.__dict__.items()]
        data.sort(key=lambda x: x[0])
        data = tuple(data)
        return hash(data)
    
    def __eq__(self, other):
        if not is_custom_class(other) or not hashable(other):
            return False
        return self.__class__ == other.__class__ and self.__hash__() == other.__hash__()

jack = Person('Jack', 33, Job.Teacher, hobbies)
another_jack = Person('Jack', 33, Job.Teacher, hobbies)
mike = Person('Mike', 24, Job.Doctor, hobbies)
persons = [jack, another_jack, mike]

with open(json_path, 'w') as fp:
    json.dump(persons, fp, cls=AllRefJSONEncoder)
# output text:
# [{"$id": "1", "$values": {"name": "Jack", "age": 33, "job": 0, "hobbies": {"$id": "2", "$values": ["Swimming", "Video Games", "Fishing"]}}}, {"$ref": "1"}, {"name": "Mike", "age": 24, "job": 2, "hobbies": {"$ref": "2"}}]
```