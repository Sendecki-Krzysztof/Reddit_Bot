import praw
from praw.models import MoreComments
from gtts import gTTS
from playwright.sync_api import sync_playwright


def screenshotPost(currentNum, givenPost='', givenComment=''):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.set_viewport_size({'width': 1920, 'height': 1080})
        page.goto("https://www.reddit.com/" + givenPost)
        url = page.url
        page.goto(url + givenComment)
        image = str(currentNum) + '.png'
        page.screenshot(path=image)
        browser.close()


testBot = praw.Reddit(client_id='k1nwIrUWW716xJZpguPS1Q',
                      client_secret='_UEvS23EyGaIv12OUXXhSzXfLhp2vw',
                      user_agent='<console:MangoBot:0.1>')
postTitle = ''
subreddit = testBot.subreddit('AskReddit')
commentList = []
for post in subreddit.hot(limit=1):
    postTitle = post.title
    print(postTitle)
    print(post.id)
    screenshotPost(-1, post.id)
    currentComment = 0

    for comment in post.comments:
        if currentComment == 1:
            print(comment.id)
            screenshotPost(currentComment, post.id, comment.id)
        if isinstance(comment, MoreComments):
            continue
        if len(comment.body) > 20:
            commentList.append(comment.body)
            currentComment += 1

print(commentList[0])

textToSpeech = gTTS(text=(commentList[0]), lang='en')
textToSpeech.save('test.mp3')
