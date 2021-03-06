import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init(debug=True)
nonebot.load_builtin_plugins("echo")
nonebot.load_plugin("nonebot_plugin_guild_patch")
nonebot.get_driver().register_adapter(Adapter)

if __name__ == "__main__":
    nonebot.run()
