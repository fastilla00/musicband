import pygame.midi
import time

# Инициализация музыкального модуля
def initialize_music():
    pygame.midi.init()
    global midi_out
    midi_out = pygame.midi.Output(pygame.midi.get_default_output_id())

# Генерация музыки на основе параметров
def generate_music(params):
    pitch = params.get("pitch", 60)  # Нота (MIDI pitch)
    volume = int(params.get("volume", 0.5) * 127)  # Громкость (0-127)
    tempo = params.get("tempo", 120)  # Темп в ударах в минуту

    # Воспроизведение ноты
    midi_out.note_on(pitch, volume)
    time.sleep(60 / tempo)  # Продолжительность ноты зависит от темпа
    midi_out.note_off(pitch, volume)

# Остановка музыкального модуля
def stop_music():
    midi_out.close()
    pygame.midi.quit()
