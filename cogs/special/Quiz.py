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
    async def setup(self, ctx, *arg):
        quiz_options = await self.create_quiz_options(arg)
        #print('Quiz_Options: ' + str(quiz_options), flush=True)
        quiz_url = await self.create_quiz_url(quiz_options)
        #print(quiz_url, flush=True)
        self.quiz_details = await self.return_quiz_details(quiz_url)
        #print(self.quiz_details, flush=True)
        self.q_num = 0

    @commands.command(hidden=True)
    async def question(self, ctx):
        question = self.quiz_details[self.q_num]['question']
        answer_desc = await self.create_answer_desc(self.quiz_details, self.q_num)
        embed = discord.Embed(title=question, description=answer_desc)
        self.question_msg = await ctx.send(embed=embed)
        self.q_num += 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return None

    @commands.command(hidden=True)
    async def check(self, ctx):
        event_message = await ctx.fetch_message(self.question_msg.id)
        reaction = event_message.reactions
        print(reaction, flush=True)

    #Takes in arg tuple and creates a quiz_options dictionary
    async def create_quiz_options(self, arg):
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
        categories_dict = {'Animals': 27, 'Art': 25, 'Celebrities': 26, 'Entertainment: Board Games': 16, 'Entertainment: Books': 10, 'Entertainment: Cartoon & Animations': 32, 'Entertainment: Comics': 29, 'Entertainment: Film': 11, 'Entertainment: Japanese Anime & Manga': 31, 'Entertainment: Music': 12, 'Entertainment: Musicals & Theatres': 13, 'Entertainment: Television': 14, 'Entertainment: Video Games': 15, 'General Knowledge': 9, 'Geography': 22, 'History': 23, 'Mythology': 20, 'Politics': 24, 'Science & Nature': 17, 'Science: Computers': 18, 'Science: Gadgets': 30, 'Science: Mathematics': 19, 'Sports': 21, 'Vehicles': 28}
        category_id = str(categories_dict[category])
        return category_id

    #Takes in quiz_options dictionary and creates quiz_url string
    async def create_quiz_url(self, quiz_options):
        quiz_url = "https://opentdb.com/api.php?"
        for key, item in quiz_options.items():
            quiz_url = quiz_url + key + '=' + item + '&'
        return quiz_url

    #Pings Quiz API and returns quiz_details
    async def return_quiz_details(self, quiz_url):
        response = requests.request("GET", quiz_url)
        if json.loads(response.text)['response_code']==0:
            quiz_details = json.loads(response.text)['results']
            for i in range(len(quiz_details)):
                quiz_details[i]['question'] = html.unescape(quiz_details[i]['question'])
                quiz_details[i]['correct_answer'] = html.unescape(quiz_details[i]['correct_answer'])
                quiz_details[i]['incorrect_answers'] = html.unescape(quiz_details[i]['incorrect_answers'])
                quiz_details[i]['all_answers'] = quiz_details[i]['incorrect_answers'].copy()
                quiz_details[i]['all_answers'].append(quiz_details[i]['correct_answer'])
                random.shuffle(quiz_details[i]['all_answers'])
                quiz_details[i]['answer_map'] = {}
                for j in range(len(quiz_details[i]['all_answers'])):
                    quiz_details[i]['answer_map'][ascii_uppercase[j]] = quiz_details[i]['all_answers'][j]
        else:
            print('Error on Retrieving Quiz : '.format(json.loads(response.text)['response_code']), flush=True)
        return quiz_details

    #Takes in quiz_details and creates answer_desc for embed
    async def create_answer_desc(self, quiz_details, q_num):
        answer_desc = ''
        for letter, answer in quiz_details[q_num]['answer_map'].items():
            answer_desc = answer_desc + letter + " : " + answer + '\n'
        return(answer_desc)

async def setup(bot):
    await bot.add_cog(Quiz(bot))
