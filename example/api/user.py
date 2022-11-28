from fastframework.decorators import actions
from fastframework.resources import GenericResource
from fastapi import Request, Response


class UserResource(GenericResource):
    # tags = ["user"]

    @actions(path="/users", methods=["POST"])
    async def get_user_list(self, request: Request, response: Response, user_id: int):
        return {"message": "get_user_list"}