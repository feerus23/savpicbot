from handlers import register
from data import dispatcher, base

import asyncio

register(dispatcher)


async def main():
    base.init()
    await dispatcher.start_polling()

asyncio.run(main())
