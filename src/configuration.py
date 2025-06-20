import logging
from pydantic import BaseModel, Field, ValidationError, field_validator
from keboola.component.exceptions import UserException

from consts import DEFAULT_PLACE_ID_COLUMN, DEFAULT_PLACE_URL_COLUMN


class Destination(BaseModel):
    incrementalOutput: bool = Field()
    outputTableName: str = Field()


class Configuration(BaseModel):
    token: str = Field(alias="#token")

    language: str = Field()
    maxReviews: int = Field()
    personalData: bool = Field()
    reviewsOrigin: str = Field()
    reviewsSort: str = Field()
    reviewsStartDate: str = Field()
    destination: Destination = Field()
    placeIdColumn: str = Field(default=DEFAULT_PLACE_ID_COLUMN)
    placeUrlColumn: str = Field(default=DEFAULT_PLACE_URL_COLUMN)

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as e:
            error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            raise UserException(f"Validation Error: {', '.join(error_messages)}")

    @field_validator('token')
    def validate_token(cls, value):
        if not value:
            raise UserException('Apify API Token is empty. Please, make sure you set the token correctly')
        return value
