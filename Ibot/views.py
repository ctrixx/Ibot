from django.shortcuts import render
from django.http import HttpResponse
from main import bot_functions as botf





def index(request):
    return render(request, 'Ibot/index.html')


def full(request):
    return render(request, "Ibot/full-screen-chat.html")


def help(request):
    return render(request, "Ibot/help.html")


# View rendered to submit query and return response

def submit(request):
    user_query = request.GET.get('query')
    words = botf.make_word_list(user_query)
    words = botf.remove_unwanted(words)
    reply = botf.check_question_database(words,user_query)
    return HttpResponse(reply)

