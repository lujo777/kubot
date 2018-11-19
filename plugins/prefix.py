from kutana import Plugin, Message
import re


plugin = Plugin(name="Prefix")


@plugin.on_startup()
async def on_startup(update, env):
    plugin.names = tuple(update["kutana"].storage["names"])
    plugin.separators = (" ", ",", ".", "!", "?")

    plugin.pattern = re.compile(
        "^ *" +
        "(" + "|".join(re.escape(n) for n in plugin.names) +  ")" +
        "(" + "|".join(re.escape(s) for s in plugin.separators) + ")" +
        "( |\n)?(?P<text>.*)",
        re.IGNORECASE
    )


@plugin.on_has_text()
async def on_has_text(message, attachments, env):
    match = plugin.pattern.match(message.text)

    if message.from_id != message.peer_id:
        mention_match = re.search(
            r"\[[a-zA-Z0-9]+\|.+?\]",
            message.raw_update["object"]["text"]
        )

    else:
        mention_match = None

    if not (mention_match or match and match.group("text")):
        return "DONE"

    env.eenv._cached_message = Message(
        match and match.group("text") or message.text,
        message.attachments,
        message.from_id,
        message.peer_id,
        message.raw_update
    )

    return "GOON"
