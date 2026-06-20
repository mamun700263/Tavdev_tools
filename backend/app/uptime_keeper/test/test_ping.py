# import pytest
# import httpx
# from app.uptime_keeper.ping import normalize_url, ping

# # @pytest.mark.asyncio
# # async def test_normalize_url_adds_https():
# #     url = "google.com"
# #     result = await normalize_url(url)
# #     assert result == "https://google.com"

# # @pytest.mark.asyncio
# # async def test_normalize_url_keeps_https():
# #     url = "https://google.com"
# #     result = await normalize_url(url)
# #     assert result == "https://google.com"

# # @pytest.mark.asyncio
# # async def test_normalize_url_keeps_https():
# #     url = "https://google.com"
# #     result = await normalize_url(url)
# #     assert result == "https://google.com"

# # @pytest.mark.asyncio
# # async def test_normalize_url_trims_spaces():
# #     url = "   google.com   "
# #     result = await normalize_url(url)
# #     assert result == "https://google.com"

# def mock_response(request):
#     return httpx.Response(
#         status_code=200,
#         content=b"OK",
#         request=request
#     )

# # @pytest.mark.asyncio
# # async def test_ping_success():
# #     transport = httpx.MockTransport(mock_response)

# #     async with httpx.AsyncClient(transport=transport) as client:
# #         result = await ping("example.com")

# #     assert result["is_up"] is True
# #     assert result["status_code"] == 200
# #     assert result["error_message"] is None
# #     assert "response_time_ms" in result
# #     assert result["checked_at"] is not None

# def mock_redirect(request):
#     return httpx.Response(
#         status_code=301,
#         headers={"location": "https://example.com"},
#         request=request
#     )
# # @pytest.mark.asyncio
# # async def test_ping_redirect():
# #     transport = httpx.MockTransport(mock_redirect)

# #     async with httpx.AsyncClient(transport=transport) as client:
# #         result = await ping("example.com")

# #     assert result["is_up"] is True
# #     assert result["status_code"] == 301

# # def mock_timeout(request):
# #     raise httpx.TimeoutException("timeout")
# # @pytest.mark.asyncio
# # async def test_ping_timeout():
# #     transport = httpx.MockTransport(mock_timeout)

# #     async with httpx.AsyncClient(transport=transport) as client:
# #         result = await ping("example.com")

# #     assert result["is_up"] is False
# #     assert result["status_code"] is None
# #     assert "timeout" in result["error_message"].lower()


# # def mock_connection_error(request):
# #     raise httpx.ConnectError("connection failed")
# # @pytest.mark.asyncio
# # async def test_ping_connection_error():
# #     transport = httpx.MockTransport(mock_connection_error)

# #     async with httpx.AsyncClient(transport=transport) as client:
# #         result = await ping("example.com")

# #     assert result["is_up"] is False
# #     assert result["status_code"] is None
