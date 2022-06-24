from pathlib import Path
import praw
from praw.models import MoreComments
from gtts import gTTS
from playwright.sync_api import sync_playwright
from mutagen.mp3 import MP3
from moviepy.editor import *

testBot = praw.Reddit(client_id='k1nwIrUWW716xJZpguPS1Q',
                      client_secret='_UEvS23EyGaIv12OUXXhSzXfLhp2vw',
                      user_agent='<console:MangoBot:0.1>')

subreddit = testBot.subreddit('AskReddit')
redditPost = None
videoLength = 0
commentList = []
audioList = []
clipList = []
H = 1080
W = 1920


# Takes a screenshot of the current site element,
# givenPost is the reddit Post id and givenComment is the reddit Comment id.
# currentNum is the resulting file name, if you wish to take a
# screenshot of the Post title input -1 here.
def screenshot(currentNum, givenPost='', givenComment=''):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.set_viewport_size({'width': 1920, 'height': 1080})
        page.goto("https://www.reddit.com/" + givenPost)
        url = page.url
        page.goto(url + givenComment)
        if not currentNum == -1:
            image = str(currentNum) + '.png'
            page.locator(f"#t1_{givenComment}").screenshot(path='./images/' + image)
        else:
            page.locator('[data-test-id="post-content"]').screenshot(path='./images/title.png')

        browser.close()


# Gets all the comments of a given post and inputs them into the commentsList
def getComments(post):
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue
        if comment.body in ["[removed]", "[deleted]"]:
            continue
        if len(comment.body) > 20:
            commentList.append(comment)


# Processes the Posts
def getPost():
    print("Getting Reddit Posts...")
    for post in subreddit.hot(limit=1):
        global redditPost
        redditPost = post

        # screenshots the title of post
        screenshot(-1, post.id)
        getComments(post)


getPost()
# makes sure dir exist...
Path("audio").mkdir(parents=True, exist_ok=True)
Path("images").mkdir(parents=True, exist_ok=True)

print("Creating audio and screenshots...")
titleMP3 = gTTS(text=redditPost.title, lang='en')
titleMP3.save('./audio/title.mp3')
titleAudio = AudioFileClip(f"audio/title.mp3")
audioList.append(titleAudio)
videoLength += MP3('./audio/title.mp3').info.length
total = 0
for comment in commentList:
    if videoLength <= 600:
        audio = gTTS(text=commentList[total].body, lang='en')
        screenshot(total, redditPost.id, commentList[total].id)
        audioDir = './audio/' + str(total) + '.mp3'
        audio.save(audioDir)
        audioList.append(AudioFileClip(audioDir))
        videoLength += MP3(audioDir).info.length
        total += 1
print(videoLength)

print("Creating final Video")
titleAudio = AudioFileClip(f"audio/title.mp3")
clipList.append(
    ImageClip("images/title.png")
        .set_duration(titleAudio.duration)
        .set_audio(titleAudio)
        .set_position('center')
)

for i in range(0, total):
    print(i)
    clipList.append(
        ImageClip('images/' + str(i) + ".png")
            .set_duration(audioList[i + 1].duration)
            .set_audio(audioList[i + 1])
            .set_position('center')
    )
imageConcat = concatenate_videoclips(clipList).set_position(("center", "center"))
audioComposite = CompositeAudioClip([concatenate_audioclips(audioList)])

imageConcat.resize(width=W, height=H)
background = ImageClip("Background.png").set_position("center")

final = CompositeVideoClip([background, imageConcat])
final = final.set_duration(audioComposite.duration)
final.write_videofile(str(redditPost.title) + ".mp4", fps=30, audio_codec='aac', audio_bitrate='192k')

print("done!")
