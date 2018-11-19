from kutana import Plugin


plugin = Plugin(
    name="Echo",
    cmds=("echo text - reply with specified text",)
)


@plugin.on_startswith_text("echo ", "эхо ")
async def on_echo(message, attachments, env):
    if env.body:
        return await env.reply("{}".format(env.body))

    return await env.reply("You didn't specified text.")
