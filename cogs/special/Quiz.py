import discord
from datetime import datetime as dt
import pytz
import requests
import json
from discord.ext import commands
import random
import html
from string import ascii_uppercase
from collections import Counter

Signature = "\n\nSincerely, Robot"

print('Special Cog Quiz Loaded', flush=True)

class Quiz(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    #Takes in Quiz Setup and retrieves response
    @commands.command()
    async def setup(self, ctx, *arg):
        """
        The command invoked by users to setup and start the quiz.

        Arguments:
        ctx (Context): Represents the context in which a command is being invoked under.
        *arg (tuple): Optional Arguments to specify quiz options.
        """
        quiz_options = await self.create_quiz_options(arg)
        quiz_url = await self.create_quiz_url(quiz_options)
        self.quiz_details = await self.return_quiz_details(quiz_url)
        await self.ask_question(ctx)

    @commands.command()
    async def question(self, ctx):

        error_message = await self.ask_question(ctx)
        await ctx.send(error_message + Signature)

    async def ask_question(self, ctx):
        if self.quiz_details:
            self.current_quiz_detail = self.quiz_details.pop()
            question = self.current_quiz_detail['question']
            answer_desc = await self.create_answer_desc(self.current_quiz_detail)
            embed = discord.Embed(title=question, description=answer_desc)
            self.question_msg = await ctx.send(embed=embed)
            for reaction in {'🇦':'A', '🇧':'B', '🇨':'C', '🇩':'D'}.keys():
                await self.question_msg.add_reaction(reaction)
        else:
            error_message = 'Sorry, but there are no more questions!\nPlease use the setup command to retrieve more questions.'
            return error_message

    @commands.command()
    async def lock_in(self, ctx):
        event_message = await ctx.fetch_message(self.question_msg.id)
        user_answers = await self.create_user_answers(event_message.reactions)
        correct_letter = await self.return_correct_letter(self.current_quiz_detail)
        cheating_users = await self.check_cheating_users(user_answers)
        correct_users = await self.check_correct_users(user_answers, cheating_users, correct_letter)
        message = ''
        if cheating_users:
            message = await self.format_answer_message(cheating_users) + 'caught cheating! They have been disqualified!\n\n'
        if correct_users:
            message = message + await self.format_answer_message(correct_users) + "correct with their answer of {} : '{}'.".format(correct_letter, self.current_quiz_detail['answer_map'][correct_letter])
        else:
            message = message + "Nobody was correct! The answer was {} : '{}'".format(correct_letter, self.current_quiz_detail['answer_map'][correct_letter])
        await ctx.send(message + Signature)
        await self.ask_question(ctx)

    async def format_answer_message(self, users):
        """
        Lists users for use in a message sent by Robot.

        Arguments:
        users (list): List of user strings

        Returns:
        message (string): gramatically correct list of users
        """
        message = ''
        user_count = len(users)
        if user_count == 1:
            grammer = ' was '
            message = users[0] + grammer
        elif user_count > 1:
            grammer = ' were '
            for i in range(user_count-1):
                message = message + users[i] + ', '
            message = message[:-2] + 'and ' + users[-1] + grammer
        return message

    async def check_cheating_users(self, user_answers):
        """
        Returns users that cheated by selecting multiple answers.

        Arguments:
        user_answers (dict of str : list): Mapping of answer to users

        Returns:
        cheating_users (list): Users that cheated
        """
        flat_users = []
        cheating_users = []
        for users in user_answers.values():
            for user in users:
                flat_users.append(user)
        for user, answer_count in Counter(flat_users).items():
            if answer_count > 1:
                cheating_users.append(user)
        return cheating_users

    async def check_correct_users(self, user_answers, cheating_users, correct_letter):
        """
        Returns users that were correct without cheating.

        Arguments:
        user_answers (dict of str : list): Mapping of answer to users
        cheating_users (list): Users that cheated
        correct_letter (str): The correct answer represented by a letter

        Returns:
        correct_users (list): Users that were correct
        """
        correct_users = []
        for letter, users in user_answers.items():
            if letter == correct_letter:
                correct_users = users
        for user in correct_users:
            if user in cheating_users:
                correct_users.remove(user)
        return correct_users

    async def return_correct_letter(self, current_quiz_detail):
        """
        Returns the correct answer for the current quiz question.

        Arguments:
        current_quiz_detail (dict): Mapping of quiz parameters for current question

        Returns:
        correct_letter (str): The correct answer represented by a letter
        """
        for letter, answer in current_quiz_detail['answer_map'].items():
            if current_quiz_detail['correct_answer'] == answer:
                correct_letter = letter
        return correct_letter

    async def create_user_answers(self, reactions):
        """
        Returns the answer from each user's reaction to the question.

        Arguments:
        reactions (list): Reactions to a message

        Returns:
        user_answers (dict of str : list): Mapping of answer to users
        """
        emoji_dict = {'🇦':'A', '🇧':'B', '🇨':'C', '🇩':'D'}
        user_answers = {}
        for reaction in reactions:
            users = [user.name async for user in reaction.users()]
            users.remove('Robot')
            letter_answer = emoji_dict.get(reaction.emoji)
            if letter_answer:
                user_answers[letter_answer] = users
        return user_answers

    async def create_quiz_options(self, arg):
        """
        Creates a dictionary of quiz options from user provided arguments.

        Arguments:
        arg (tuple): Strings provided by user with selected quiz options

        Returns:
        quiz_options (dict of str : str): Mapping of user selected quiz options
        """
        quiz_options={'amount':'1'}
        for element in arg:
            if element.startswith('difficulty'):
                difficulty = element[len('difficulty='):]
                quiz_options['difficulty']=difficulty
            elif element.startswith('type'):
                type = element[len('type='):]
                quiz_options['type']=type
            elif element.startswith('category'):
                category = element[len('category='):]
                quiz_options['category'] = await self.find_category_id(category)
            elif element.startswith('amount'):
                count = element[len('amount='):]
                quiz_options['amount']=count
            else:
                print('Unrecognised argument from command !quiz_setup: ' + element, flush=True)
        return quiz_options

    #Takes in category string and finds category_id
    async def find_category_id(self, category):
        """
        Returns the category ID for use in the quiz_options dict.

        Arguments:
        category (str): Name of category provided by user

        Returns:
        category_id (int): ID of category
        """
        categories_dict = {
            'Animals': 27, 'Art': 25, 'Celebrities': 26,
            'Board_Games': 16, 'Books': 10, 'Cartoons': 32, 'Comics': 29,
            'Film': 11, 'Anime/Manga': 31, 'Music': 12, 'Theatre': 13,
            'Television': 14, 'Video_Games': 15, 'General_Knowledge': 9,
            'Geography': 22, 'History': 23, 'Mythology': 20, 'Politics': 24,
            'Science/Nature': 17, 'Computers': 18, 'Gadgets': 30, 'Maths': 19,
            'Sports': 21, 'Vehicles': 28
            }
        category_id = str(categories_dict[category])
        return category_id

    #Takes in quiz_options dictionary and creates quiz_url string
    async def create_quiz_url(self, quiz_options):
        """
        Returns a custom opentdb URL to retrieve the quiz from.

        Arguments:
        quiz_options (dict of str : str): Mapping of user selected quiz options

        Returns:
        quiz_url (str): URL to retrieve quiz data from.
        """
        quiz_url = "https://opentdb.com/api.php?"
        for key, item in quiz_options.items():
            quiz_url = quiz_url + key + '=' + item + '&'
        return quiz_url

    async def return_quiz_details(self, quiz_url):
        """
        Retrieves quizzes from opentdb or prints an error if unsuccessful.

        Arguments:
        quiz_url (str): URL to retrieve quiz data from.

        Returns:
        quiz_details (list): All quizzes retrieved from opentdb.com
        """
        response = requests.request("GET", quiz_url)
        if json.loads(response.text)['response_code']==0:
            quiz_details = json.loads(response.text)['results']
            for i in range(len(quiz_details)):
                quiz_details[i]['question'] = html.unescape(quiz_details[i]['question'])
                quiz_details[i]['correct_answer'] = html.unescape(quiz_details[i]['correct_answer'])
                for j in range(len(quiz_details[i]['incorrect_answers'])):
                    quiz_details[i]['incorrect_answers'][j] = html.unescape(quiz_details[i]['incorrect_answers'][j])
                quiz_details[i]['all_answers'] = quiz_details[i]['incorrect_answers'].copy()
                quiz_details[i]['all_answers'].append(quiz_details[i]['correct_answer'])
                random.shuffle(quiz_details[i]['all_answers'])
                quiz_details[i]['answer_map'] = {}
                for j in range(len(quiz_details[i]['all_answers'])):
                    quiz_details[i]['answer_map'][ascii_uppercase[j]] = quiz_details[i]['all_answers'][j]
        else:
            print('Error on Retrieving Quiz : '.format(json.loads(response.text)['response_code']), flush=True)
        return quiz_details

    async def create_answer_desc(self, current_quiz_detail):
        """
        Returns the message containing possible answers.

        Arguments:
        current_quiz_detail (dict): Mapping of quiz parameters for current question

        Returns:
        answer_desc (str): Multiple choice message to be sent by Robot
        """
        answer_desc = ''
        for letter, answer in current_quiz_detail['answer_map'].items():
            answer_desc = answer_desc + letter + " : " + answer + '\n'
        return(answer_desc)

async def setup(bot):
    await bot.add_cog(Quiz(bot))
