from typing import TypedDict


class DeathTypeDto(TypedDict):
    id: int
    Name: int


class DeathDto(TypedDict):
    id: int
    description: str
    factors: list
    genes: list


class FactorDto(TypedDict):
    id: int
    activation: str


class GeneDto(TypedDict):
    id: int
    activation: str
