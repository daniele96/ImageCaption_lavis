from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
import torch
from lavis.models import load_model_and_preprocess

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
model, vis_processors, _ = load_model_and_preprocess(
    name="blip_caption", model_type="base_coco", is_eval=True, device=device
)

@app.post("/caption")
async def caption_image(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    image = vis_processors["eval"](image).unsqueeze(0).to(device)
    caption = model.generate({"image": image})
    return {"caption": caption[0]}
