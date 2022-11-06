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
    @commands.command()
    async def setup(self, ctx, *arg):
        quiz_options = await self.create_quiz_options(arg)
        #print('Quiz_Options: ' + str(quiz_options), flush=True)
        quiz_url = await self.create_quiz_url(quiz_options)
        #print(quiz_url, flush=True)
        self.quiz_details = await self.return_quiz_details(quiz_url)
        #print(self.quiz_details, flush=True)
        await self.ask_question(ctx)

    @commands.command()
    async def question(self, ctx):
        await self.ask_question(ctx)

    async def ask_question(self, ctx):
        self.current_quiz_detail = self.quiz_details.pop()
        question = self.current_quiz_detail['question']
        answer_desc = await self.create_answer_desc(self.current_quiz_detail)
        embed = discord.Embed(title=question, description=answer_desc)
        self.question_msg = await ctx.send(embed=embed)
        for reaction in {'🇦':'A', '🇧':'B', '🇨':'C', '🇩':'D'}.keys():
            await self.question_msg.add_reaction(reaction)


    @commands.command()
    async def lock_in(self, ctx):
        event_message = await ctx.fetch_message(self.question_msg.id)
        reactions = event_message.reactions
        user_answers = await self.create_user_answers(reactions)
        user_count={}
        for key, value in user_answers.items():
            for user in value:
                user_count[user] = user_count.get(user, 0) + 1
        for key, value in user_count.items():
            if value > 1:
                await ctx.send(key + " guessed more than once!")
                return None
        correct_users = await self.check_user_answers(user_answers, self.current_quiz_detail)
        if correct_users:
            message = 'Correct Users: ' + ' '.join(correct_users)
        else:
            message = 'No Correct Users'
        await ctx.send(message)
        await self.ask_question(ctx)

    #Takes in user_answers and current_quiz_detail and returns correct_users
    async def check_user_answers(self, user_answers, current_quiz_detail):
        #print(current_quiz_detail, flush=True)
        correct_users = []
        for letter, answer in current_quiz_detail['answer_map'].items():
            if current_quiz_detail['correct_answer'] == answer:
                correct_letter = letter
        for letter, users in user_answers.items():
            if letter == correct_letter:
                correct_users = users
        return correct_users

    #Takes in reactions and creates a user_answers dictionary
    async def create_user_answers(self, reactions):
        emoji_dict = {'🇦':'A', '🇧':'B', '🇨':'C', '🇩':'D'}
        user_answers = {}
        for reaction in reactions:
            users = [user.name async for user in reaction.users()]
            users.remove('Robot')
            user_answer = emoji_dict.get(reaction.emoji)
            if user_answer:
                user_answers[user_answer] = users
        return user_answers

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
        categories_dict = {'Animals': 27, 'Art': 25, 'Celebrities': 26, 'Board_Games': 16, 'Books': 10, 'Cartoons': 32, 'Comics': 29, 'Film': 11, 'Anime/Manga': 31, 'Music': 12, 'Theatre': 13, 'Television': 14, 'Video_Games': 15, 'General_Knowledge': 9, 'Geography': 22, 'History': 23, 'Mythology': 20, 'Politics': 24, 'Science/Nature': 17, 'Computers': 18, 'Gadgets': 30, 'Maths': 19, 'Sports': 21, 'Vehicles': 28}
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

    #Takes in quiz_details and creates answer_desc for embed
    async def create_answer_desc(self, current_quiz_detail):
        answer_desc = ''
        for letter, answer in current_quiz_detail['answer_map'].items():
            answer_desc = answer_desc + letter + " : " + answer + '\n'
        return(answer_desc)

async def setup(bot):
    await bot.add_cog(Quiz(bot))
