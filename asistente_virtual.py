import pyttsx3, speech_recognition as sr, pywhatkit, yfinance as yf
import pyjokes, webbrowser, datetime, wikipedia


# -----------------------------------------------------------------------------------
# VOCES DISPONIBLES PARA EL ASISTENTE
# -----------------------------------------------------------------------------------

'''engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)'''

# Voces en Español (ES - MX)
id_1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id_2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
# Voces en Inglés (Masculino - Femenino)
id_3 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
id_4 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# -----------------------------------------------------------------------------------
# ESCUCHAR MICRÓFONO Y DEVOLVER AUDIO COMO TEXTO
# -----------------------------------------------------------------------------------

def audio_a_texto():

    # Almacenar Recognizer en una variable
    r = sr.Recognizer()

    # Configurar el micrófono
    with sr.Microphone() as origen:
        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzó la grabación
        print('Iniciando grabación')

        # Guardar lo escuchado como audio
        audio = r.listen(origen)

        try:
            # Buscar en Google
            pedido = r.recognize_google(audio, language = 'es-ve')
            
            # Prueba de que ingresó el audio
            print('Dijiste: ' + pedido)

            # Devolver pedido
            return pedido
        
        # En caso de no comprender el audio
        except sr.UnknownValueError:
            # Prueba de que no comprendió el audio
            print('Lo siento, no entendí la consulta')

            # Devolver error
            return 'Sigo esperando'
        
        # En caso de no poder resolver el pedido
        except sr.RequestError:
            # Prueba de que no se puede completar la consulta
            print('Lo siento, no puedo llevar a cabo tu consulta')

            # Devolver error
            return 'Sigo esperando'
        
        # Errores inesperados
        except:
            # Prueba de error inesperado
            print('Algo ha esalido mal, intenta de nuevo')

            # Devolver error
            return 'Sigo esperando'
        

# -----------------------------------------------------------------------------------
# FUNCIONES PARA QUE EL ASISTENTE HABLE
# -----------------------------------------------------------------------------------

def hablar(mensaje):

    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id_2)

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar el día
def pedir_dia():

    # Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear variable para el día de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario con nombres de días
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    
    # Decir el día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# Informar la hora actual
def pedir_hora():

    # Crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'Actualmente son las {hora.hour} con {hora.minute} y {hora.second} segundos'

    # Decir la hora
    hablar(hora)


# Función saludo inicial
def saludo_inicial():

    # Variación del saludo según la hora
    hora = datetime.datetime.now()
    if hora.hour < 5 or hora.hour > 19:
        momento = 'Buenas noches'
    elif 5 <= hora.hour < 12:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    # Decir el saludo
    hablar(f'{momento}, soy Sabina, tu asistente personal. ¿Cómo puedo ayudarte?')


# -----------------------------------------------------------------------------------
# FUNCIÓN CENTRAL DEL ASISTENTE
# -----------------------------------------------------------------------------------

def realizar_pedido():

    # Activar saludo inicial
    saludo_inicial()

    # Variable de corte
    comenzar = True

    # Bucle principal
    while comenzar:
        
        # Activar el micrófono y guardar el pedido en un string
        pedido = audio_a_texto().lower()

        # Abrir YouTube
        if 'abrir youtube' in pedido or 'abre youtube' in pedido:
            hablar('Con gusto, abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
            continue

        # Abrir navegador
        elif 'abrir navegador' in pedido or 'abre el navegador' in pedido:
            hablar('Con gusto, abriendo el navegador')
            webbrowser.open('https://www.google.com')
            continue

        # Decir el día
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue

        # Decir la hora
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue

        # Buscar en Wikipedia
        elif 'busca en wikipedia' in pedido or 'buscar en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            if 'busca en wikipedia' in pedido:
                pedido = pedido.replace('busca en wikipedia', '')
            else:
                pedido = pedido.replace('buscar en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences = 1)
            hablar('La búsqueda dio el siguiente resultado:')
            hablar(resultado)
            continue

        # Buscar en Google o internet
        elif 'busca en google' in pedido or 'busca en internet' in pedido:
            hablar('Con gusto. Buscando')
            if 'busca en google' in pedido:
                pedido = pedido.replace('busca en google', '')
            else: pedido = pedido.replace('busca en internet', '')

            pywhatkit.search(pedido)
            continue

        # Reproducir video en YouTube
        elif 'reproducir' in pedido or 'reproduce' in pedido:
            hablar('Excelente idea, buscando')
            pywhatkit.playonyt(pedido)
            continue

        # Contar un chiste
        elif 'broma' in pedido or 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue

        # Obtener información de mercados financieros
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'El precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Lo siento, no la he encontrado ')
                continue

        # Tomar captura de pantalla
        elif 'captura de pantalla' in pedido or 'captura a la pantalla' in pedido:
            hablar('En seguida, tomando captura de pantalla')
            nombre_archivo = 'pywhatkit_screenshot'
            pywhatkit.take_screenshot(nombre_archivo, 2)
            hablar(f'Captura tomada con el nombre {nombre_archivo}')

        # Finalizar asistente
        elif 'eso es todo' in pedido:
            hablar('Fue un gusto ayudarte, hasta luego')
            break


realizar_pedido()
