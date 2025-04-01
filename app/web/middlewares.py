import json
import typing

# from aiohttp.web_exceptions import HTTPUnprocessableEntity
# from aiohttp.web_middlewares import middleware
# from aiohttp_apispec import validation_middleware
# from fastapi.exceptions import HTTPException

# from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application

# HTTP_ERROR_CODES = {
#     400: "bad_request",
#     401: "unauthorized",
#     403: "forbidden",
#     404: "not_found",
#     405: "not_implemented",
#     409: "conflict",
#     500: "internal_server_error",
# }


# @middleware
# async def error_handling_middleware(request: "Request", handler):
#     try:
#         response = await handler(request)
#     except HTTPUnprocessableEntity as e:
#         return error_json_response(
#             http_status=400,
#             status=HTTP_ERROR_CODES[400],
#             message=e.reason,
#             data=json.loads(e.text),
#         )
#     except HTTPException as e:
#         http_status = e.status_code if hasattr(e, 'status_code') else 500
#         if http_status not in HTTP_ERROR_CODES:
#             http_status = 500

#         message = getattr(e, 'reason')

#         data = None
#         if hasattr(e, 'text'):
#             try:
#                 data = json.loads(e.text)
#             except json.JSONDecodeError:
#                 data = e.text

#         return error_json_response(
#             http_status=http_status,
#             status=HTTP_ERROR_CODES[http_status],
#             message=message,
#             data=data,
#         )
#     # except Exception as e:  # TODO: раскомментить когда-нибудь
#     #     status = HTTP_ERROR_CODES[500]
#     #     message = "Internal server error"
#     #     return error_json_response(
#     #         http_status=500,
#     #         status=status,
#     #         message=message,
#     #         data={"err": str(e)},
#     #     )
#     return response


def setup_middlewares(app: "Application"):
    # app.middleware(error_handling_middleware)
    # app.middleware(validation_middleware)
    pass
