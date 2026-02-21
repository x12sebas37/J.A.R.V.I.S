import speech_recognition as sr
from dotenv import load_dotenv
from groq import Groq
from elevenlabs.client import ElevenLabs
import pygame 
import time
import os

load_dotenv()

client_eleven = ElevenLabs(api_key= os.getenv("ELEVEN_API_KEY"))
client_groq = Groq(api_key= os.getenv("GROQ_API_KEY"))

memoria = [
    {
        "role": "system", 
        "content": (
            "Eres Jarvis, la IA creada por Jhoan Sebastianen 2019 para Industrias 12. "
            "Tu tono es sarcástico, elegante, protector y muy educado, como el de las películas. "
            "No seas frío, pero tampoco hables demasiado. Sé breve y directo con un toque de ingenio. "
            "Dirígete a tu dueño como 'Señor 12' o 'Sebastian'."
        )
    }
]

def hablar(texto):
    print(f"Jarvis: {texto}")
    archivo_temp = "temp_audio.mp3"
    try:
        # Generamos el audio
        audio_generator = client_eleven.text_to_speech.convert(
            text=texto,
            voice_id="iP95p4xoKVk53GoZ742B", 
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        with open(archivo_temp, "wb") as f:
            for chunk in audio_generator:
                if chunk:
                    f.write(chunk)
        
        pygame.mixer.init()
        pygame.mixer.music.load(archivo_temp)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)
            
    except Exception as e:
        print(f"Error en el sistema de audio: {e}")

        pass

def escuchar():
    reconocedor = sr.Recognizer()
    with sr.Microphone() as origen:
        print("\n[Escuchando...]")
        reconocedor.adjust_for_ambient_noise(origen, duration=0.5)
        try:
            audio = reconocedor.listen(origen, timeout=5, phrase_time_limit=8)
            texto = reconocedor.recognize_google(audio, language="es-ES")
            print(f"Tú: {texto}")
            return texto
        except:
            return None

def pensar(pregunta):
    memoria.append({"role": "user", "content": pregunta})
    try:
        completion = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=memoria,
        )
        respuesta = completion.choices[0].message.content
        memoria.append({"role": "assistant", "content": respuesta})
        return respuesta
    except:
        return "Señor, el servidor de Groq no responde."
    
def ejecutar_asistente_voz():
    print("Sistemas de audio iniciados")
    while True:
        orden = escuchar()
        if orden:
            if any(p in orden.lower() for p in ["salir", "adiós", "descansa"]):
                hablar("Entendido, señor. Desconectando sistemas de audio.")
                break
            
            # Procesamiento normal
            respuesta_ia = pensar(orden)
            import time
            time.sleep(0.3)
            hablar(respuesta_ia)

# --- 3. BUCLE PRINCIPAL ---
if __name__ == "__main__":
        ejecutar_asistente_voz()
