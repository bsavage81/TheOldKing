from discord.ext import commands
import discord
from discord import app_commands
from discord.ext.modal_paginator import ModalPaginator, PaginatorModal
from typing import Any, Dict, List


# pre-defined questions and title for each modal
# this could be loaded from a json file or database
# each "modal" is a dict with the following keys:
# title: str - the title of the modal
# required: bool - whether the modal is required to be filled out before the paginator can be finished
# questions: List[str] - a list of questions to ask the user. Max 5 questions per modal.
personal_questions = {
    "title": "Personal Questions",
    "required": True,
    "questions": [
        "What is your name?",
        "What is your age?",
        "Any hobbies?",
        "Dad's name?",
        "Mom's name?",
    ],
}
misc_questions = {
    "title": "Miscellaneous Questions",
    "required": False,
    "questions": [
        "What is your favorite color?",
        "What is your favorite food?",
        "What is your favorite animal?",
        "What is your favorite movie?",
        "What is your favorite game?",
    ],
}
reason_questions = {
    "title": "Why Questions",
    "required": True,
    "questions": [
        "Why do you want to join?",
        "Why should we let you in?",
        "What do you like about the server?",
        "What do you like about the bot?",
        "What do you like about the community?",
    ],
}
# want even more control over the inputs?
# you can use the TextInput class directly
# from discord.ui import TextInput
# and then add the TextInput to the modal
# modal.add_item(TextInput(...)) instead of looping.
# see the discord.py docs for more info on the TextInput class.

# more dict like? use a dict for the questions too
# questions = [
#   {
#     "label": "What is your name?",
#     "min_length": 2,
#     "max_length": 200,
#     "required": False,
#     ...
#   },
#   ...
# ]
# etc...


# subclass the paginator to define our own on_finish method
# and to add the modals to the paginator via a custom __init__
class VerifyModal(ModalPaginator):
    def __init__(self, questions_inputs: List[Dict[str, Any]], *, author_id: int, **kwargs: Any) -> None:
        # initialize the paginator with the the author_id kwarg
        # and any other kwargs we passed to the constructor.
        # possible kwargs are as follows:
        # timeout: Optional[int] = None - the timeout for the paginator (view)
        # disable_after: bool = True - whether to disable all buttons after the paginator is finished or cancelled.
        # can_go_back: bool = True - whether the user can go back to previous modals using the "Previous" button.
        # sort_modals: bool = True - whether to sort the modals by the required kwarg.
        # See more on the class.
        super().__init__(author_id=author_id, **kwargs)
        # iterate over the questions_inputs list
        for data in questions_inputs:
            # unpack the data from the dict
            title: str = data["title"]
            required: bool = data["required"]
            questions: List[str] = data["questions"]
            # create a new modal with the title and required kwarg
            modal = PaginatorModal(title=title, required=required)
            # add the questions to the modal
            for question in questions:
                modal.add_input(
                    label=question,  # the label of the text input
                    min_length=2,  # the minimum length of the text input
                    max_length=200,  # the maximum length of the text input
                    # see the discord.py docs for more info on the other kwargs
                )

            # add the modal to the paginator
            self.add_modal(modal)    

    # override the on_finish method to send the answers to the channel when the paginator is finished.
    async def on_finish(self, interaction: discord.Interaction[Any]) -> None:
        # you probably don't need to defer the response here.
        await interaction.response.defer()
        # call the original on_finish method
        # which will also disable the buttons
        await super().on_finish(interaction)

        # create a list of answers
        # default format: **Modal Title**\nQuestion: Answer\nQuestion: Answer\n... etc
        answers: list[str] = []
        for modal in self.modals:
            prefix = f"**{modal.title}**\n"
            field: discord.ui.TextInput[Any]
            for field in modal.children:  # type: ignore
                prefix += f"{field.label}: {field.value}\n"

            answers.append(prefix)

        print(answers)
        await interaction.followup.send(f"Answers from {interaction.user.mention}:\n\n" + "\n\n".join(answers))

class VerifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='verify', description='apply to the server')
    async def verify(self, interaction: discord.Interaction[Any]):
        # initialize the paginator with all the questions data we defined above in a list
        # and the author_id so that only the command invoker can use the paginator.
        questions_inputs = [personal_questions, misc_questions, reason_questions]
        paginator = VerifyModal(questions_inputs, author_id=interaction.user.id)

        # send the paginator to the current channel
        await interaction.response.send_message("Be sure to complete all pages of questions before clicking Finish")
        await paginator.send(interaction.channel)


async def setup(bot):
    await bot.add_cog(VerifyCog(bot))