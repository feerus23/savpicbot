from handlers import message, command


def register(dp):
    command.reg(dp)
    message.reg(dp)
