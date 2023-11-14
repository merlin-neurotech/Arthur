import UnicornPy
from neurol import streams
from neurol.connect_device import get_lsl_EEG_inlets
from neurol.BCI import generic_BCI, automl_BCI
from neurol import BCI_tools
from neurol.models import classification_tools
from sys import exit
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import openai
import time




clb = lambda stream:  BCI_tools.band_power_calibrator(stream, ['EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 'EEG 5', 'EEG 6', 'EEG 7', 'EEG 8'], 'unicorn', bands=['beta'],
                                                        percentile=5, recording_length=10, epoch_len=1, inter_window_interval=0.25)

gen_tfrm = lambda buffer, clb_info: BCI_tools.band_power_transformer(buffer, clb_info, ['EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 'EEG 5', 'EEG 6', 'EEG 7', 'EEG 8'], 'unicorn', bands=['beta'],
                                                        epoch_len=1)

global xs, EEG1, EEG2, EEG3, EEG4, EEG5, EEG6, EEG7, EEG8                                                   
xs = []
EEG1 = []
EEG2 = []
EEG3 = []
EEG4 = []
EEG5 = []
EEG6 = []
EEG7 = []
EEG8 = []

def clf(clf_input, clb_info):

    clf_input = clf_input[:clb_info.shape[0]]

    #EEG1.append(clf_input[0])
    EEG1.append(clf_input[0])
    EEG2.append(clf_input[1])
    EEG3.append(clf_input[2])
    EEG4.append(clf_input[3])
    EEG5.append(clf_input[4])
    EEG6.append(clf_input[5])
    EEG7.append(clf_input[6])
    EEG8.append(clf_input[7])
    xs.append(len(EEG1))

    binary_label = classification_tools.threshold_clf(clf_input, clb_info, clf_consolidator='all')

    label = classification_tools.decode_prediction(
    binary_label, {True: 'HIGH', False: 'LOW'})
 
    return label

def plot_waves(x, EEG):
    names = ['EEG1','EEG2','EEG3','EEG4','EEG5','EEG6','EEG7','EEG8']
    plt.figure()
    for i in range(8):
        plt.plot(x, EEG[i], label=names[i])
    plt.xlabel('Measurements (time)')
    plt.ylabel('Beta Wave Activity')
    plt.show()


streams1 = resolve_stream("name='Unicorn'")
inlet = StreamInlet(streams1[0])
stream = streams.lsl_stream(inlet, buffer_length=1024)



GPT_Generic = generic_BCI(clf, transformer=gen_tfrm, action=print, calibrator=clb)
GPT_Generic.calibrate(stream)
GPT_Generic.run(stream)
