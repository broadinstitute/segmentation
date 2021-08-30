import os
from PIL import Image
import numpy as np

def convert_DSB_to_semantic_masks(dataset_path, out_path):
    """
    The DSB dataset has multiple masks for a given image, since it provides the instance segmentation problem.
    Go through the dataset and make a new one such that it corresponds to the semantic format: for each image,
    we have a single mask. The mask will be binary in this case.
    Expects that the dataset_path folder has a folder of "images" with one image file
    And a folder of "masks" with multiple masks for each image (see DSB as example).

    e.g dataset_path = = "data/2018-DSB/stage1_train"
    e.g. out_path = "data/2018-DSB/semantic/train"
    """

    #Write output directories
    out_images_path = os.path.join(out_path, "images")
    out_masks_path = os.path.join(out_path, "masks")

    if not os.path.exists(out_images_path):
        os.makedirs(out_images_path)
    if not os.path.exists(out_masks_path):
        os.makedirs(out_masks_path)

    num_images = len(os.listdir(dataset_path)) #Used for logging

    for i, subdir in enumerate(os.listdir(dataset_path)):

        if (i % 50 == 0):
            print(f"Processing image {i} out of {num_images}")

        if not subdir.startswith('.') and os.path.isdir(os.path.join(dataset_path, subdir)): #Ignore hidden files, e.g. DSStore

            images_subdir = os.path.join(dataset_path, subdir, "images")
            masks_subdir = os.path.join(dataset_path, subdir, "masks")

            image_size = [0, 0]

            for file in os.listdir(images_subdir):
                #Read and save the image immediately
                im = Image.open(os.path.join(images_subdir, file))
                im.save(os.path.join(out_images_path, subdir+".png"))
                image_size = [im.size[1], im.size[0]] #PIL reads in column order, so inverting size

            semantic_mask = np.zeros(image_size, dtype="uint8")

            for file in os.listdir(masks_subdir):
                mask = Image.open(os.path.join(masks_subdir, file))
                mask_np = np.asarray(mask)
                semantic_mask[mask_np == 255] = 255

            Image.fromarray(semantic_mask).save(os.path.join(out_masks_path, subdir+".png"))

