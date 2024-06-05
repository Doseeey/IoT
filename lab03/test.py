from aiohttp import web
import json
import asyncio

messages = []
barrier_count = 18
barrier_event = asyncio.Event()

async def handle_post(request):
    data = await request.json()
    messages.append(data)
    print(f"Received message from client {data['ID']}: {data['message']}")
    if len(messages) >= barrier_count:
        print("Setting barrier as done")
        barrier_event.set()
    return web.Response(text="OK")

async def barrier_task():
    print("Task blocked by barrier")
    await barrier_event.wait()
    print("Barrier released - printing message:")
    print(" ".join([x['message'] for x in sorted(messages, key=lambda x: x['ID'])]))

async def main():
    app = web.Application()
    app.router.add_post('/', handle_post)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    barrier_task_handle = asyncio.create_task(barrier_task())

    await asyncio.gather(barrier_task_handle)

asyncio.run(main())
