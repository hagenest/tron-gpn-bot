import asyncio

# Dictionary to store wall positions for each player
walls = {}

# Store the map size
map_width = 0
map_height = 0

async def parse_packet(packet):
    global walls, map_width, map_height
    parts = packet.split('|')
    packet_type = parts[0]
    
    if packet_type == 'motd':
        print(f"Message of the day: {parts[1]}")
    elif packet_type == 'error':
        print(f"Error: {parts[1]}")
    elif packet_type == 'pos':
        player_id = int(parts[1])
        x = int(parts[2])
        y = int(parts[3])
        if player_id not in walls:
            walls[player_id] = []
        walls[player_id].append((x, y))
    elif packet_type == 'die':
        dead_player_ids = [int(pid) for pid in parts[1:]]
        for dead_player_id in dead_player_ids:
            if dead_player_id in walls:
                del walls[dead_player_id]
    elif packet_type == 'game':
        map_width = int(parts[1])
        map_height = int(parts[2])
    # Add other packet type handling here

async def send_move(writer, direction):
    writer.write(f"move|{direction}\n".encode())
    await writer.drain()

async def tron_bot():
    reader, writer = await asyncio.open_connection('94.45.236.142', 4000)

    # Send join packet
    writer.write(b"join|hagitron-0.4|mypassword\n")
    await writer.drain()

    while True:
        data = await reader.readline()
        packet = data.decode().strip()
        await parse_packet(packet)
        # Add logic for determining the bot's next move
        await send_move(writer, "up")  # Example move

asyncio.run(tron_bot())
