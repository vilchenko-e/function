from pydantic import BaseModel, Field, field_validator


class MaterialCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = ""
    sources: str = ""

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        title = value.strip()

        if not title:
            raise ValueError("Название не должно быть пустым")

        return title
