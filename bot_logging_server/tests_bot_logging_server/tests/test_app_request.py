# pylint: disable=C0103
import pytest


@pytest.mark.asyncio
async def test_request_parsing_failed(logging_app):
    # User token must be 32 length here is 31
    r = await logging_app.post(
        "/send_logs",
        json={
            "data": {
                "user": "some",
                "pid": 1221,
                "p_name": "some pname",
                "post_time": "2020-05-05T12:22:22+00:00",
                "logs": [
                    {
                        "level": "error",
                        "msg": "msg",
                        "event_at": "2020-05-05T12:22:22+00:00",
                        "p_description": "process_user_desc",
                    }
                ],
            }
        },
        headers={
            "X-User-Token": "testtesttesttesttettesttesttest",
            "Content-Type": "application/json",
        },
    )
    async for data in r.response:
        assert data == b'{"code":400,"message":"BadRequest"}'


@pytest.mark.asyncio
async def test_request_but_no_mysql(logging_app):
    # mysql mock does not set in this project
    r = await logging_app.post(
        "/send_logs",
        json={
            "data": {
                "user": "some",
                "pid": 1221,
                "p_name": "some pname",
                "post_time": "2020-05-05T12:22:22+00:00",
                "logs": [
                    {
                        "level": "error",
                        "msg": "msg",
                        "event_at": "2020-05-05T12:22:22+00:00",
                        "p_description": "process_user_desc",
                    }
                ],
            }
        },
        headers={
            "X-User-Token": "testtesttesttesttettesttesttetst",
            "Content-Type": "application/json",
        },
    )
    async for data in r.response:
        assert data == b'{"code":500,"message":"Internal Server Error"}'
