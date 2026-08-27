import logging
from typing import NoReturn

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class APIError(Exception):
    def __init__(self, *, status_code: int, code: str, message: str) -> None:
        super().__init__(code)
        self.status_code = status_code
        self.code = code
        self.message = message


def raise_api_error(*, status_code: int, code: str, message: str) -> NoReturn:
    raise APIError(status_code=status_code, code=code, message=message)


def register_error_handlers(application: FastAPI) -> None:
    @application.exception_handler(APIError)
    async def handle_api_error(_request: Request, error: APIError) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code,
            content={"code": error.code, "message": error.message},
        )

    @application.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        _error: RequestValidationError,
    ) -> JSONResponse:
        if request.url.path == "/api/feedback":
            message = "反馈格式无效，请检查评分和反馈内容。"
        elif request.url.path == "/api/tracking-events":
            message = "行为事件格式无效。"
        elif request.url.path.startswith("/api/conversations/") and request.url.path.endswith(
            "/messages"
        ):
            message = "追问格式无效，请检查问题内容。"
        else:
            message = "请求格式无效，请检查职位描述。"
        return JSONResponse(
            status_code=400,
            content={
                "code": "INVALID_REQUEST",
                "message": message,
            },
        )

    @application.exception_handler(Exception)
    async def handle_unexpected_error(_request: Request, error: Exception) -> JSONResponse:
        logger.exception("Unhandled backend error", exc_info=error)
        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_ERROR",
                "message": "服务暂时不可用，请稍后重试。",
            },
        )
