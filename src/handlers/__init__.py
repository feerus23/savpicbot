from handlers import message, command, inline


def register(dp):
    inline.reg(dp)
    command.reg(dp)
    message.reg(dp)
