#to find obscurity
#imports libraries
#os is used to clear console for percentage meter
#praw is the reddit api
#matplotlib's pyplot was used to graph findFrequency
#numpy also used for graphing purposes
import pip
import os
import time

#set if debug mode is on or not
CONST_DEBUG = True

def install(package):
    pip.main(['install', package])
"""
def install(name):
    subprocess.call(['pip', 'install', name])
"""

try:
    import praw

except ImportError:
    install("praw")

import praw

try:
    import matplotlib.pyplot as plt
except ImportError:
    install("matplotlib")

import matplotlib.pyplot as plt
try:
    import numpy as np
except ImportError:
    install("numpy")

import numpy as np

try:
    import progressbar
except ImportError:
    install("progressbar2")
import progressbar

words = []

def arraywords(dir):
    file = open(dir, "r")
    words = []
    for word in file:
        words.append(word.rstrip())
    file.close()
    return words

#finds how many occurances of a term happen in a string
def term_detection(string,term):
    #initializes total variable
    occurances = 0
    #splits string into a list of words to iterate through
    list1 = string.split()
    #iterates through words
    for word in list1:
        #tests to see if term current word.
        if term == word:
            #increments total var if term is in string
            occurances += 1
    return occurances

def findFrequency(networkData,searchWord,postlimit):
    i = 0
    j = 0
    #iterates through the top x posts in a given subreddit decided earlier
    with progressbar.ProgressBar(max_value=int(postlimit)) as bar:
        for submission in networkData:
            #used for testing in early period
            #print(submission.title)
            #print("--------------------------------------------------------------")
            i += term_detection(submission.title,searchWord)
            #Prevents the MoreComments object from causing any trouble
            #by removing it if it is encountered.

            submission.comments.replace_more(limit=0)
            #iterates through comments in top x submissons
            for comment in submission.comments:
                #was throwing an error when comment chains were too longer
                #apparently some comments have the attribute "MoreComments"
                #this fixes the problems
                try:
                    #increments i for frequncy determined by term_detection
                    i += term_detection(comment.body,searchWord)
                #Made a fix on line 64 that should make it sou that
                #this exception should never happen but you never know
                except AttributeError:
                    print("MoreCommntsError: Tell the programmers!")
            j += 1
            bar.update(j)
    os.system("cls" if os.name == "nt" else "clear")
    return i

#Graph function written by Pete using matplotlib and pychart
def graph(xAxis,yAxis,words):
    const = 300
    plt.xticks(rotation=30)
    plt.xticks(xAxis,words, fontsize = const / len(words))
    plt.plot(xAxis,yAxis, 'ro')
    #for x in range(len(xAxis) - 1):
    #    print(str(x) + "= " + str(words[x]))
    plt.show()

def prompt(dir):
    if not CONST_DEBUG:
        choice = input("Do you want to enter new words(y/n): ")
    if choice == 'y':
        user_input = open(dir,"a+")
        searchform = input("Please enter in search terms(with spaces between): ")
        list = searchform.split()
        for term in list:
            user_input.write(str(term) + "\n")
        user_input.close()
    return arraywords(dir)
'''
#prompts user for data.
def prompt(dir):
    #Catches exeption if the user decides to be an ass.
    try:
        user_input = open(dir,"a+")
        searchform = input("Enter in search terms(with spaces between): ")
        list = searchform.split()
        for term in list:
      	     user_input.write(str(term) + "\n")
        user_input.close()
    except not user_input == type(string):
        print("Wrong type dummy!")
        #recurses if exeption is caught
        prompt(dir)
'''
choice = ''
if  not CONST_DEBUG:
    while True:
        choice = input("Do you have a specific text file of terms to check for (y/n): ")
        if choice == 'y':
            directory = input("Enter the directory of the file: ")
            words = prompt(directory)
            break
        elif choice == 'n':
            words = prompt("list.txt")
            break
        else:
            print("try again")


    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Please enter how you would like to sort posts.")
        try:
            sortChoice = input("Choices = \'top\' \'hot\' \'controversial\' \'new\': ")
            if sortChoice == "top" or sortChoice == "hot" or sortChoice == "controversial" or sortChoice == "new":
                break
            else:
                print("Please enter in a valid sort choice. ")
        except NameError:
            print("NameError: Please enter in a valid sort choice.")
else:
    words = arraywords("list.txt")
    sortChoice = "top"

# logs into reddit and creates reddit instance
#instance is not in read only mode so in theory we could manipulate
#here lies version number(line 105)
#posts if we wished
#don't ask
reddit = praw.Reddit(client_id='IcZ2s5Xu1eTCRw',
client_secret='hIjaSArp-M7YAkd2gFgHQIJgOYg',
user_agent='Windows:ObscureBot:1.2 (by /u/CakeHD)',
username='Obscurebot',
password='greengoblin')

#function needs to be here because it uses reddit instance
def is_a_sub_real(sub):
    try:
        #Tries to get first (2) subs of a a given subreddit
        for x in reddit.subreddit(sub).hot(limit = 2):
            print()
    #if program fails in getting first 2 posts it returns false
    except:
        return False
    #returns true if program succeeds.
    return True

if not CONST_DEBUG:
    #asks user for subreddit and how many posts to search through.
    while True:
        sub = input("What subreddit should I search?: ")
        postlim = input("How many posts should I look through?: ")

        #If user inputs a typo or is an idiot it gives them another chance
        if not is_a_sub_real(sub) and not postlim > 0:
            if not is_a_sub_real(sub):
                print("ERROR: Sub is either empty  or does not exist!")
            elif not postlim > 0:
                print("ERROR: Post limit is too small!")
            else:
                print("Two(2) ERRORs Occured: Sub doesnt exist and post limit is too small!")
        else:
            break
else:
    sub = "wholesomememes"
    postlim = "10"
#with progressbar.ProgressBar(max_value=10) as bar:
freq = []

#variable used for percentage counter.
i = 1.0
#iterates through the array created from list.txt
if sortChoice == "top":
    #clears screen
    os.system('cls' if os.name == 'nt' else 'clear')
    with progressbar.ProgressBar(max_value=len(words)) as bar:
        for term in words:
            #initializes subreddit and how mant posts to go through
            print("----------General-Progress(above)----------------Post-Progress(below)---------------------------------")
            data = reddit.subreddit(sub).top(limit = int(postlim))
            #adds row frequency data to freq to use later in the graph.
            freq.append(findFrequency(data,term,postlim))
            #Increments percentage counter so the user isnt looking at a blank screen
            #for 20+ minutess
            #print (str(float((i + 1) / len(words) * 100)) + "%  complete")
            bar.update(i)
            i += 1
            #os.system('cls' if os.name == 'nt' else 'clear')
if sortChoice == "hot":
    #clears screen
    os.system('cls' if os.name == 'nt' else 'clear')
    with progressbar.ProgressBar(max_value=10) as bar:
        for term in words:
            #initializes subreddit and how mant posts to go through
            data = reddit.subreddit(sub).hot(limit = int(postlim))
            print("----------General-Progress(above)----------------Post-Progress(below)---------------------------------")
            #adds row frequency data to freq to use later in the graph.
            freq.append(findFrequency(data,term,postlim))
            #Increments percentage counter so the user isnt looking at a blank screen
            #for 20+ minutess
            #print (str(float((i + 1) / len(words) * 100)) + "%  complete")
            bar.update(i)
            i += 1
            #os.system('cls' if os.name == 'nt' else 'clear')
if sortChoice == "controversial":
    #clears screen
    os.system('cls' if os.name == 'nt' else 'clear')
    with progressbar.ProgressBar(max_value=10) as bar:
        for term in words:
            #initializes subreddit and how mant posts to go through
            data = reddit.subreddit(sub).controversial(limit = int(postlim))
            print("----------General-Progress(above)----------------Post-Progress(below)---------------------------------")
            #adds row frequency data to freq to use later in the graph.
            freq.append(findFrequency(data,term,postlim))
            #Increments percentage counter so the user isnt looking at a blank screen
            #for 20+ minutess
            #print (str(float((i + 1) / len(words) * 100)) + "%  complete")
            bar.update(i)
            i += 1
            #os.system('cls' if os.name == 'nt' else 'clear')
if sortChoice == "new":
    #clears screen
    os.system('cls' if os.name == 'nt' else 'clear')
    with progressbar.ProgressBar(max_value=10) as bar:
        for term in words:
            #initializes subreddit and how mant posts to go through
            data = reddit.subreddit(sub).new(limit = int(postlim))
            print("----------General-Progress(above)----------------Post-Progress(below)---------------------------------")
            #adds row frequency data to freq to use later in the graph.
            freq.append(findFrequency(data,term,postlim))
            #Increments percentage counter so the user isnt looking at a blank screen
            #for 20+ minutess
            #print (str(float((i + 1)/ len(words) * 100)) + "%  complete")
            bar.update(i)

            i += 1
            #os.system('cls' if os.name == 'nt' else 'clear')
os.system('cls' if os.name == 'nt' else 'clear')
#prints raw data
print(words)
print(freq)

#uses raw data and puts it in a pretty graph.
graph(np.asarray(list(range(0,len(words)))),np.asarray(freq),words)
