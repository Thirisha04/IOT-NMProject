import time
import sounddevice as sd
import numpy as np
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
# Initialization of LCD
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D18)
lcd_d5 = digitalio.DigitalInOut(board.D23)
lcd_d4 = digitalio.DigitalInOut(board.D24)
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 16, 2)
# Set up the microphone
sample_rate = 44100
duration = 10 # Number of seconds to record sound
def callback(indata, frames, time, status):
 if status:
 print(status, flush=True)
def record_sound():
 with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
 sd.sleep(duration * 1000)
def analyze_sound(data):
 # Calculate the average volume
 average_volume = np.mean(np.abs(data))
 
 # Classify loudness
 if average_volume < 30:
 return "Quiet"
 elif average_volume < 60:
 return "Moderate"
 else:
 return "Loud"
# Main loop
while True:
 lcd.clear()
 lcd.message = "Listening..."
 
 # Record and analyze sound
 sound_data, overflowed = sd.rec(int(sample_rate * duration), samplerate=sample_rate, 
channels=1, dtype='int16')
 sd.wait()
 loudness = analyze_sound(sound_data)
 
 lcd.clear()
 lcd.message = f"Sound Level: {loudness}"
 time.sleep(10)
