import shutil
import time
import io
from fastapi.testclient import TestClient
from app.main import BASE_DIR, UPLOAD_DIR, app, get_settings
from PIL import Image, ImageChops

client = TestClient(app)

# Have to name the test function with 'test_' prefix for pytest to recognize it

def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']
    assert "Code On!" in response.text
    assert "MadhushankhaDeS" in response.text

def test_invalid_image_upload():
    response = client.post("/")
    assert response.status_code == 422  # Unprocessable Entity for missing file
    assert "application/json" in response.headers['content-type']

def test_echo_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/img-echo/", files={"file": open(path, 'rb')})
        if img is None:
            assert response.status_code == 400
        else:
            # Returning a valid image
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()
            assert difference is None
    # time.sleep(3)
    shutil.rmtree(UPLOAD_DIR)


def test_prediction_upload():
    img_saved_path = BASE_DIR / "images"
    settings = get_settings()
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None

        response = client.post("/", files={"file": open(path, 'rb')}, headers={"Authorization": f"JWT {settings.app_auth_token}"})
        if img is None:
            assert response.status_code == 400
        else:
            # Returning a valid image
            assert response.status_code == 200
            data = response.json()
