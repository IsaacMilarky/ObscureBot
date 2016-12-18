#to find obscurity

import praw
import time
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


def term_detection(string,term):
    occurances = 0
    list1 = string.split()
    for word in list1:
        if term == word:
            occurances += 1
    return occurances


def findFrequency(networkData,searchWord):
    i = 0
    for submission in networkData:
        for comment in submission.comments:
            i += term_detection(comment.body,term)
    return i


def graph(xAxis,yAxis,words):
    const = 300
    plt.xticks(rotation=30)
    plt.xticks(xAxis,words, fontsize = const / len(words))
    plt.plot(xAxis,yAxis, 'ro')
    #for x in range(len(xAxis) - 1):
    #    print(str(x) + "= " + str(words[x]))
    plt.show()


def prompt(dir):
    choice = raw_input("Do you want to enter new words(y/n): ")
    if choice == 'y':
        user_input = open(dir,"a+")
        searchform = raw_input("Please enter in search terms(with spaces between): ")
        list = searchform.split()
        for term in list:
            user_input.write(str(term) + "\n")
        user_input.close()
    return arraywords(dir)
choice = ''


while True:
    choice = raw_input("Do you have a specific text file of terms to check for (y/n): ")
    if choice == 'y':
        directory = raw_input("Enter the directory of the file: ")
        words = prompt(directory)
        break
    elif choice == 'n':
        words = prompt("list.txt")
        break
    else:
        print("try again")


#asks user for search term
sub = raw_input("What subreddit should I search?: ")
postlim = 10#int(raw_input("How many posts should I search: "))
# logs into reddit
reddit = praw.Reddit(client_id='IcZ2s5Xu1eTCRw',
client_secret='hIjaSArp-M7YAkd2gFgHQIJgOYg',
user_agent='Windows:ObscureBot:0.1 (by /u/CakeHD)',
username='Obscurebot',
password='greengoblin')


freq = []
i = 0.0
for term in words:
    data = reddit.subreddit(sub).hot(limit = postlim)
    freq.append(findFrequency(data,term))
    print (str(float(i / len(words) * 100)) + "%  complete")
    i += 1
graph(np.asarray(list(range(0,len(words)))),np.asarray(freq),words)
