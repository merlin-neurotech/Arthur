import UnicornPy
import neurolArthur
import time
from pylsl import StreamInlet, resolve_stream
from neurolArthur import streams
from neurolArthur.connect_device import get_lsl_EEG_inlets
from neurolArthur.BCI import generic_BCI, automl_BCI
from neurolArthur import BCI_tools
from neurolArthur.models import classification_tools

clb = lambda stream:  BCI_tools.band_power_calibrator(stream, ['EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 'EEG 5', 'EEG 6', 'EEG 7', 'EEG 8'], 'unicorn', bands=['alpha_low', 'alpha_high'],
                                                        percentile=10, recording_length=10, epoch_len=1, inter_window_interval=0.25)
gen_tfrm = lambda buffer, clb_info: BCI_tools.band_power_transformer(buffer, clb_info, ['EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 'EEG 5', 'EEG 6', 'EEG 7', 'EEG 8'], 'unicorn', bands=['alpha_low', 'alpha_high'],
                                                        epoch_len=1)

def clf(clf_input, clb_info):

    clf_input = clf_input[:clb_info.shape[0]]



    binary_label = classification_tools.threshold_clf(clf_input, clb_info, clf_consolidator='all')

    label = classification_tools.decode_prediction(
    binary_label, {True: 'HIGH', False: 'LOW'})
 
    return label

streams1 = resolve_stream("name='Unicorn'")
inlet = StreamInlet(streams1[0])
stream = streams.lsl_stream(inlet, buffer_length=1024)
concentration1 = concentration(run_length = 60, verbose = False)
concentration_BCI = generic_BCI(clf, transformer=gen_tfrm, action=concentration1.updateCondentration, calibrator=clb)
concentration_BCI.calibrate(stream)
concentration_BCI.run(stream)

#for every 100 lows in a row =+ 1, if there is +5 notifiy the user, for every 100 highes rest to 0
class concentration:
      def __init__(self, run_length=60, verbose=False):
        self.concentration_high = 0 
        self.concentration_low = 0 
        self.concnetration_sum = 0
        self.verbose = verbose
        self.start_time = None
        self.run_length = run_length
        self.timer_start = False
  def updateConcentration(self, EEG_output):

        if not self.timer_start:
            self.start_time = time.time()
            self.timer_start = True

        current_time = time.time()

        if current_time - self.start_time > self.run_length
            print("Time's up!")
            exit() 
    
        if EEG_output == 'LOW':
            self.concentration_low += 1
            self.concentration_high = 0
            if self.concentration_low == 100
              self.concentration_sum += 1
              self.concentration_low = 0
        elif EEG_output == 'HIGH':
            self.concentration_high += 1
            self.concentration_low = 0
            if self.concentration_high == 100
              self.concentration_sum -= 1
              self.concentration_high = 0
        if self.concentration_sum == 5
            print("Concentration has fallen too much")
            exit()
          
            
            

#no interval notications, 
