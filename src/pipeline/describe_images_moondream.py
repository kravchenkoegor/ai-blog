import os
import torch
from glob import glob
from PIL import Image
from transformers import (
  AutoModelForCausalLM,
  AutoTokenizer,
)

def describe_images_moondream(folder_path):
  """
  Describe images in the specified folder using the Moondream model.

  :param folder_path: Path to the folder containing images.
  """

  # Set the default device and dtype
  device, dtype = 'cpu', torch.float32

  # Check if CUDA (GPU) is available and set device and dtype accordingly
  if torch.cuda.is_available():
    device, dtype = 'cuda', torch.float16
  # Check if Metal Performance Shaders (MPS) is available for Apple devices
  elif torch.backends.mps.is_available():
    device, dtype = 'mps', torch.float16

  # Define model ID and revision
  model_id = 'vikhyatk/moondream2'
  revision = '2024-07-23'  # The latest version as of 4th Sep 2024

  # Load the pre-trained model with FlashAttention2 optimization
  model = AutoModelForCausalLM.from_pretrained(
    model_id,
    attn_implementation='flash_attention_2',
    revision=revision,
    torch_dtype=dtype,
    trust_remote_code=True
  ).to(device=device)

  # Load the pre-trained tokenizer
  tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    revision=revision
  )

  # Find all images in the specified folder
  images = glob(os.path.join(folder_path, '*.jpg'))
  
  for image_path in images:
    image = Image.open(image_path)

    # Encode the image using the model
    encoded_image = model.encode_image(image)

    # Generate a description for the image
    answer = model.generate(
      image_embeds=encoded_image,
      prompt='<image>\n\nQuestion: Describe this image.\n\nAnswer:',
      tokenizer=tokenizer,
      max_new_tokens=128
    )[0].strip()

    # Append the generated description to a text file
    with open(os.path.join(folder_path, 'description_moondream.txt'), 'a') as txt_file:
      txt_file.write(answer + '\n')
          
  print(f'Generated descriptions for {len(images)} images')
  