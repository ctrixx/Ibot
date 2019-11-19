from main.models import Questions
import json
from nltk.chat.util import Chat, reflections



my_reflections ={
    "go":"gone",
    "hello":"hey there"
}

pairs = [
[
    r"my name is (.*)",
    ["Hello %1, How are you today ?",]
],
[
    r"what is your name ?",
    ["My name is Ibot and I'm a chatbot ?",]
],
[
    r"how are you ?",
    ["I'm doing good\nHow about You ?",]
],
[
    r"sorry (.*)",
    ["Its alright","Its OK, never mind",]
],
[
    r"i'm (.*) doing good",
    ["Nice to hear that","Alright :)",]
],
[
    r"what is your name ?",
    ["My name is Chatty and I'm a chatbot ?",]
],
[
    r"hi|hey|hello",
    ["Hello", "Hey there",]
],
[
    r"(.*) age?",
    ["I'm a computer program dude\nSeriously you are asking me this?",]
],
[
    r"what (.*) want ?",
    ["Make me an offer I can't refuse",]
],
[
    r"(.*) created ?",
    ["Nagesh created me using Python's NLTK library ",]
],
[
    r"(.*) (location|city) ?",
    ['Chennai, Tamil Nadu',]
],
[
    r"how is weather in (.*)?",
    ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1",]
],
[
    r"i work in (.*)?",
    ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
],
[
    r"(.*)raining in (.*)",
    ["No rain since last week here in %2","Damn its raining too much here in %2",]
],
[
    r"how (.*) health(.*)",
    ["I'm a computer program, so I'm always healthy ",]
],
[
    r"(.*) (sports|game) ?",
    ["I'm a very big fan of Football",]
],
[
    r"who (.*) sportsperson ?",
    ["Messy","Ronaldo","Roony",]
],
[
    r"who (.*) (moviestar|actor)?",
    ["Brad Pitt",]
],
[
    r"quit",
    ["BBye take care. See you soon :) ","It was nice talking to you. See you soon :)",]
],
    ]

def chatFunction(user_query):
    chat = Chat(pairs, reflections)
    response = chat.respond(user_query)
    return response

# Function to convert users query to a list/array form for assessment
# Convert Query to word list

def make_word_list(user_query):
    user_query = user_query.lower()
    lent = len(user_query)
    if user_query[lent-1] == "?":
        user_query = user_query[0:-1]
    split = list(user_query)
    words = []
    grp = ""
    for i in split:
        if i != " ":
            grp += i
        else:
            words.append(grp)
            grp = ""
    words.append(grp)
    return words




# Function to check content of query keywords for completeness and meaning

def checkStructure(user_query):
    questionHelpers = ['How','Where','Who','When','What','Find','Time','Locate','Located','Location','Day']
    totalmatch = 0
    queryLength = len(user_query)
    for word in user_query:
        for tag in questionHelpers:
            tag = tag.lower()
            if tag == word:
                totalmatch+=1
    if totalmatch >= queryLength:
        return 0
    else:
        return 1

# Function to remove unnecessary words and phrases from the query for effective score generation

def remove_unwanted(listt):
    unwanted = ['is', 'was', 'the', 'a', 'an', 'can', 'could', 'will', 'would', 'may', 'do', 'does','i','of']
    for word in unwanted:
        try:
            listt.remove(word)
        except:
            pass
    return listt


# Function to check the database for query match, calculate mach score and response


def check_question_database(query,raw_input,follow):
    all_questions = Questions.objects.all()
    if follow != []:
        query = query + follow
    # Initialize all scores and all responses for Zero (No id present for zero)
    all_responses = [0]
    all_scores = [0]
    setscore = 0
    structure_scores = []
    matchscores = {}
    attachments={}
    for row in all_questions:
        all_responses.append(row.Response)
        all_scores.append(row.MinMatchScore)
        '''try:
            questionstructures = row.QuestionKeywords.split('|')
        except:
            questionstructures = [row.QuestionKeywords]
        for structure in questionstructures:'''
        keyword = row.QuestionKeywords.split(',')
        for tag in keyword:
            tag = tag.lower()
            for word in query:
                if word == tag:
                    setscore += 1
        matchscores[row.id] = setscore
        attachments[row.id] = row.Attachment
        setscore = 0
    setscore = 0
    top = max(matchscores.values())

    # rid is for possible response id(s)
    # Adding the maximum scores related to the query to rid array

    rid=[]
    for i in matchscores.keys():
        if matchscores[i] == top:
            rid.append(i)

    # vrid means the possible verified response id

    vrid = []
    for id in rid:
        if top >= all_scores[id]:
            vrid.append(id)
    total_responses = len(vrid)
    if total_responses > 1:

        # Test for fuzzy query
        fuzzyholder= []
        fuzzymatchcount = 0
        fuzzymatchid = 0
        for id in rid:
            rowIndex = id-1
            fuzzy = all_questions[rowIndex].FuzzyResponse
            for j in fuzzyholder:
                if fuzzy == j:
                    fuzzymatchcount += 1
                    fuzzymatchid =rowIndex

            fuzzyholder.append(fuzzy)

        if fuzzymatchcount > 0:

            response_data = {}
            response_data["response_string"] = all_questions[fuzzymatchid].FuzzyResponse
            response_data["response_attachment"] = 0
            response_data["follow_up"] =raw_input
            return json.dumps(response_data)

        else:
            response_data={}
            response_data["response_string"] = "I'm not quite sure of what you are asking. Please be more specific."
            response_data["response_attachment"] = 0
            response_data["follow_up"] = "None"
            return json.dumps(response_data)

    elif total_responses < 1:

        # Test for fuzzy query
        fuzzyholder= []
        fuzzymatchcount = 0
        fuzzymatchid = 0
        queryStructure = checkStructure(query)
        for id in rid:
            rowIndex = id-1
            fuzzy = all_questions[rowIndex].FuzzyResponse
            for j in fuzzyholder:
                if fuzzy == j:
                    fuzzymatchcount += 1
                    fuzzymatchid =rowIndex

            fuzzyholder.append(fuzzy)
        if fuzzymatchcount > 0 and top >= 3 and queryStructure == 1:

            response_data = {}
            response_data["response_string"] = all_questions[fuzzymatchid].FuzzyResponse
            response_data["response_attachment"] = 0
            response_data["follow_up"]=raw_input
            return json.dumps(response_data)

        else:
                response = chatFunction(raw_input)
                response_data={}
                if response != None:
                    response_data["response_string"] = response
                else:
                    response_data["response_string"] = "Sorry, I don't have the answer to that question. Try rephrasing it, maybe I'll understand better."
                response_data["response_attachment"] = 0
                response_data["follow_up"] = "None"
                return json.dumps(response_data)

    else:
        # Create the response data to be returned to the user

        response_data={}
        response_data["response_string"] = all_responses[vrid[0]]
        response_data["response_attachment"] = attachments[vrid[0]]
        response_data["follow_up"] = "None"

        # Using the json.dumps function to convert to javascript readable object
        return json.dumps(response_data)


