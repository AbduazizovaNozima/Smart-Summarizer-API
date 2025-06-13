from pydantic import BaseModel, validator


class TextRequest(BaseModel):
    """Text summarization uchun so'rov modeli"""
    text: str

    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Text must not be empty')
        return v


class SummaryResponse(BaseModel):
    """Text summarization uchun javob modeli"""
    summary: str