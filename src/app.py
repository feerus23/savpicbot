from handlers import register
from data import dispatcher, base, register_commands

import asyncio

register(dispatcher)


async def main():
    base.init()
    await register_commands(dispatcher)
    await dispatcher.start_polling()

asyncio.run(main())
