#!/usr/bin/env python3
# -*- config: utf-8 -*-

import os
import shutil
import random

def main():
    signs = '''um
dois
tres
quatro
cinco
seis
sete
oito
nove
hospital
alergia
doente
febre
frio
medico
normal
quente
remedio
sentir_mal
oi'''.splitlines()
    signs = [i.capitalize() for i in signs]
    print(signs)

    source_dir = 'Treinamento'
    destination_dir = "TreinamentoSample"

    # Define the number of random images to select for each class and number
    num_images_per_class = 5

    random.seed(67)

    # Loop through each class
    for class_name in signs:
        # Loop through each number (0, 1, 2, ...)
        for i in range(4):  # Assuming numbers go from 0 to 4
            # Create a directory for the current class and number
            class_dir = os.path.join(destination_dir, str(i), class_name)
            os.makedirs(class_dir, exist_ok=True)
            
            # Collect all images for the current class and number
            images = [filename for filename in os.listdir(source_dir) if filename.startswith(f"{class_name}{i}")]
            
            # Select random images from the collected images
            random_images = random.sample(images, min(num_images_per_class, len(images)))
            print(random_images)
            # Copy the selected random images to the destination directory
            for image in random_images:
                source_path = os.path.join(source_dir, image)
                destination_path = os.path.join(class_dir, image)
                shutil.copyfile(source_path, destination_path)

if __name__ == '__main__': main()
