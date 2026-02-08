from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    model_validator
)


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2, pattern=r'^[A-Za-z ]+$')
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode='after')
    def check_age_employment(self):
        if self.is_employed:
            if self.age < 18 or self.age > 65:
                raise ValueError('Возраст должен быть от 18 до 65 лет.')
        return self


# Пример корректных данных
json_ok = """{
    "name": "Ivan Petrov",
    "age": 40,
    "email": "ivan.petrov@gmail.com",
    "is_employed": true,
    "address": {
        "city" : "Frankfurt",
        "street": "Berger Street",
        "house_number": 123
    }
}"""

# Пример некорректных данных (возраст не соответствует статусу занятости)
json_bad_age = """{
    "name": "Ivan Petrov",
    "age": 70,
    "email": "ivan.petrov@gmail.com",
    "is_employed": true,
    "address": {
        "city" : "Frankfurt",
        "street": "Berger Street",
        "house_number": 123
    }       
}"""

# Пример некорректных данных (значение имени не соответствует условию поля)
json_bad_name = """{
    "name": "Ivan123",
    "age": 30,
    "email": "ivan.petrov@gmail.com",
    "is_employed": false,
    "address": {
        "city" : "Frankfurt",
        "street": "Berger Street",
        "house_number": 123
    }       
}"""

# Пример некорректных данных (значение полей адреса не соответствует условиям)
json_bad_address = """{
    "name": "Ivan Petrov",
    "age": 40,
    "email": "ivan.petrov@gmail.com",
    "is_employed": true,
    "address": {
        "city" : "F",
        "street": "Be",
        "house_number": -1
    }       
}"""

user = User.model_validate_json(json_ok)

print(user.model_dump_json(indent=2))
