import json
import typing

from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity, HTTPBadRequest, HTTPUnauthorized, \
    HTTPForbidden, HTTPNotFound, HTTPMethodNotAllowed, HTTPConflict
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session
from sqlalchemy.exc import IntegrityError

from backend.services.web.utils import error_json_response
from backend.entities.admin import Admin

if typing.TYPE_CHECKING:
    from backend.services.web.app import Application, Request


@middleware
async def auth_middleware(request: "Request", handler: callable):
    session = await get_session(request)
    if session:
        request.admin = Admin.from_session(session)
    return await handler(request)


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPBadRequest as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data={},
        )
    except HTTPUnauthorized as e:
        return error_json_response(
            http_status=401,
            status=HTTP_ERROR_CODES[401],
            message=e.reason,
            data={},
        )
    except HTTPForbidden as e:
        return error_json_response(
            http_status=403,
            status=HTTP_ERROR_CODES[403],
            message=e.reason,
            data={},
        )
    except HTTPNotFound as e:
        return error_json_response(
            http_status=404,
            status=HTTP_ERROR_CODES[404],
            message=e.reason,
            data={},
        )
    except HTTPMethodNotAllowed as e:
        return error_json_response(
            http_status=405,
            status=HTTP_ERROR_CODES[405],
            message=e.reason,
            data={},
        )
    except HTTPConflict as e:
        return error_json_response(
            http_status=409,
            status=HTTP_ERROR_CODES[409],
            message=e.reason,
            data={},
        )
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )
    except IntegrityError as e:
        return error_json_response(
            http_status=409,
            status=HTTP_ERROR_CODES[409],
            message=str(e.orig.args[0].__str__()),
            data={}
        )
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error", message=str(e)
        )


def setup_middlewares(app: "Application"):
    app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
