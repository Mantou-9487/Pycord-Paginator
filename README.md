# Paginator for Embeds

A Paginator class for managing embeds with pagination. It allows users to navigate through a list of embeds using buttons.

## Parameters

- `timeout` (int): How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)
- `previous_button` (disnake.ui.Button, optional): Overrides default previous button.
- `next_button` (disnake.ui.Button, optional): Overrides default next button.
- `trash_button` (disnake.ui.Button, optional): Overrides default trash button.
- `page_counter_separator` (str, optional): The custom separator between the pages numbers in the page_counter button.
- `page_counter_style` (disnake.ButtonStyle, optional): Overrides default page counter style.
- `initial_page` (int, optional): Page to start the pagination on.
- `on_timeout_message` (Optional[str], optional): Overrides default `on_timeout` string set as embed footer. If `None`, no message will appear `on_timeout`.
- `interaction_check` (bool, optional): Check whether the users interacting with the paginator are the owner of the command or not. Default set to `True`.
- `interaction_check_message` (Union[disnake.Embed, str], optional): The message to send when an `interaction_check` fails, e.g., a user who is not the command owner attempted to interact with the paginator. This feature can be disabled by setting `interaction_check` to `False`.
- `ephemeral` (bool, optional): Whether the paginator should only be visible to the command invocator or to anyone else.
- `persistent` (bool, optional): Whether the paginator should persist across multiple sessions.

## How to Install
```
python setup.py build
python setup.py install
```

## Usage

To use the `Paginator` class, follow these steps:

1. Create a list of embeds that you want to paginate.
2. Instantiate the `Paginator` class, passing the list of embeds as the `embeds` parameter.
3. Use await Paginator().start method.

## Basic Example

```python
from discord import ApplicationContext, SlashCommandGroup, Embed
from discord.ext import commands

from core.paginator import Paginator

class Page(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    page = SlashCommandGroup("page", "pages")

    @page.command(name="test")
    async def test(self, ctx:ApplicationContext):
        
        embeds = [
            Embed(
                title="First embed"
            ),
            Embed(
                title="Second embed"
            ),
            Embed(
                title="Third embed"
            ),
        ]
        await Paginator().start(ctx, pages=embeds)

def setup(bot):
    bot.add_cog(Page(bot))
    
```
