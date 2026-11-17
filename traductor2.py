
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random

# CONFIGURACION DEL JUEGO

duration = 5
sample_rate = 44100

recognizer = sr.Recognizer()

# Palabras organizadas por dificultad
words_by_level = {
    "facil": [
        "gato", "perro", "manzana", "leche", "sol"
    ],

    "medio": [
        "banano", "escuela", "amigo", "ventana", "amarillo"
    ],

    "dificil": [
        "tecnologia", "universidad", "informacion",
        "pronunciacion", "imaginacion"
    ]
}

# Traducciones correctas
translations = {
    "gato": "cat",
    "perro": "dog",
    "manzana": "apple",
    "leche": "milk",
    "sol": "sun",

    "banano": "banana",
    "escuela": "school",
    "amigo": "friend",
    "ventana": "window",
    "amarillo": "yellow",

    "tecnologia": "technology",
    "universidad": "university",
    "informacion": "information",
    "pronunciacion": "pronunciation",
    "imaginacion": "imagination"
}

# VARIABLES DEL JUEGO

puntaje = 0
puntos_por_palabra = 10

print("\n ")
print("       🎮 HABLA CORRECTO 🎮")
print(" ")
print("¡Bienvenido al juego de pronunciación!")
print("Aprende inglés mientras te diviertes.")
print(" ")

# SELECCION DE DIFICULTAD

print("\nSelecciona tu nivel de dificultad:")
print("1. Fácil")
print("2. Medio")
print("3. Difícil")

niveles = {
    "1": "facil",
    "2": "medio",
    "3": "dificil"
}

while True:
    opcion = input("\nElige una opción (1, 2 o 3): ")

    if opcion in niveles:
        nivel = niveles[opcion]
        break
    else:
        print("⚠️ Opción incorrecta. Intenta nuevamente.")

# Seleccionar las palabras del nivel
palabras = random.sample(words_by_level[nivel], 5)

# INFORMACION DE LA PARTIDA

total_rondas = len(palabras)
ronda = 0

puntaje_maximo = total_rondas * puntos_por_palabra

print("\n ")
print("🎯 NIVEL SELECCIONADO:", nivel.upper())
print("📚 Palabras por responder:", total_rondas)
print("⭐ Puntos máximos:", puntaje_maximo)
print(" ")

input("\nPresiona ENTER para comenzar...")

# DESARROLLO DEL JUEGO

for palabra_espanol in palabras:

    ronda += 1
    respuesta_correcta = translations[palabra_espanol]

    print("\n ")
    print(f"📍 RONDA {ronda} DE {total_rondas}")
    print(" ")

    print("\nTraduce esta palabra al inglés:")
    print("🇪🇸", palabra_espanol.upper())

    input("\nPresiona ENTER cuando estés listo...")

    try:
        # Grabar voz
        print("\n🎤 ¡Habla ahora!")

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        # Guardar grabación
        wav.write("output.wav", sample_rate, recording)

        print("✅ Grabación completada.")
        print("🔎 Reconociendo tu respuesta...")

        # Reconocer voz en inglés
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        respuesta = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        respuesta = respuesta.lower().strip()

        print("\n🗣️ Tu respuesta:", respuesta)

        # Comprobar respuesta
        if respuesta == respuesta_correcta:

            print("🎉 ¡EXCELENTE! Respuesta correcta.")
            print("⭐ Has ganado 10 puntos.")

            puntaje += puntos_por_palabra

        else:

            print("❌ Respuesta incorrecta.")
            print("💡 Respuesta correcta:", respuesta_correcta)
            print("⭐ Has ganado 0 puntos.")

    except sr.UnknownValueError:

        print("⚠️ No se pudo reconocer tu voz.")
        print("💡 Intenta pronunciar más claramente.")
        print("⭐ Has ganado 0 puntos.")

    except sr.RequestError as e:

        print("❌ Error en el servicio de reconocimiento:", e)
        print("Esta ronda no pudo ser evaluada.")

    except Exception as e:

        print("❌ Error durante la grabación:", e)
        print("Esta ronda no pudo ser evaluada.")

    # Mostrar progreso
    print("\n📊 PROGRESO ACTUAL")
    print("Puntos obtenidos:", puntaje)
    print("Puntos máximos:", puntaje_maximo)


# FIN DEL JUEGO Y EVALUACION

print("\n")
print(" ")
print("       🏆 FIN DEL JUEGO 🏆")
print(" ")

print("\n📊 RESULTADOS FINALES")
print(" ")
print("🎯 Nivel jugado:", nivel.upper())
print("⭐ Puntos obtenidos:", puntaje)
print("🏅 Puntos máximos:", puntaje_maximo)

# Calcular porcentaje
porcentaje = (puntaje / puntaje_maximo) * 100

print("📈 Porcentaje de aciertos:", porcentaje, "%")

print(" ")

# Evaluación del jugador
if porcentaje == 100:
    print("PERFECTO! Dominas este nivel.")

elif porcentaje >= 80:
    print("¡Excelente trabajo! Sigue practicando.")

elif porcentaje >= 60:
    print("Buen trabajo, Puedes mejorar.")

elif porcentaje >= 40:
    print("Vas por buen camino. ¡No te rindas!")

else:
    print("Necesitas practicar un poco más.")

print("\nGracias por jugar HABLA CORRECTO.")
print("¡Sigue aprendiendo inglés! 🇬🇧")
print(" ")