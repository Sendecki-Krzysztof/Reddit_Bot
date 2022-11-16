from pathlib import Path
import praw
from praw.models import MoreComments
from gtts import gTTS
from playwright.sync_api import sync_playwright
from moviepy.editor import *

testBot = praw.Reddit(client_id='k1nwIrUWW716xJZpguPS1Q',
                      client_secret='_UEvS23EyGaIv12OUXXhSzXfLhp2vw',
                      user_agent='<console:MangoBot:0.1>')

subreddit = testBot.subreddit('AskReddit')
audioList = []
clipList = []
H = 1080
W = 1920


# Checks if the directories of audio and images exist. if they don't then create them.
def CheckDirectories():
    Path("audio").mkdir(parents=True, exist_ok=True)
    Path("images").mkdir(parents=True, exist_ok=True)


# Takes a screenshot of the current site element,
# givenPost is the reddit Post id and givenComment is the reddit Comment id.
# currentNum is the resulting file name, if you wish to take a
# screenshot of the Post title input -1 here.
def screenshot(index, givenPost='', givenComment=''):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({'width': 1920, 'height': 1080})
        page.goto("https://www.reddit.com/" + givenPost)
        url = page.url
        page.goto(url + givenComment)
        page.wait_for_timeout(1000)
        if not index == -1:
            image = str(index) + '.png'
            page.locator(f"#t1_{givenComment}").screenshot(path='./images/' + image)
        else:
            page.locator('[data-test-id="post-content"]').screenshot(path='images/title.png')

        browser.close()


# Gets all the comments of a given post and inputs them into the commentsList
def getComments(post):
    commentList = []
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue
        if comment.body in ["[removed]", "[deleted]"]:
            continue
        if len(comment.body) > 20:
            commentList.append(comment)
    return commentList


# Processes the post first post in "hot" of the given subreddit also puts all the posts
def getPost():
    post = None
    comments = None
    for post in subreddit.hot(limit=1):
        post = post

        # screenshots the title of post
        screenshot(-1, post.id)
        comments = getComments(post)
    return post, comments


# Takes a string input name and an GTTS audio file as audio to create a MoviePy Clip
# Adds both to there respective list
def createClip(name, audio):
    print("Creating " + name + ": Clip...", end="")
    print("Audio...", end="")
    tAudio = AudioFileClip("./audio/" + name + ".mp3")

    print("ImageClip...", end="")
    tClip = ImageClip("images/" + name + ".png")
    tClip.duration = tAudio.duration
    tClip.audio = tAudio
    tClip.pos = 'center'
    print("Done")
    clipList.append(tClip)
    audioList.append(tAudio)


if __name__ == "__main__":
    print("Getting Reddit Post...")
    redditPost, postComments = getPost()  # Get the reddit post and the comments of that post
    CheckDirectories()

    print("Creating audio and screenshots...")

    titleMP3 = gTTS(text=redditPost.title, lang='en')
    titleMP3.save('./audio/title.mp3')
    createClip("title", titleMP3)
    videoLength = audioList[0].duration
    clipNum = 1
    for comment in postComments:
        if videoLength < 45:
            commentAudio = gTTS(text=comment.body, lang='en')
            commentAudio.save('./audio/' + str(clipNum) + '.mp3')
            screenshot(clipNum, redditPost.id, comment.id)
            createClip(str(clipNum), commentAudio)
            videoLength += audioList[clipNum].duration
            clipNum += 1
        else:
            break
    print("video length will be:", videoLength)

    print("Finalizing Video...")
    imageConcat = concatenate_videoclips(clipList).set_position(("center", "center"))
    audioComposite = CompositeAudioClip([concatenate_audioclips(audioList)])
    imageConcat.resize(width=W, height=H)
    background = ImageClip("Background.png").set_position("center")

    final = CompositeVideoClip([background, imageConcat])
    final = final.set_duration(audioComposite.duration)
    final.write_videofile("title.mp4", fps=24)
