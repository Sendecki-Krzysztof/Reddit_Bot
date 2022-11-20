from os.path import isfile
import Bot
import PySimpleGUI as sg
import json

sg.theme('SandyBeach')
appOpen = True


# creates the Layout for the Json Reddit account create Window
def jsonAccountLayout():
    redditAccountCreate = [
        [sg.Text('Reddit Account Json Info')],
        [sg.Text('username:'), sg.InputText(size=(15, 1))],
        [sg.Text('password:'), sg.InputText(size=(15, 1))],
        [sg.Button("Create"), sg.Cancel()]
    ]
    return redditAccountCreate


# Handles the json Creation window
def makeAccountJson():
    redditAccount = {
        "username": "",
        "password": ""
    }

    redditBotGUI = sg.Window('Simple data entry window', jsonAccountLayout())
    accountMakerEvent, accountMakerValues = redditBotGUI.read()
    if accountMakerEvent == "Create":
        redditAccount['username'] = accountMakerValues[0]
        redditAccount['password'] = accountMakerValues[1]

        botJson = json.dumps(redditAccount, indent=2)
        with open("AccountDetails.json", "w") as output:
            output.write(botJson)

    redditBotGUI.close()


# creates the Layout for the Json create Reddit bot Window
def jsonBotLayout():
    redditBotCreate = [
        [sg.Text('Reddit Bot Json Info')],
        [sg.Text('client_id:', size=(10, 1)), sg.InputText(size=(15, 1))],
        [sg.Text('client_secret:'), sg.InputText(size=(15, 1))],
        [sg.Text('user_agent:', size=(10, 1)), sg.InputText(size=(15, 1))],
        [sg.Button("Create"), sg.Cancel()]
    ]
    return redditBotCreate


# Handles the json Creation window
def makeBotJson():
    redditBot = {
        "client_id": "",
        "client_secret": "",
        "user_agent": ""
    }

    BotLayout = jsonBotLayout()
    redditBotGUI = sg.Window('Simple data entry window', BotLayout)
    botMakerEvent, botMakerValues = redditBotGUI.read()
    if botMakerEvent == "Create":
        redditBot['client_id'] = botMakerValues[0]
        redditBot['client_secret'] = botMakerValues[1]
        redditBot['user_agent'] = botMakerValues[2]

        botJson = json.dumps(redditBot, indent=3)
        with open("BotDetails.json", "w") as output:
            output.write(botJson)

    redditBotGUI.close()


def checkStatus(filename, key):
    if isfile(filename):
        mainMenu[key].update(key + 'Status: detected!', text_color='Green')
    else:
        mainMenu[key].update(key + 'Status: not detected!', text_color='Red')


MainMenu = [
    [sg.Text('Bot Status:', key="Bot"), sg.Button("Create Bot json")],
    [sg.Text('Account Status:', key="Account"), sg.Button("Create Account json")],
    [sg.Text('Video Length (in seconds):'), sg.InputText(size=(15, 1)), sg.Text('default: 45s')],
    [sg.Text('Video Subreddit:'), sg.InputText(size=(15, 1)), sg.Text('default: "AskReddit"')],
    [sg.Text('Number of Videos:'), sg.InputText(size=(15, 1)), sg.Text('default: 1')],
    [sg.Text('Sorting Comments:'),
     sg.Radio("Best", "sortComments", default=True, key='best'),
     sg.Radio("Top", "sortComments", key='top'),
     sg.Radio("New", "sortComments", key='new'),
     sg.Radio("Hot", "sortComments", key='hot'),
     sg.Radio("Controversial", "sortComments", key='controversial')],
    [sg.Text('Sorting Subreddit Posts:'),
     sg.Radio("Rising", "sortPost", key='Rising'),
     sg.Radio("Top", "sortPost", key='Top'),
     sg.Radio("New", "sortPost", key='New'),
     sg.Radio("Hot", "sortPost", default=True, key='Hot'),
     sg.Radio("Controversial", "sortPost", key='Controversial')],
    [sg.Button("Close"), sg.Button("Create Video")]
]


def handleVideoCreation(values):
    videoLength = 45
    subreddit = "AskReddit"
    videoNumber = 1
    commentSort = "best"
    subredditSort = "top"
    print(values[0], values[1], values[2])
    if not values[0] == '':
        videoLength = int(values[0])
    if not values[1] == '':
        subreddit = str(values[1])
    if not values[2] == '':
        videoNumber = int(values[2])

    # Decide which value to sort by.
    commentSortFound = False
    subSortFound = False
    for value in values:
        if values[value] and not commentSortFound:
            commentSort = str(value).lower()
            commentSortFound = True
        elif values[value] and not subSortFound:
            subredditSort = str(value).lower()
            commentSortFound = True


    Bot.createVideo(videoLength, subreddit, videoNumber, commentSort, subredditSort)


mainMenu = sg.Window('Reddit Video Maker', MainMenu, finalize=True)

checkStatus("BotDetails.json", 'Bot')
checkStatus("AccountDetails.json", "Account")

event, values = mainMenu.read()
while appOpen:

    if event == "Create Bot json":
        makeBotJson()
        checkStatus("BotDetails.json", 'Bot')
    elif event == "Create Account json":
        makeAccountJson()
        checkStatus("AccountDetails.json", "Account")
    elif event == "Create Video":
        handleVideoCreation(values)

    elif event == "Close" or event == sg.WIN_CLOSED:
        print("Closing...")
        mainMenu.close()
        appOpen = False
    event, values = mainMenu.read()

print("Application Closed")
