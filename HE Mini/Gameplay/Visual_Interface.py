import discord
from discord.ext import commands


class PageView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=300)
        self.author_id = author_id
        self.current_page = "home"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "These page controls belong to another user.",
                ephemeral=True,
            )
            return False
        return True

    async def show_page(self, interaction: discord.Interaction, page: str):
        self.current_page = page
        embed = self.get_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    async def delete_after_spawn(self):
        """Remove the instance information message once the player spawns."""
        if self.message is not None:
            await self.message.delete()

    def get_embed(self) -> discord.Embed:
        pages = {
            "home": (
                "===Home===\n"
                "Welcome to HE (Mini)! This is Text Based as you can probably tell.\n",
                "Gameplay is a little different here, For Ease of Play We removed the Y axis.\n"
                "You can move left and right, and up and down, but not diagonally. This is to make it easier to play on mobile devices.\n"
                "Below this message you probably see some buttons, these are pages you can navigate to on this message.\n"
                "The Home page is the page you are currently on, and it will always be the first page you see when you open this message.\n"
                "The Profile page will show you your player profile and instance information.\n"
                "The Balance page will show you your current balance and transaction details. Along with a section allowing you to make payments with players in the same server.\n"
                "The Access Codes page will show you the access codes assigned to your account, and allow you to redeem new access codes.\n"
                "Hitting the buttons will navigate you to the corresponding page, and you can always return to the Home page by hitting the Home button.\n"
                "To Reduce strain on the server, this 'Instance' Automatically Deletes after 1 hour of inactivity, so be sure to save your progress before leaving the game or leaving your computer for a while\n"
                "another thing, You probably see a Green button called Spawn? this button spawns you as a player in the game, this button only appears once as all your progress gets saved.\n"
                "If you have any questions or need help, please reach out to the server admins or moderators for assistance. They do monitor the logs quite frequently.\n"
                "When you are ready to start playing, hit the Spawn button and have fun!\n"
                "If you want to leave the game, you can do so by hitting the Delete button, this will delete your instance and all progress will be lost, so be sure to save your progress before leaving the game.\n"
                "If you want to save your progress, you can do so by hitting the Save button, this will save your progress and allow you to load it later.\n"
                "If you want to load your progress, you can do so by hitting the Load button, this will load your progress and allow you to continue playing from where you left off.\n"
                "The profile, Balance, and Access codes, pages do not contain any information at first, but gradually as you play the game, they will fill up with information about your progress and achievements.\n"
            ),
            "profile": (
                "Profile",
                "View your player profile and instance information here.",
            ),
            "balance": (
                "Balance",
                "View your current balance and transaction details here.",
            ),
            "access": (
                "Access Codes",
                "View the access codes assigned to your account here.",
            ),
        }
        title, description = pages[self.current_page]
        return discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blurple(),
        )

    @discord.ui.button(label="Home", style=discord.ButtonStyle.primary)
    async def home_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.show_page(interaction, "home")

    @discord.ui.button(label="Profile", style=discord.ButtonStyle.secondary)
    async def profile_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.show_page(interaction, "profile")

    @discord.ui.button(label="Balance", style=discord.ButtonStyle.secondary)
    async def balance_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.show_page(interaction, "balance")

    @discord.ui.button(label="Access Codes", style=discord.ButtonStyle.secondary)
    async def access_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.show_page(interaction, "access")

    @discord.ui.button(label="Spawn", style=discord.ButtonStyle.success, row=1)
    async def spawn_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        
        await interaction.response.defer()
        await self.delete_after_spawn()


class Visual_Interface(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_instance_page(
        self, destination: discord.abc.Messageable, author_id: int
    ) -> PageView:
        """Send the instance page when an instance is created.

        Call ``view.delete_after_spawn()`` after spawning if spawning is
        handled outside the Spawn button callback.
        """
        view = PageView(author_id)
        view.message = await destination.send(embed=view.get_embed(), view=view)
        return view



async def setup(bot: commands.Bot):
    await bot.add_cog(Visual_Interface(bot))
