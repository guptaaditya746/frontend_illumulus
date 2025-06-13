# /home/prims/frontend_illumulus/ai-story-exhibit/tests/unit/test_image_gen_client.py

import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
import base64
import io

from services.image_gen_client import (
    create_image_client,
    MockImageClient,
    WebisImageClient
)
# Assuming stable_diffusion.WebisAPI is the actual API client class
WEBIS_API_PATH = "services.image_gen_client.WebisAPI" # Path relative to where it's imported

def test_create_image_client_mock():
    """Test factory creates MockImageClient."""
    client = create_image_client(backend="mock")
    assert isinstance(client, MockImageClient)

def test_create_image_client_webis():
    """Test factory creates WebisImageClient."""
    with patch(f"{WEBIS_API_PATH}") as mock_webis_constructor:
        client = create_image_client(backend="webis")
        assert isinstance(client, WebisImageClient)
        mock_webis_constructor.assert_called_once() # WebisAPI takes no args in __init__

def test_create_image_client_unknown():
    """Test factory raises ValueError for unknown backend."""
    with pytest.raises(ValueError) as excinfo:
        create_image_client(backend="unknown_backend")
    assert "Unknown image backend: unknown_backend" in str(excinfo.value)

def test_mock_image_client_generate():
    """Test MockImageClient's generate method."""
    client = MockImageClient()
    prompt = "A beautiful sunset"
    image = client.generate(prompt)
    assert isinstance(image, Image.Image)
    assert image.size == (512, 512)
    assert image.mode == "RGB"

def test_webis_image_client_generate(mocker):
    """Test WebisImageClient's generate method calls the underlying API correctly."""
    mock_webis_api_instance = MagicMock()
    
    # Create a dummy 1x1 black pixel PNG image, then base64 encode it
    img = Image.new("RGB", (1, 1), color="black")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    b64_encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    mock_webis_api_instance.generate.return_value = b64_encoded_image
    
    # Patch the constructor of WebisAPI to return our mock instance
    mocker.patch(WEBIS_API_PATH, return_value=mock_webis_api_instance)
    
    client = WebisImageClient() # Constructor is patched
    
    prompt = "A futuristic city"
    result_image = client.generate(prompt)
    
    mock_webis_api_instance.generate.assert_called_once_with(prompt)
    assert isinstance(result_image, Image.Image)
    assert result_image.size == (1, 1) # Check if the decoded image matches our dummy

    # Verify content by checking a pixel (optional, but good for simple mock images)
    pixel_data = result_image.getpixel((0,0))
    assert pixel_data == (0,0,0) # Black pixel