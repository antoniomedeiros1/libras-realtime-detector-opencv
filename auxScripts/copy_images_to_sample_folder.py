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
    # signs = ['Um']
    print(signs)

    source_dir = 'TreinamentoSample'
    
    for i in range(4):
        for sign in signs:
            source_path = f'{source_dir}/{i}/{sign}'
            num_test = 0

            for name in os.listdir(source_path):
                full_path = f'{source_path}/{name}'

                if i != 2:
                    if os.path.isfile(full_path):
                        shutil.copy(full_path, 'TrainSet')
                    elif os.path.isdir(full_path):
                        augmented_files = os.listdir(full_path)

                        test_file = augmented_files.pop(random.randrange(len(augmented_files)))
                        shutil.copy(f'{full_path}/{test_file}', 'TestSet')

                        valid_file = augmented_files.pop(random.randrange(len(augmented_files)))
                        shutil.copy(f'{full_path}/{valid_file}', 'ValidSet')

                        # print('Length', len(augmented_files))
                        for num in range(len(augmented_files)):
                            if num > 65:
                                break
                            augmented_name = augmented_files[num]
                            full_augmented_path = f'{full_path}/{augmented_name}'
                            shutil.copy(f'{full_augmented_path}', 'TrainSet')
                else:
                    if os.path.isfile(full_path):
                        if num_test < 3:
                            shutil.copy(full_path, 'TestSet')
                            num_test += 1
                        else:
                            shutil.copy(full_path, 'ValidSet')
                        # print('Num test', num_test)
                    elif os.path.isdir(full_path):
                        augmented_files = os.listdir(full_path)

                        for num in range(len(augmented_files)):
                            # print('Num', num)
                            augmented_name = augmented_files[num]
                            full_augmented_path = f'{full_path}/{augmented_name}'
                            if num < 4:
                                shutil.copy(f'{full_augmented_path}', 'TestSet')
                            elif num < 9:
                                shutil.copy(f'{full_augmented_path}', 'ValidSet')
                            else:
                                break

if __name__ == '__main__': main()
