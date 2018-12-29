import json

from kutana import (Kutana, TGManager, VKManager, load_configuration,
                    load_plugins)


# Create engine
kutana = Kutana()


# Load configuration and available plugins
with open("config.json", "r") as fh:
    config = json.load(fh)

kutana.storage["names"] = config["info"]["names"]

plugins_storage = {plugin.name: plugin for plugin in load_plugins("plugins/")}


# Register plugins specified in configuration
plugins = []

for plugin_name in config["plugins"]:
    plugins.append(plugins_storage[plugin_name])

kutana.executor.register_plugins(plugins)


# Add managers from configuration
for manager_conf in config["managers"]:
    manager = None

    if manager_conf["type"] == "vkontakte":
        manager = VKManager

    elif manager_conf["type"] == "telegram":
        manager = TGManager

    if manager is None:
        raise ValueError(
            "Unknown manager type: {}".format(manager_conf["type"])
        )

    kwargs = manager_conf
    kwargs.pop("type")

    kutana.add_manager(manager(**kwargs))

# Start engine if this file was run
if __name__ == "__main__":
    kutana.run()
