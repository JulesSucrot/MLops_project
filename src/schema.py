# src/schema.py
from pydantic import BaseModel, Field
from typing import Literal

class Student(BaseModel):
    Blood_Status: Literal["Half-blood","Muggle-born","Pure-blood"] = Field(alias="Blood Status")
    Bravery: int
    Intelligence: int
    Loyalty: int
    Ambition: int
    Dark_Arts_Knowledge: int = Field(alias="Dark Arts Knowledge")
    Quidditch_Skills: int = Field(alias="Quidditch Skills")
    Dueling_Skills: int = Field(alias="Dueling Skills")
    Creativity: int

    def as_dataframe_row(self):
        return {
            "Blood Status": self.Blood_Status,
            "Bravery": self.Bravery,
            "Intelligence": self.Intelligence,
            "Loyalty": self.Loyalty,
            "Ambition": self.Ambition,
            "Dark Arts Knowledge": self.Dark_Arts_Knowledge,
            "Quidditch Skills": self.Quidditch_Skills,
            "Dueling Skills": self.Dueling_Skills,
            "Creativity": self.Creativity,
        }