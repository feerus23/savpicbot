from handlers import message, command


def register(dp):
    commands.reg(dp)
    message.reg(dp)
