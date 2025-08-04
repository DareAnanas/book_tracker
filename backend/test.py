from pydantic import BaseModel

class Test(BaseModel):
    test: str
    test2: str

test = Test(test='biba', test2='baraben')

print(test.test2)