import asyncio

async def task():
    print("Hello World")
    await asyncio.sleep(10)
    print("Finish Hello World")

async def main():
    while True:
        asyncio.create_task(task())
        await asyncio.sleep(1)  

if __name__ == "__main__":
    asyncio.run(main())