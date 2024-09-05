import os
from diffimg import diff
from glob import glob

# Define a threshold value for image difference comparison
THRESHOLD = 0.1  

def get_image_difference(image1_path, image2_path):
  """
  Compare two images and determine if they are different based on a predefined threshold.
  
  :param image1_path: Path to the first image.
  :param image2_path: Path to the second image.
  :return: True if the images are different by more than the threshold, False otherwise.
  """

  num_diff = diff(
    im1_file=image1_path, 
    im2_file=image2_path, 
    delete_diff_file=True,
  )
  return num_diff > THRESHOLD

def filter_images(images):
  """
  Filter a list of images, keeping only those that are different from previously processed images.
  
  :param images: List of image file paths to be processed.
  :return: List of image file paths that are considered different from previously processed images.
  """

  result = dict()  # Initialize a dictionary to store image differences
  
  for index, image in enumerate(images):
    # For the first image, always add it to the result as different
    if index == 0:
      result[image] = True
      continue
    
    result_keys = list(result.keys())  # Get a list of previously processed image paths
    
    is_different = True  # Assume the current image is different by default
    
    for key in result_keys:
      if not get_image_difference(image, key):
        is_different = False  # Update is_different if any comparison finds the images are not different
        break  # Exit the loop if a similar image is found
    
    result[image] = is_different  # Store the result for the current image
  
  # Return a list of image paths that are considered different
  return [key for key, value in result.items() if value]

def filter_similar_images(folder_path):
  """
  Process all images in a given folder and filter them.
  
  :param folder_path: Path to the folder containing images.
  """

  images = glob(os.path.join(folder_path, '*.jpg'))
  filtered_images = filter_images(images)
  
  # Print the total number of images and the number of filtered images
  print(f'All images: {len(images)}, filtered images: {len(filtered_images)}')
    