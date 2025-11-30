import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_proxy_no_auth(client: AsyncClient):
    response = await client.post(
        "/api/v1/proxy/",
        json={"prompt": "hello"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_proxy_invalid_auth(client: AsyncClient):
    response = await client.post(
        "/api/v1/proxy/",
        headers={"X-API-Key": "invalid-key"},
        json={"prompt": "hello"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_proxy_success(client: AsyncClient):
    # Create app to get key
    create_res = await client.post(
        "/api/v1/apps/",
        json={"name": "proxy-test-app"}
    )
    api_key = create_res.json()["api_key"]

    # Mock the agent graph to bypass actual security checks (which require LLM/GCP)
    with patch("app.agents.graph.agent_graph.ainvoke") as mock_invoke:
        mock_invoke.return_value = {
            "input": {"prompt": "hello world"},
            "security_score": 0.1,
            "is_blocked": False,
            "block_reason": None
        }
        
        # Call proxy
        response = await client.post(
            "/api/v1/proxy/",
            headers={"X-API-Key": api_key},
            json={"prompt": "hello world"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "proxy-test-app"
    assert data["received_body"]["prompt"] == "hello world"
