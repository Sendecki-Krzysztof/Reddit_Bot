import praw
from praw.models import MoreComments
from gtts import gTTS
from playwright.sync_api import sync_playwright

testBot = praw.Reddit(client_id='k1nwIrUWW716xJZpguPS1Q',
                      client_secret='_UEvS23EyGaIv12OUXXhSzXfLhp2vw',
                      user_agent='<console:MangoBot:0.1>')

postTitle = ""
subreddit = testBot.subreddit('AskReddit')
commentList = []
screenshotList = []
audioList = []


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
    currentComment = 0
    for comment in post.comments:
        if currentComment == 0:
            screenshot(currentComment, post.id, comment.id)
        if isinstance(comment, MoreComments):
            continue
        if comment.body in ["[removed]", "[deleted]"]:
            continue
        if len(comment.body) > 20:
            commentList.append(comment.body)
            currentComment += 1


def getPost():
    for post in subreddit.hot(limit=1):
        global postTitle
        postTitle = post.title

        # screenshots the title of post
        screenshot(-1, post.id)
        getComments(post)


getPost()
print(commentList[0])
print(postTitle)

textToSpeech = gTTS(text=(commentList[0]), lang='en')
textToSpeech.save('test.mp3')
