import os
import tempfile

import face_recognition
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Configure CORS settings
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/detect-face")
async def detect_face(files: list[UploadFile]):
    try:
        success_list=[]
        for file in files:
            # Check if the uploaded file is an image
            if not file.content_type.startswith("image/"):
                return JSONResponse(
                    status_code=400, content={"error": "File must be an image."}
                )
            if file.content_type not in ["image/jpeg", "image/png"]:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Unsupported image format. Only JPEG and PNG are allowed."
                    },
                )
            # Ensure the directory for temporary files exists
            os.makedirs(tempfile.gettempdir(), exist_ok=True)
            # Check if the file size is within limits (e.g., 5MB)
            if file.size > 5 * 1024 * 1024:  # 5 MB limit
                return JSONResponse(
                    status_code=400,
                    content={"error": "File size exceeds the limit of 5MB."},
                )
            # Save uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            # Load image and detect faces
            image = face_recognition.load_image_file(tmp_path)
            boxes = face_recognition.face_locations(image, model="hog")

            # Cleanup
            os.remove(tmp_path)

            if not boxes:
                return JSONResponse(status_code=400, content={"error": "No face detected."})

            success_list.append({
                "filename": file.filename,
                "boxes": boxes
            })

        return {"success_list": success_list} 

    except Exception:
        return JSONResponse(
            status_code=500, content={"error": "Could not detect faces"}
        )


@app.post("/encode-face")
async def encode_face(files: list[UploadFile]):
    try:
        knownEncodings = []
        for file in files:
            # Check if the uploaded file is an image
            if not file.content_type.startswith("image/"):
                return JSONResponse(
                    status_code=400, content={"error": "File must be an image."}
                )
            if file.content_type not in ["image/jpeg", "image/png"]:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Unsupported image format. Only JPEG and PNG are allowed."
                    },
                )
            # Ensure the directory for temporary files exists
            os.makedirs(tempfile.gettempdir(), exist_ok=True)
            # Check if the file size is within limits (e.g., 5MB)
            if file.size > 5 * 1024 * 1024:  # 5 MB limit
                return JSONResponse(
                    status_code=400,
                    content={"error": "File size exceeds the limit of 5MB."},
                )
            print(file.filename)
            # Save uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            # Load image and encode
            image = face_recognition.load_image_file(tmp_path)
            boxes = face_recognition.face_locations(image, model="hog")
            encodings = face_recognition.face_encodings(image, boxes)
            for encoding in encodings:
                knownEncodings.append(encoding.tolist())

            # Cleanup
            os.remove(tmp_path)

        if not knownEncodings:
            return JSONResponse(status_code=400, content={"error": "No face detected."})

        return {"encoding": knownEncodings}  # return all face encodings

    except Exception:
        return JSONResponse(
            status_code=500, content={"error": "Could not generate face encodings"}
        )
