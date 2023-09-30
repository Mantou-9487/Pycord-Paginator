import logging
import inspect
import os

from discord.ui import View, button, Button
from discord import ButtonStyle, Interaction, Embed, Color, PartialEmoji, ApplicationContext
from colorlog import ColoredFormatter

class Paginator(View):
    """
    Embed Paginator.

    Parameters:
    ----------
    timeout: int
        How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)
    previous_button: disnake.ui.Button
        Overrides default previous button.
    next_button: disnake.ui.Button
        Overrides default next button.
    trash_button: disnake.ui.Button.
        Overrides default trash Button.
    page_counter_separator: str
        The custom separator between the pages numbers
        in the page_counter button.
    page_counter_style: disnake.ButtonStyle
        Overrides default page counter style.
    initial_page: int
        Page to start the pagination on.
    on_timeout_message: Optional[str]
        Overrides default `on_timeout` str set as embed footer.
        If `None` no message will appear `on_timeout`.
    interaction_check: bool
        Check whether the users interacting with the paginator are the owner
        of the command or not. Default set to `True`.
    interaction_check_message: Union[disnake.Embed, str]
        The message to send when an `interaction_check` fails e.g a user
        who is not the command owner attempted to interact with the paginator.
        This feature can be disabled by setting `interaction_check` to `False`.
    ephemeral: bool
        Whether the paginator should only be visible to the command invocator or
        to anyone else.
    persistent: bool
    
    """

    __running_interaction_ids: list[int] = []

    def __init__(self,
        *,
        timeont: int | float | None = 180,
        previous_button: Button | None = None,
        next_button: Button | None = None,
        trash_button: Button | None = None,
        page_counter_separator: str = "/",
        page_counter_style: ButtonStyle = ButtonStyle.grey,
        initial_page: int = 0,
        on_timeout_message: str | None = None,
        interaction_check: bool = True,
        interaction_check_message: Embed | str = Embed(
            description="You cannot control this pagination because you did not execute it.",
            color=Color.red(),
        ),
        ephemeral: bool = False,
        persistent: bool = False
    ) -> None:
        
        self.timeout = timeont
        self.previous_button = previous_button
        self.next_button = next_button
        self.trash_button = trash_button

        self.page_counter_separator = page_counter_separator
        self.page_counter_style = page_counter_style
        self.initial_page = initial_page

        self.ephemeral = ephemeral
        self.original_message_deleted: bool = False
        self.on_timeout_message = on_timeout_message
        self._interaction_check = interaction_check
        self.interaction_check_message = interaction_check_message
        self.persistent = persistent

    __running_interaction_ids: list[int] = []

    def __init__(self,
        *,
        timeont: int | float | None = 180,
        previous_button: Button | None = None,
        next_button: Button | None = None,
        trash_button: Button | None = None,
        page_counter_separator: str = "/",
        page_counter_style: ButtonStyle = ButtonStyle.grey,
        initial_page: int = 0,
        on_timeout_message: str | None = None,
        interaction_check: bool = True,
        interaction_check_message: Embed | str = Embed(
            description="You cannot control this pagination because you did not execute it.",
            color=Color.red(),
        ),
        ephemeral: bool = False,
        persistent: bool = False
    ) -> None:
        
        self.timeout = timeont
        self.previous_button = previous_button
        self.next_button = next_button
        self.trash_button = trash_button

        self.page_counter_separator = page_counter_separator
        self.page_counter_style = page_counter_style
        self.initial_page = initial_page

        self.ephemeral = ephemeral
        self.original_message_deleted: bool = False
        self.on_timeout_message = on_timeout_message
        self._interaction_check = interaction_check
        self.interaction_check_message = interaction_check_message
        self.persistent = persistent

        self.setup_logging()

        if self.persistent and self.timeout:
            raise ValueError(f"To create a persistent Paginator the timeout must be None, not {self.timeout.__class__!r}")

        super().__init__(timeout=self.timeout)
    
    async def start(
        self,
        ctx: ApplicationContext,
        pages: list[Embed]
    ) -> None:
        
        if self.previous_button is None:
            self.previous_button = Button(
                emoji=PartialEmoji(name="\U000025c0"),
                custom_id=f"PREV_BTN:{ctx.interaction.id}:{ctx.author.id}",
            )
        if self.next_button is None:
            self.next_button = Button(
                emoji=PartialEmoji(name="\U000025b6"),
                custom_id=f"NEXT_BTN:{ctx.interaction.id}:{ctx.author.id}",
            )
        if self.trash_button is None:
            self.trash_button = Button(
                emoji=PartialEmoji(name="\U0001f5d1"),
                style=ButtonStyle.danger,
                custom_id=f"TRASH_BTN:{ctx.interaction.id}:{ctx.author.id}",
            )
        
        Paginator.__running_interaction_ids.append(ctx.command.id)
        self.pages = pages
        self.total_page_count = len(pages)
        self.interaction = ctx.interaction
        self.current_page = self.initial_page
        self.original_message_deleted = False
        self.next_button.disabled = self.previous_button.disabled = self.trash_button.disabled = False

        self.previous_button.callback = self.__previous_button_callback
        self.next_button.callback = self.__next_button_callback
        self.trash_button.callback = self.__trash_button_callback

        self.page_counter: Button = Button(
            label=f"{self.initial_page + 1} {self.page_counter_separator} {self.total_page_count}",
            style=self.page_counter_style,
            disabled=True,
        )

        if self.persistent and not all((self.previous_button.custom_id, self.next_button.custom_id, self.trash_button.custom_id)):
            raise ValueError("You need to set the custom ID of buttons to make the Paginator persistent.")

        self.add_item(self.previous_button)
        self.add_item(self.page_counter)
        self.add_item(self.next_button)
        self.add_item(self.trash_button)

        await ctx.interaction.response.send_message(
            embed=self.pages[self.initial_page], view=self, ephemeral=self.ephemeral
        )

        if self.persistent:
            ctx.bot.add_view(self)

    async def on_timeout(self) -> None:
        if not self.original_message_deleted:
            self.previous_button.disabled = self.next_button.disabled = self.trash_button.disabled = True # type: ignore
            embed = self.pages[self.current_page]
            if self.on_timeout_message:
                embed.set_footer(text=self.on_timeout_message)
            await self.interaction.response.edit_message(embed=embed, view=self)
        
        Paginator.__running_interaction_ids.remove(self.interaction.id)
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        if isinstance(self._interaction_check, bool) and self._interaction_check:
            if interaction.user.id != self.interaction.user.id:
                if isinstance(self.interaction_check_message, Embed):
                    await interaction.response.send_message(
                        embed=self.interaction_check_message, ephemeral=True
                    )
                elif isinstance(self.interaction_check_message, str):
                    await interaction.response.send_message(
                        self.interaction_check_message, ephemeral=True
                    )
                return False
            return True
        else:
            return False
    
    async def __previous(self, interaction: Interaction) -> None:
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1} {self.page_counter_separator} {self.total_page_count}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )

    async def __next(self, interaction: Interaction) -> None:
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1} {self.page_counter_separator} {self.total_page_count}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )
    async def __next_button_callback(
        self, interaction: Interaction
    ) -> None:
        await self.__next(interaction)

    async def __previous_button_callback(
        self, interaction: Interaction
    ) -> None:
        await self.__previous(interaction)

    async def __trash_button_callback(
        self, interaction: Interaction
    ) -> None:
        self.original_message_deleted = True
        await interaction.response.defer()
        await interaction.delete_original_response()

    def setup_logging(self):
        """
        Set up the loggings for the bot
        :return: None
        """
        formatter = ColoredFormatter(
            '%(asctime)s %(log_color)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(filename="lava.log", encoding="utf-8", mode="w")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logging.basicConfig(
            handlers=[stream_handler, file_handler], level=logging.INFO
        )