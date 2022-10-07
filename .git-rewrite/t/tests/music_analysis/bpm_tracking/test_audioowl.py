import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt # cannot plot shit. must change the thing.
import audioowl # do not install with dependencies. check it in setup.py and install latest versions.

myMusic = "tarot_desc_acc_exceprt.wav"
# myMusic = "/root/Desktop/works/bilibili_tarot/tarot_desc_acc.wav"

from MediaInfo import MediaInfo

info = MediaInfo(filename = myMusic)
info = info.getInfo()

print(info)
# breakpoint()
audioSampleRate = info["audioSamplingRate"]
audioSampleRate = int(audioSampleRate)

waveform = audioowl.get_waveform(myMusic,sr=audioSampleRate)
data = audioowl.analyze_file(myMusic,sr=audioSampleRate) # how fucking long?

# plt.figure()
# plt.vlines(data['beat_samples'], -1.0, 1.0)
# plt.plot(waveform)
# plt.show()
# dict_keys(['sample_rate', 'duration', 'beat_samples', 'number_of_beats', 'tempo_float', 'tempo_int', 'zero_crossing', 'noisiness_median', 'noisiness_sum', 'notes', 'dominant_note'])

def getClosest(mlist,standard):
    # mlist is sorted.
    # assert mlist == list(sorted(mlist))
    queue_list = []
    last_elem = None
    for elem in mlist:
        mred = abs(elem-standard)
        queue_list.append(mred)
        if len(queue_list) > 2:
            queue_list.pop(0)
        if len(queue_list) == 2:
            #compare now.
            last_mred = queue_list[0]
            if mred >= last_mred: return last_elem
        last_elem = elem
    return last_elem



a,b,c,d = [data[k] for k in ["beat_samples","duration","sample_rate","tempo_float"]]
print(data)
breakpoint()

single_bpm_time = 60/d

bpm_times = [single_bpm_time*(2**x) for x in range(5)] #usually works.

min_beat_time = 2 # minimum beat skip time.

closest_beat_time = getClosest(bpm_times,min_beat_time)

# breakpoint()
min_outro_time = 3 # must longer than the song.
# total_samples = b*c

beat_times = [x/c for x in a if x <= c*(b - min_outro_time)] # no final cut.
# so the beats are evenly sliced.
# print(beat_times)
# breakpoint()
selected_beat_times = [0] # original beat. the startup.
for i,x in enumerate(beat_times):
    lastBeat = selected_beat_times[-1]
    if x <= lastBeat:
        continue
    ired_beat_times = beat_times[i:] # exactly what we want.
    selectedBeat = getClosest(ired_beat_times,lastBeat+closest_beat_time)
    selected_beat_times.append(selectedBeat)
print('selected beat times:')
print(selected_beat_times)

# we have to check the thing.