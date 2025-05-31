import os
import tempfile

import face_recognition
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/encode-face")
async def encode_face(file: UploadFile):
    try:
        # Check if the uploaded file is an image
        if not file.content_type.startswith("image/"):
            return JSONResponse(
                status_code=400, content={"error": "File must be an image."}
            )
        if file.content_type not in ["image/jpeg", "image/png"]:
            return JSONResponse(
                status_code=400,
                content={"error": "Unsupported image format. Only JPEG and PNG are allowed."},
            )
        # Ensure the directory for temporary files exists
        os.makedirs(tempfile.gettempdir(), exist_ok=True)
        # Check if the file size is within limits (e.g., 5MB)
        if file.size > 5 * 1024 * 1024:  # 5 MB limit
            return JSONResponse(
                status_code=400, content={"error": "File size exceeds the limit of 5MB."}
            )
        # Save uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Load image and encode
        image = face_recognition.load_image_file(tmp_path)
        encodings = face_recognition.face_encodings(image)

        # Cleanup
        os.remove(tmp_path)

        if not encodings:
            return JSONResponse(status_code=400, content={"error": "No face detected."})

        return {"encoding": encodings[0].tolist()}  # return first face encoding

    except Exception:
        return JSONResponse(
            status_code=500, content={"error": "Could not generate face encodings"}
        )
