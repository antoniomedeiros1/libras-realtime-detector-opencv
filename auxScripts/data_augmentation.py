#!/usr/bin/env python3
# -*- config: utf-8 -*-

import Augmentor
import os

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
        if i == 2:
            sample_size = 9
        else:
            sample_size = 22
        for sign in signs:
            p = Augmentor.Pipeline(f'{source_dir}/{i}/{sign}')
            p.rotate(probability=0.5, max_left_rotation=10, max_right_rotation=10)
            p.zoom(probability=0.2, min_factor=1.1, max_factor=1.2)
            p.random_color(probability=0.2,min_factor=0.5,max_factor=1.0)
            p.random_contrast(probability=0.2,min_factor=0.8,max_factor=1)
            p.skew_tilt(probability=0.5,magnitude=0.2)
            p.shear(probability=0.2, max_shear_left=10, max_shear_right=10)
            p.flip_left_right(probability=0.2)
            p.random_distortion(probability=0.5, grid_width=4, grid_height=4, magnitude=8)
            p.sample(sample_size)

if __name__ == '__main__': main()
