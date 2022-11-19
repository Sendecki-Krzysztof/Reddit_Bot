from os.path import isfile
from pathlib import Path
from praw.models import MoreComments
from gtts import gTTS
from playwright.sync_api import sync_playwright
from moviepy.editor import *
import praw
import json


def login(page):
    print("Logging into Reddit Account...", end="")
    if isfile("AccountDetails.json"):
        with open('AccountDetails.json', 'r') as openfile:
            accountDetails = json.load(openfile)
        page.goto("https://www.reddit.com/")
        page.locator('role=button[name="Log In"]').click()
        page.frame_locator("#SHORTCUT_FOCUSABLE_DIV iframe").get_by_placeholder("\n        Username\n      ").fill(
            accountDetails["username"])
        page.frame_locator("#SHORTCUT_FOCUSABLE_DIV iframe").get_by_placeholder("\n        Password\n      ").click()
        page.frame_locator("#SHORTCUT_FOCUSABLE_DIV iframe").get_by_placeholder("\n        Password\n      ").fill(
            accountDetails["password"])
        page.frame_locator("#SHORTCUT_FOCUSABLE_DIV iframe").get_by_placeholder("\n        Password\n      ").press(
            "Enter")
        page.wait_for_url("https://www.reddit.com/")
        page.get_by_role("button", name="Close").click()
        page.get_by_role("link", name="User avatar").click()
        print("Success!")
    else:
        print("Failed!")


# Takes in a list of comments to screenshot and the post to screenshot from, outputs them all into the images' folder.
def screenshot(post, toScreenshot):
    with sync_playwright() as p:
        print("Taking Screenshot...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size({'width': 1920, 'height': 1080})

        login(page)

        page.goto("https://www.reddit.com/" + str(post.id))

        url = page.url
        for i in range(0, len(toScreenshot)):
            print("Taking Screenshot ", i, "...", end="")
            page.goto(url + toScreenshot[i].id)
            if i == 0:
                page.locator('[data-test-id="post-content"]').screenshot(path='images/0.png')
                page.goto(url + toScreenshot[i].id)
                page.locator('[data-test-id="post-content"]').screenshot(path='images/0.png')
            else:
                page.locator(f"#t1_{toScreenshot[i].id}").screenshot(path='./images/' + str(i) + '.png')
            print("Done!")

        context.close()
        browser.close()


# Checks if the directories of audio and images exist. if they don't then create them.
def CheckDirectories():
    print("Checking Directories...", end="")
    Path("audio").mkdir(parents=True, exist_ok=True)
    print("audio...", end="")

    Path("images").mkdir(parents=True, exist_ok=True)
    print("images...Done!", end="")
    print()


# Uses the BotDetails.json file to create a bot using the praw wrapper. Returns the created reddit bot object
def createBot():
    print("Creating Bot...", end="")
    with open('BotDetails.json', 'r') as openfile:
        botDetails = json.load(openfile)

    bot = praw.Reddit(client_id=botDetails['client_id'],
                      client_secret=botDetails['client_secret'],
                      user_agent=botDetails['user_agent'])
    print("Done!")
    return bot


# Takes the User defined subreddit and returns the first post within it. (when searching by hot)
def getPost(subreddit):
    print("Getting Post...", end="")
    for post in subreddit.hot(limit=1):
        return post


# Takes in a post and an empty list to be filled with comment ids. It also takes the optional value minWordCount,
# This will make sure all posts have at least that many characters
def getComments(post, commentList, minWordCount=20):
    print("Comments...", end="")
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue
        if comment.body in ["[removed]", "[deleted]"]:
            continue
        if len(comment.body) > minWordCount:
            commentList.append(comment)

    print("Done!")


# Finds the Comments to add to the video and then appends them to the screenshot list. It also creates the audio
# files that will be needed for the video finalization. Breaks when the video length is greater than the desired length
def getVideoClips(screenshotsToTake, audioList, finalVideoLength, comments):
    print("Finding Video Clips...")
    titleMP3 = gTTS(text=screenshotsToTake[0].title, lang='en')
    titleMP3.save('./audio/0.mp3')
    audioList.append(AudioFileClip("./audio/0.mp3"))
    currentLength = audioList[0].duration
    includedClips = 1
    for comment in comments:
        if currentLength < finalVideoLength:
            print("Finding Clip ", includedClips, "...", end="")
            MP3 = gTTS(text=comment.body, lang='en')
            MP3.save('./audio/' + str(includedClips) + '.mp3')
            audioList.append(AudioFileClip('./audio/' + str(includedClips) + '.mp3'))
            MP3duration = audioList[includedClips].duration
            screenshotsToTake.append(comment)
            currentLength += MP3duration
            includedClips += 1
            print("Done!")
        else:
            print("Final video will be", currentLength, "seconds Long and have", includedClips - 1, "Clips!")
            break


def generateClips(clips, audioList):
    for i in range(0, len(audioList)):
        print("Creating " + str(i) + ": Clip...", end="")
        clip = ImageClip("images/" + str(i) + ".png")
        clip.duration = audioList[i].duration
        clip.audio = audioList[i]
        clip.pos = 'center'
        clips.append(clip)
        print("Done!")


def createFinalVideo(clips, sounds, name, height=1080, width=1920):
    imageConcat = concatenate_videoclips(clips).set_position(("center", "center"))
    audioComposite = CompositeAudioClip([concatenate_audioclips(sounds)])
    imageConcat.resize(width=width, height=height)
    background = ImageClip("Background.png").set_position("center")

    final = CompositeVideoClip([background, imageConcat])
    final = final.set_duration(audioComposite.duration)
    final.write_videofile(name, fps=24)


def createVideo(finalVideoLength, chosenSubreddit):
    screenshotsToTake = []
    audioList = []
    clips = []
    comments = []

    CheckDirectories()
    bot = createBot()

    subreddit = bot.subreddit(chosenSubreddit)

    post = getPost(subreddit)
    getComments(post, comments)

    screenshotsToTake.append(post)
    getVideoClips(screenshotsToTake, audioList, finalVideoLength, comments)

    screenshot(post, screenshotsToTake)

    generateClips(clips, audioList)

    createFinalVideo(clips, audioList, "Video.mp4")
