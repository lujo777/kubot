from kutana import Kutana, VKController, load_plugins, load_configuration
import json

kutana = Kutana()

with open("config.json", "r") as fh:
    config = json.load(fh)

kutana.storage["names"] = config["info"]["names"]

for ctype in config["tokens"]:
    controller = None

    if ctype == "vkontakte":
        controller = VKController

    if controller is None:
        raise ValueError("Unknown controller type: {}".format(ctype))

    for token in config["tokens"][ctype]:
        if not token:
            continue

        kutana.add_controller(controller(token))

plugins_base = {plugin.name: plugin for plugin in load_plugins("plugins/")}

plugins = []

for plugin_name in config["plugins"]:
    plugins.append(plugins_base[plugin_name])

kutana.executor.register_plugins(*plugins)

kutana.run()
