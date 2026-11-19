import ntptime, time
from machine import Pin
import time

ntptime.settime()

def tiempo_actual():
    tiempo = time.localtime(time.time() - (3 * 3600))
    lista_tiempo = [tiempo.tm_year,tiempo.tm_mon,tiempo.tm_mday,tiempo.tm_hour,tiempo.tm_min]
    return lista_tiempo

def webpage():
    html = '''
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alarma en web</title>
    <style>body {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: Arial, Helvetica, sans-serif;
        background-image: linear-gradient(to left, white, rgb(149, 205, 255));
    }
    
    .entradas{
        flex-direction: column;
        display: flex;
        gap: 20px;
    }

    .ttl1 { font-size: 45px; font-family: "Pusab"; src: url("PUSAB.ttf") format('truetype'); }
    .entradas { align-items: center; }
    #fecha { font-family: Arial, Helvetica, sans-serif; font-size: 18px; padding: 15px 15px; border-radius: 15px; border: black; }
    #hora { font-family: Arial, Helvetica, sans-serif; font-size: 18px; padding: 15px 15px; border-radius: 15px; border: none; }
    #send { font-family: Arial, Helvetica, sans-serif; font-size: 18px; font-weight: bold; padding: 20px 25px; background-image: linear-gradient(to left, rgb(218, 218, 218), rgb(150, 148, 148)); border: none; border-radius: 15px; transition-duration: 250ms; }
    #send:hover { transform: scale(1.15); }
    #send:active { transform: scale(0.95); }
    </style>
</head>
<body>
    <div>
        <h1 class="ttl1">Hora y fecha actual</h1>
        <div class="entradas">
            <input type="date" Id="fecha">
            <input type="time" Id="hora">
            <input type="button" value="Enviar" Id="send">
        </div>
    </div>
    <script>
        const ahora = new Date();
        const year = ahora.getFullYear();
        const month = String(ahora.getMonth() + 1).padStart(2, '0');
        const day = String(ahora.getDate()).padStart(2, '0');
        document.getElementById('fecha').value = `${year}-${month}-${day}`;

        const hour = String(ahora.getHours()).padStart(2, '0');
        const minute = String(ahora.getMinutes()).padStart(2, '0');
        document.getElementById("hora").value = `${hour}:${minute}`;

        const sendBtn = document.getElementById('send');

        sendBtn.addEventListener("click", () => {
            const SelectedDate = document.getElementById("fecha").value;
            const SelectedHour = document.getElementById("hora").value;
        });

        document.getElementById('send').onclick = (event) => {
            event.preventDefault();

            const fecha = document.getElementById('fecha').value
            const hora = document.getElementById("hora").value.replaceAll(":","-")
            
            const resultado = fecha + "-" + hora
            console.log(resultado)

            const url = window.location.href.split('/update?')[0];
            document.location.href = url + '/update?' + resultado;
        }
        
    </script>
</body>
</html>
        '''
    return html

def obtener_parametros(request):
    try:
        request = request.decode('utf-8')
    except:
        pass

    lineas = request.split(' ')
    linea_correcta = None
    for linea in lineas:
        if '/update?' in linea:
            linea_correcta = linea
            break

    if not linea_correcta:
        return []
    
    query = linea_correcta.split('/update?', 1)[1]
    parametros = []
    for item in query.split('-'):
        parametros.append(item)
    
    return parametros

def sonar_alarma():


buzzer = Pin(26, Pin.OUT)

while True:
    buzzer.value(1)
    time.sleep(0.01)
    buzzer.value(0)

def iniciar_alarma(fecha):
    print(f"Fecha de la pagina:{fecha}")
    print(f"Fecha de la placa:{tiempo_actual()}\n")
    if fecha == tiempo_actual():
        sonar_alarma()
    pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(f'Entro una conexion desde {str(addr)}')
    request = conn.recv(1024)
    request = str(request)
    print(f'Contenido = {request}')

    parametros = obtener_parametros(request)

    iniciar_alarma(parametros)

    response = webpage()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type text/html\n')
    conn.send('Conecction: close\n\n')
    conn.sendall(response)
    conn.close()