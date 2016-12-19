#PLEASE UPDATE VERSION NUMBER IF YOU MAKE SIGNIFICANT PROGRESS
#to find obscurity
#imports libraries
#os is used to clear console for percentage meter
#praw is the reddit api
#time is no longer used in program but was used for testing
#matplotlib's pyplot was used to graph findFrequency
#numpy also used for graphing purposes
import pip
import os
import time

def install(package):
    pip.main(['install', package])

try:
    import praw

except ImportError:
    install(praw)
    import praw
try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    install(matplotlib)
    import matplotlib.pyplot as plt
    import numpy as np


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

def findFrequency(networkData,searchWord):
    i = 0
    #iterates through the top x posts in a given subreddit decided earlier
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

freq = []

#variable used for percentage counter.
i = 0.0

#iterates through the array created from list.txt
for term in words:
    #initializes subreddit and how mant posts to go through
    data = reddit.subreddit(sub).hot(limit = int(postlim))
    #adds row frequency data to freq to use later in the graph.
    freq.append(findFrequency(data,term))
    #clears screen
    os.system('cls' if os.name == 'nt' else 'clear')
    #Increments percentage counter so the user isnt looking at a blank screen
    #for 20+ minutess
    print (str(float(i / len(words) * 100)) + "%  complete")
    i += 1
os.system('cls' if os.name == 'nt' else 'clear')
#prints raw data
#print(words)
#print(freq)

#uses raw data and puts it in a pretty graph.
graph(np.asarray(list(range(0,len(words)))),np.asarray(freq),words)
