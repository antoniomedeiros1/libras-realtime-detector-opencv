import csv
import os
import re

gs_uri_train = 'gs://sinais-libras/TrainSetHandPoints/'
gs_uri_validation = 'gs://sinais-libras/ValidSetHandPoints/'
gs_uri_test = 'gs://sinais-libras/TestSetHandPoints/'

labels = [
    'um',
    'dois',
    'tres',
    'quatro',
    'cinco',
    'seis',
    'sete',
    'oito',
    'nove',
    'hospital',
    'alergia',
    'doente',
    'febre',
    'frio',
    'medico',
    'normal',
    'quente',
    'remedio',
    'sentir mal',
    'oi'
]

train_set_files = [filename for filename in os.listdir('./TreinamentoNovo/TrainSetHandPoints')]
with open('train_set.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for file in train_set_files:
        label = re.split(r'\d+', file)[0]
        label = label.split('_')[0]
        writer.writerow([f'{gs_uri_train}{file}', label.lower()])

validation_set_files = [filename for filename in os.listdir('./TreinamentoNovo/ValidSetHandPoints')]
with open('validation_set.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for file in validation_set_files:
        label = re.split(r'\d+', file)[0]
        label = label.split('_')[0]
        writer.writerow([f'{gs_uri_validation}{file}', label.lower()])

test_set_files = [filename for filename in os.listdir('./TreinamentoNovo/TestSetHandPoints')]
with open('test_set.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for file in test_set_files:
        label = re.split(r'\d+', file)[0]
        label = label.split('_')[0]
        writer.writerow([f'{gs_uri_test}{file}', label.lower()])
