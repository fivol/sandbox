import asyncio

import websockets


async def main():
    async with websockets.connect('ws://localhost:3001/test') as s:
        await s.send("Hello world!")
        print(await s.recv())


if __name__ == '__main__':
    asyncio.run(main())