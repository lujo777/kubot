import asyncio
import json

import aiohttp
from kutana import Plugin


HEADERS = {
    "Host": "searchface.ru",
    "Origin": "http://searchface.ru",
    "Referer": "http://searchface.ru/",
    "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36")
}


plugin = Plugin(
    name="Searchface",
    cmds=("searchface // search similar faces to sent photo",)
)


# Technical functions
@plugin.on_startup()
async def on_startup(kutana, rplugins):
    plugin.session = aiohttp.ClientSession()


@plugin.on_dispose()
async def on_dispose():
    await plugin.session.close()


# Process functions
@plugin.on_text("searchface")
async def on_text(message, env):
    photo = None

    if message.attachments:
        photo = await env.get_file_from_attachment(message.attachments[0])

    if not photo:
        await env.reply("Send photo to search faces similar to")
        return

    fd = aiohttp.FormData()
    fd.add_field("upl", photo)

    async with plugin.session.post("http://searchface.ru/request/",
                                   headers=HEADERS, data=fd) as resp:

        response = await resp.text()

    try:
        result = json.loads(response)

    except Exception:
        if response == "Image contains 0 faces":
            await env.reply("We couldn't detect any faces")
            return

        if response and response.startswith("Image contains"):
            await env.reply("We detected multiple faces")
            return

        await env.reply("Something went wrong")
        return

    download_upload_tasks = []

    def _get_urls(result):
        for block in result:
            for image in block[1]:
                yield image[0]

    async def _download_upload(url):
        async with plugin.session.get(url) as resp:
            image_file = await resp.read()

        return await env.upload_photo(image_file)

    for url in _get_urls(result):
        download_upload_tasks.append(_download_upload(url))

        if len(download_upload_tasks) >= 10:
            break

    await env.reply(
        "", attachment=await asyncio.gather(*download_upload_tasks)
    )
