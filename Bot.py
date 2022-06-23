import praw
from praw.models import MoreComments
from gtts import gTTS

testBot = praw.Reddit(client_id='k1nwIrUWW716xJZpguPS1Q',
                      client_secret='_UEvS23EyGaIv12OUXXhSzXfLhp2vw',
                      user_agent='<console:MangoBot:0.1>')
postTitle = ''
subreddit = testBot.subreddit('AskReddit')
commentList = []
for post in subreddit.hot(limit=1):
    postTitle = post.title
    currentComment = 0
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue
        if len(comment.body) > 20:
            commentList.append(comment.body)
            currentComment += 1

print(commentList[0])

textToSpeech = gTTS(text=commentList[0], lang='en')
textToSpeech.save('test.mp3')
