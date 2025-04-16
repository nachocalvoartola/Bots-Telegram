from telethon import TelegramClient, events

# Credenciales de la API
API_ID = "242684"  # Reemplazar con tu API ID
API_HASH = "7a6b808006eaaf408646bd914c0b2eec"  # Reemplazar con tu API Hash

# Teléfono del usuario que accederá al canal
PHONE = "+34658936280"  # Reemplazar con tu número (incluido el código del país)

# ID o nombre de usuario del canal de origen y canal de destino

SOURCE_CHANNEL = -1002059932006  # Canal Gold  WSM premium
# SOURCE_CHANNEL = -1002460410884  # Canal recibir señales de prueba
DEST_CHANNEL = -1002337168486  # Canal Gold reenvio Javi Amat

SESSION_NAME = "bot_reenvio_gold_WSM"

# Crear cliente de Telethon
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


# Evento para capturar mensajes nuevos del canal de origen
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def forward_new_message(event):
    # Verifica si el mensaje tiene texto o medios
    if event.message.text or event.message.media:
        # Envía el mensaje al canal de destino
        await client.send_message(
            DEST_CHANNEL,
            message=event.message.text,
            file=event.message.media,  # Adjunta el medio si está presente
        )
        print(f"Mensaje nuevo reenviado: {event.message.text}")


# Evento para capturar mensajes editados del canal de origen
@client.on(events.MessageEdited(chats=SOURCE_CHANNEL))
async def forward_edited_message(event):
    # Verifica si el mensaje tiene texto o medios
    if event.message.text or event.message.media:
        # Envía el mensaje editado al canal de destino
        await client.send_message(
            DEST_CHANNEL,
            message=f"(Editado): {event.message.text}",
            file=event.message.media,  # Adjunta el medio si está presente
        )
        print(f"Mensaje editado reenviado: {event.message.text}")


# Iniciar cliente
async def main():
    await client.start(PHONE)
    print("Bot " + SESSION_NAME + " iniciado y escuchando mensajes...")
    await client.run_until_disconnected()


# Ejecutar
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
