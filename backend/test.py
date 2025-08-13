from pydantic import BaseModel

class Test(BaseModel):
    test: str
    test2: str

test = Test(test='biba', test2='baraben')

test.test = 'abobobobobob'

print(test.test)