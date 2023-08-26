# Paginator for Embeds

A Paginator class for managing embeds with pagination. It allows users to navigate through a list of embeds using buttons.

## Parameters

- `embeds` (List[Embed]): List of embeds which are in the Paginator. The Paginator starts from the first embed.
- `author` (int, optional): The ID of the author who can interact with the buttons. If not specified, anyone can interact with the Paginator buttons.
- `timeout` (float, optional): How long the Paginator should timeout, in seconds, after the last interaction.

## How to Install
```
python setup.py build
python setup.py install
```

## Usage

To use the `Paginator` class, follow these steps:

1. Create a list of embeds that you want to paginate.
2. Instantiate the `Paginator` class, passing the list of embeds as the `embeds` parameter.
3. Optionally, specify the `author` parameter to restrict interaction with the buttons to a specific user.
4. Optionally, specify the `timeout` parameter to set a timeout value for the Paginator.
5. Add the Paginator to view using the `view=Paginator(pages, ctx.author.id, None)` method.

## Example

```python
from paginator import Paginator
from discord.ext import commands
from discord import Embed

@commands.slash_command(name="paginator", description="test")
async def pg(self, ctx):
    embed1 = Embed(title="1")
    embed2 = Embed(title="1")
    embed3 = Embed(title="1")
    # Create a list of embeds
    pages = [embed1, embed2, embed3]
    # Add the Paginator to a send_message
    await ctx.interaction.send_message(embed=pages[0], view=Paginator(pages, ctx.author.id, None))
    
```