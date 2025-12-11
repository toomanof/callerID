from pydantic import BaseModel


class RegistryData(BaseModel):
    hash: str
    abc_def: int
    range_from: int
    range_to: int
    capacity: int
    operator: str
    region: str
    territory: str
    inn: str






