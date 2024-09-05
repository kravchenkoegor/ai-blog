import torch
from pipeline import (
  filter_similar_images,
  describe_images_moondream,
  describe_images_llava,
)

def run(folder_path: str):
  filter_similar_images(folder_path)
  
  describe_images_moondream(folder_path)
  
  # We are limited in VRAM, so we need to unload previous model
  torch.cuda.empty_cache()
  
  describe_images_llava(folder_path)
