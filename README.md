# nonebot-plugin-guild-patch

*Patch plugin for NoneBot2 QQ guild (go-cqhttp) support.*

*NoneBot2 QQ 频道 (go-cqhttp) 支持适配补丁插件.*

> **注: 本补丁没有经过充分测试, 不建议在生产环境使用, 如果发现任何问题请评论反馈**

## 适用版本

- [`go-cqhttp` >= `1.0.0-beta8`](https://github.com/Mrs4s/go-cqhttp/releases/tag/v1.0.0-beta8)
  - 已支持[`1.0.0-beta8-fix1`](https://github.com/Mrs4s/go-cqhttp/releases/tag/v1.0.0-beta8-fix1)新加入的事件
- `NoneBot2` >= `2.0.0b1`

## 支持功能

- [x] 正常接收并处理频道消息事件
  - [x] 支持字符串形式消息上报
  - [x] 支持数组形式消息上报
- [x] 支持`bot.send`和`matcher.send`直接向频道发送消息
- [ ] 支持`event.to_me`以支持`to_me`规则
- [ ] 可选的事件转换器, 将频道消息事件转换为群消息

## 安装

使用`nb-cli`或者其他什么你喜欢的方式安装并加载该插件即可

如果它被成功加载, 你在调试模式下应该看到这样的日志:

```diff
11-13 09:14:52 [DEBUG] nonebot | Succeeded to load adapter "cqhttp"
11-13 09:14:52 [SUCCESS] nonebot | Succeeded to import "nonebot.plugins.echo"
+ 11-13 09:14:52 [SUCCESS] nonebot | Succeeded to import "nonebot_guild_patch"
11-13 09:14:52 [SUCCESS] nonebot | Running NoneBot...
11-13 09:14:52 [DEBUG] nonebot | Loaded adapters: cqhttp
11-13 09:14:52 [INFO] uvicorn | Started server process [114514]
11-13 09:14:52 [INFO] uvicorn | Waiting for application startup.
11-13 09:14:52 [INFO] uvicorn | Application startup complete.
```

## 使用

这里有一个示例插件, 它只会接收来自频道的消息

```python
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageSegment

from nonebot_plugin_guild_patch.models import GuildMessageEvent

matcher = on_command('image')


@matcher.handle()
async def _(bot: Bot, event: GuildMessageEvent):
    await matcher.send(
        MessageSegment.image(
            file='https://1mg.obfs.dev/',
            cache=False,
        ))
```

## 开源许可

本项目使用[MIT](./LICENSE)许可证开源

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
