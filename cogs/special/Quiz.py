import discord
from datetime import datetime as dt
import pytz
import requests
import json
from discord.ext import commands
import random
import html
from string import ascii_uppercase

Signature = "\n\nSincerely, Robot"

print('Special Cog Quiz Loaded', flush=True)

class Quiz(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Takes in Quiz Setup and retrieves response
    @commands.command(hidden=True)
    async def quiz_setup(self, ctx, *arg):
        quiz_options = await self.create_quiz_options(arg)
        print('Quiz_Options: ' + str(quiz_options), flush=True)
        quiz_url = await self.create_quiz_url(quiz_options)
        print(quiz_url, flush=True)

    #Takes in arg tuple and creates a quiz_options dictionary
    async def create_quiz_options(self, arg):
        quiz_options={}
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
            elif element.startswith('count'):
                count = element[len('count='):]
                quiz_options['count']=count
            else:
                print('Unrecognised argument from command !quiz_setup: ' + element, flush=True)
        return quiz_options

    #Takes in category string and finds category_id
    async def find_category_id(self, category):
        categories_dict = {'Animals': 27, 'Art': 25, 'Celebrities': 26, 'Entertainment: Board Games': 16, 'Entertainment: Books': 10, 'Entertainment: Cartoon & Animations': 32, 'Entertainment: Comics': 29, 'Entertainment: Film': 11, 'Entertainment: Japanese Anime & Manga': 31, 'Entertainment: Music': 12, 'Entertainment: Musicals & Theatres': 13, 'Entertainment: Television': 14, 'Entertainment: Video Games': 15, 'General Knowledge': 9, 'Geography': 22, 'History': 23, 'Mythology': 20, 'Politics': 24, 'Science & Nature': 17, 'Science: Computers': 18, 'Science: Gadgets': 30, 'Science: Mathematics': 19, 'Sports': 21, 'Vehicles': 28}
        category_id = str(categories_dict[category])
        return category_id

    #Takes in quiz_options dictionary and creates quiz_url string
    async def create_quiz_url(self, quiz_options):
        quiz_url = "https://opentdb.com/api.php?"
        for key, item in quiz_options.items():
            quiz_url = quiz_url + key + '=' + item + '&'
        return quiz_url




    """
    async def return_quiz(self,):
        #unpack dictionary and ping quiz_url
        #if valid then return results

        https://opentdb.com/api.php?amount=10
        &category=12
        &difficulty=easy
        &type=boolean






        quizurl = "https://opentdb.com/api.php?amount=3"
        response = requests.request("GET", quizurl)
        quiz_details = json.loads(response.text)['results'][0]
        print(json.loads(response.text), flush=True)



    #Plays Quiz Theme
    async def play_theme(self):

    #Ends Quiz
    @commands.command(hidden=True)
    async def quiz_end(self, ctx):

    #Creates
    async def create_description(self, all_answer):
        if len(all_answer)==2:
            answers_str = 'True\nFalse'
        elif len(all_answer)==4:
            random.shuffle(all_answer)
            self.answers_dict = {}
            answers_str = ''
            for letter, answer in zip(ascii_uppercase[:4], all_answer):
                self.answers_dict[letter] = answer
                answers_str += letter + ' : ' + answer + '\n'
        return answers_str


    async def set_colour(self,)

    @commands.command(hidden=True)
    async def quiz(self, ctx):

        question = html.unescape(quiz_details['question'])
        self.correct_answer = html.unescape(quiz_details['correct_answer'])
        all_answer = quiz_details['incorrect_answers']
        all_answer.append(self.correct_answer)



        embed = discord.Embed(title=question, description=answers_str, color=discord.Colour.dark_purple())
        await ctx.send(embed=embed)
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return None
        else:
            print('{} guessed {}'.format(message.author, self.answers_dict.get(message.content)), flush=True)
            if self.answers_dict.get(message.content) == self.correct_answer:
                await message.channel.send('Correct!')

async def setup(bot):
    await bot.add_cog(Quiz(bot))
