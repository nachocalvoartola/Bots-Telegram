from telethon import TelegramClient, events
from typing import List
import re
import asyncio
import emoji

# Parámetros de las entradas
NUM_ORDENES = 2
DIST_ORDENES = 2

# Tiempo de espera entre mensajes en segundos
TIEMPO_ESPERA = 5


# Credenciales de la API
API_ID = "242684"  # Reemplazar con tu API ID
API_HASH = "7a6b808006eaaf408646bd914c0b2eec"  # Reemplazar con tu API Hash

# Teléfono del usuario que accederá al canal
PHONE = "+34658936280"  # Reemplazar con tu número (incluido el código del país)

# ID o nombre de usuario del canal de origen y canal de destino

# SOURCE_CHANNEL = -1002244724483  # Canal recibir señales BEN
SOURCE_CHANNEL = -1002460410884  # Canal recibir señales de prueba
DEST_CHANNEL = -1002202028058  # Canal envio MT4 BEN


SESSION_NAME = "bot_reenvio_gold_BEN"

# Crear cliente de Telethon
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


# Eliminar todos los emoticonos
def eliminar_emoticonos(texto):
    return emoji.replace_emoji(texto, replace="")


# Eliminar las líneas en blanco
def eliminar_lineas_en_blanco(texto):
    return "\n".join(filter(str.strip, texto.splitlines()))


# Función para enviar la primera orden de compra o venta a mercado
def envio_orden_mercado(text: str) -> str:
    if "buy" in text:
        return "GOLD BUY NOW"
    if "sell" in text:
        return "GOLD SELL NOW"
    return "nada"


# Función para preparar las órdenes
def lista_ordenes(text: str) -> List[str]:
    # Eliminamos la @ del texto
    text = text.replace("@", "")

    # Cambiamos el texto tp1 y tp2
    text = text.replace("tp1", "tp").replace("tp2", "tp")

    # Definimos el precio de entrada, el tp y el sl
    numeros = re.findall(r"\d+\.\d|\d+", text)
    entrada = float(numeros[0])
    sl = float(numeros[2])
    ordenes = []

    # Definimos las órdenes
    if ("buy") in text:
        for valor in range(int(NUM_ORDENES)):
            entrada_orden = entrada - valor * DIST_ORDENES
            ordenes.append(f"Buy Limit Gold {entrada_orden} tp:{entrada + 4} sl:{sl}")
        return ordenes
    else:
        for valor in range(int(NUM_ORDENES)):
            entrada_orden = entrada + valor * DIST_ORDENES
            ordenes.append(f"Sell Limit Gold {entrada_orden} tp:{entrada - 4} sl:{sl}")
        return ordenes


# Evento para capturar mensajes del canal de origen
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def forward_message(event):
    original_text = event.message.text

    # Pasamos todo el mensaje a minúsculas
    original_text_lower = original_text.lower()

    # Eliminamos los emoticonos y las líneas en blanco
    text = eliminar_lineas_en_blanco(eliminar_emoticonos(original_text_lower)).replace(
        "*", ""
    )
    print(text)

    if not text:
        print("El mensaje no contiene texto.")
    else:
        if ("let’s scalping" in text) or ("lets scalping" in text):
            # Envía la orden primera a mercado
            order = envio_orden_mercado(text)
            # await client.send_message(DEST_CHANNEL, order) # envio de orden a mercado
        else:
            if ("buy gold @" in text) or ("sell gold @" in text):
                for order in lista_ordenes(text):
                    # Envía el mensaje modificado al canal de destino
                    print(order)
                    await client.send_message(DEST_CHANNEL, order)
                    await asyncio.sleep(TIEMPO_ESPERA)


# Iniciar cliente
async def main():
    await client.start(PHONE)
    print("Bot " + SESSION_NAME + " iniciado y escuchando mensajes...")
    await client.run_until_disconnected()


# Ejecutar
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
