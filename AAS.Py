import tkinter as tk
import pyaudio
import numpy as np
import threading

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Global gain variable (default = 1.0 = no boost)
gain = 1.0
running = True

def audio_loop():
    global gain, running
    p = pyaudio.PyAudio()

    stream_in = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

    stream_out = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

    while running:
        try:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            boosted = np.clip(audio_data * gain, -32768, 32767).astype(np.int16)
            stream_out.write(boosted.tobytes())
        except Exception as e:
            print("Error:", e)

    stream_in.stop_stream()
    stream_in.close()
    stream_out.stop_stream()
    stream_out.close()
    p.terminate()

def start_audio_thread():
    thread = threading.Thread(target=audio_loop)
    thread.daemon = True
    thread.start()

def set_gain(val):
    global gain
    gain = float(val)

def on_close():
    global running
    running = False
    root.destroy()

# Build GUI
root = tk.Tk()
root.title("Mic Booster")

slider = tk.Scale(root, from_=1, to=99, resolution=0.1,
                  orient=tk.HORIZONTAL, label="Mic Boost",
                  command=set_gain)
slider.set(1.0)
slider.pack(padx=20, pady=20)

root.protocol("WM_DELETE_WINDOW", on_close)

start_audio_thread()
root.mainloop()
