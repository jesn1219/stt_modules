import torch
import zipfile
import torchaudio
from glob import glob
import record
import time
import pickle 
import sys
import unpickler
from src.silero import utils

device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU


model = None
decoder = None
utils_ob = None

#model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt', language='en', device=device)


def save_model() :
    global model, decoder, utils_ob
    model.save("./models/model.pk")
    torch.save(decoder,"./models/decoder")
    torch.save(utils_ob,'./models/utils')


def load_model() :
    global model, decoder, utils_ob
    model = torch.jit.load("./models/model.pk")
    decoder = torch.load("./models/decoder")
    utils_ob = torch.load("./models/utils")    

load_model()

(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils_ob  # see function signature for details

# download a single file, any format compatible with TorchAudio (soundfile backend)
#torch.hub.download_url_to_file('https://opus-codec.org/static/examples/samples/speech_orig.wav',
#                               dst ='speech_orig.wav', progress=True)
#test_files = glob('speech_orig.wav')


while True :
    record.start()
    time.sleep(4)
    record.stop()
    test_files = glob('test.wav')

    batches = split_into_batches(test_files, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)

    output = model(input)
    for example in output:
        print(decoder(example.cpu()))