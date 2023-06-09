import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Dictionary to store wall positions for each player
walls = {}
game: bool = False

# Store the map size
map_width = 0
map_height = 0


async def parse_packet(packet, writer):
    global walls, map_width, map_height
    parts = packet.split("|")
    packet_type = parts[0]

    if packet_type == "motd":
        logging.info(f"Message of the day: {parts[1]}")
    elif packet_type == "error":
        logging.error(f"Error: {parts[1]}")
    elif packet_type == "pos":
        player_id = int(parts[1])
        x = int(parts[2])
        y = int(parts[3])
        logging.info(f"Player {player_id} is at ({x}, {y})")
        if player_id not in walls:
            walls[player_id] = []
        walls[player_id].append((x, y))
    elif packet_type == "die":
        dead_player_ids = [int(pid) for pid in parts[1:]]
        for dead_player_id in dead_player_ids:
            if dead_player_id in walls:
                logging.info(f"Player {dead_player_id} died")
                logging.info(f"Deleted the following walls: {walls[dead_player_id]}")
                del walls[
                    dead_player_id
                ]  # Move this line after logging the deleted walls
                logging.info(f"Remaining players: {list(walls.keys())}")
    elif packet_type == "game":
        game = True
        map_width = int(parts[1])
        map_height = int(parts[2])
        walls = {}
        logging.info(f"Map size: {map_width}x{map_height}")
    elif packet_type == "lose":
        logging.info(f"Lost the game")
        game = False
    elif packet_type == "win":
        logging.info(f"Won the game")
        game = False
    elif packet_type == "tick":
        if game:
            await send_move(writer, "down")


async def send_move(writer, direction):
    writer.write(f"move|{direction}\n".encode())
    logging.info(f"Sent move: {direction}")
    await writer.drain()


async def tron_bot():
    reader, writer = await asyncio.open_connection("94.45.236.142", 4000)

    # Send join packet
    writer.write(b"join|hagitron-0.5|fewihfoiewhfweobubdofnewoif43\n")
    logging.info(f"Sent join packet")
    await writer.drain()

    while True:
        data = await reader.readline()
        packet = data.decode().strip()
        await parse_packet(packet, writer)


asyncio.run(tron_bot())
