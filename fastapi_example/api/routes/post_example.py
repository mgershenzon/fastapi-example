from typing import Union

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

router = APIRouter()


class PostRequestExample(BaseModel):
    str_for_example: str
    float_or_none_for_example: Union[float, None]


@router.post('/post_example')
async def post_example(post_request: PostRequestExample):
    """
    Returns the string that was sent in the request

    :return:  the string that was sent in the request
    """

    # In restful APIs a new object is usually created and saved here

    return post_request
