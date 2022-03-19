from handlers import register
from data import dispatcher

register(dispatcher)
await dispatcher.start_polling()
