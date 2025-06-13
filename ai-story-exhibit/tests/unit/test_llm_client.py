# /home/prims/frontend_illumulus/ai-story-exhibit/tests/unit/test_llm_client.py

import pytest
from unittest.mock import patch, MagicMock
from services.llm_client import (
    create_llm_client,
    MockLLMClient,
    APIBaseClient,
    BaseClient
)
# Assuming modules.clients.llm_client.LLMClient is the actual API client class
# If the path is different, adjust the patch target accordingly.
LLM_API_CLIENT_PATH = "modules.clients.llm_client.LLMClient"

def test_create_llm_client_mock():
    """Test factory creates MockLLMClient."""
    client = create_llm_client(backend="mock")
    assert isinstance(client, MockLLMClient)

def test_create_llm_client_api():
    """Test factory creates APIBaseClient."""
    # We patch the APIClient to avoid actual initialization during this factory test
    with patch(f"{LLM_API_CLIENT_PATH}") as mock_api_client_constructor:
        client = create_llm_client(backend="api", config_path="dummy/path.yaml")
        assert isinstance(client, APIBaseClient)
        mock_api_client_constructor.assert_called_once_with(config_path="dummy/path.yaml")

def test_create_llm_client_unknown():
    """Test factory raises ValueError for unknown backend."""
    with pytest.raises(ValueError) as excinfo:
        create_llm_client(backend="unknown_backend")
    assert "Unknown LLM backend: unknown_backend" in str(excinfo.value)

def test_mock_llm_client_generate():
    """Test MockLLMClient's generate method."""
    client = MockLLMClient()
    prompt = "A cat sat on a mat"
    genre = "Fable"
    elements = ["talking cat", "magic mat"]
    expected_seed = f"{prompt}. Genre: {genre}. Elements: {', '.join(elements)}."
    expected_output = f"{expected_seed} And so, this story begins…"
    
    result = client.generate(prompt=prompt, genre=genre, elements=elements)
    assert result == expected_output

def test_api_base_client_generate(mocker):
    """Test APIBaseClient's generate method calls the underlying client correctly."""
    mock_llm_api_instance = MagicMock()
    mock_llm_api_instance.send.return_value = "Generated text from API"
    
    # Patch the constructor of the underlying APIClient to return our mock instance
    mocker.patch(f"{LLM_API_CLIENT_PATH}", return_value=mock_llm_api_instance)
    
    client = APIBaseClient(config_path="dummy/config.yaml") # Config path is for constructor
    
    prompt = "Tell me a story."
    kwargs = {
        "stream": False,
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.9,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.2,
        "agent_name": "test_agent"
    }
    
    expected_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    result = client.generate(prompt, **kwargs)
    
    assert result == "Generated text from API"
    mock_llm_api_instance.send.assert_called_once_with(
        messages=expected_messages,
        **kwargs # The client.send method expects these kwargs directly
    )