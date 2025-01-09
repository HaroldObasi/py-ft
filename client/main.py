from client import Client
import asyncio

async def main():
    client = Client()
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())