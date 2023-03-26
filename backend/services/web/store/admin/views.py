from aiohttp.web import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session, get_session

from backend.services.web.store.admin.schemes import AdminSchema
from backend.services.web.app import View
from backend.services.web.mixins import AuthRequiredMixin
from backend.services.web.schemes import OkResponseSchema
from backend.services.web.utils import json_response


class AdminLoginView(View):
    @docs(
        tags=["admin"],
        summary="Admin login method",
        description="Admin login method"
    )
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        admin = await self.request.app.store.admins.get_by_email(self.data["email"])
        if admin and admin.is_password_valid(self.data["password"]):
            session = await new_session(self.request)
            session["admin"] = {"email": admin.email, "id": admin.id}
            return json_response(data=AdminSchema().dump(admin))
        raise HTTPForbidden()


class AdminCurrentView(AuthRequiredMixin, View):
    @docs(
        tags=["admin"],
        summary="Current admin",
        description="Get current admin information method"
    )
    @response_schema(AdminSchema, 200)
    async def get(self):
        return json_response(AdminSchema().dump(self.request.admin))


class AdminLogoutView(AuthRequiredMixin, View):
    @docs(
        tags=["admin"],
        summary="Admin logout method",
        description="Admin logout method"
    )
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        session = await get_session(self.request)
        session.invalidate()
        return json_response()
