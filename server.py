import asyncio
import websockets

CLIENTS = set()

async def handler(ws, *args):
    
    CLIENTS.add(ws)
    try:
        await broadcast("Alguien se conectó")
        async for msg in ws:
            await broadcast(msg)  
    except websockets.ConnectionClosed:
        pass
    finally:
        CLIENTS.discard(ws)
        await broadcast("Alguien se desconectó")

async def broadcast(message: str):
    if not CLIENTS:
        return
    dead = set()
    for c in CLIENTS:
        try:
            await c.send(message)
        except Exception:
            dead.add(c)
    for c in dead:
        CLIENTS.discard(c)

async def main():
    print("Servidor WebSocket en ws://localhost:8766")
    async with websockets.serve(handler, "localhost", 8766):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())