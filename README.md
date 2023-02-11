# Reddit Video Making Bot

This is a reddit bot that will scrape the reddit website on a given subreddit for making quick short like videos, however for any length. It works by connecting to the Reddit API wrapper with a bot account and then uses Playwright to open a headless browser that looks at each comment received. 

## Features

- Select a subreddit to search
- Screenshots the title and comments
- Select a sort by method (hot, new, top, etc.)
- Change the length of the video made (deafault is 45 seconds)
- Connect a reddit account
- Make any number of voiced videos automatically 

## FAQ

#### What was the purpose of this app?

I created this application in order to create short style video that can be uploaded to a website like Youtube to generate revenue and views on a channel. I made it publically available for anyone that wants to use it.  



## Getting Started  
When the application is opened you will see this GUI:

![Main GUI Image](https://github.com/Sendecki-Krzysztof/Reddit_Bot/blob/master/assets/MainGUI_Reddit.PNG)

Create a reddit app using this link: https://ssl.reddit.com/prefs/apps/

Once the bot is created then you can click on the butto titled "Create bot json" in the GUI. This will bring up the following page:

![Create Bot GUI Image](https://github.com/Sendecki-Krzysztof/Reddit_Bot/blob/master/assets/AddBotJsonGUI_Reddit.PNG)

Enter the data in the corresponding locations and hit "Create". doing this will bring you back to the main screen where the Bot status will now be green.

You can also, optionally,  added a reddit account using the "Create account json" button this will bring up the following page:

![Create Account GUI Image](https://github.com/Sendecki-Krzysztof/Reddit_Bot/blob/master/assets/AddAccountJsonGUI_Reddit.PNG)

From there enter the desired vidoe characteristic and press the "Create Video" button when done.

Here is a short sample output: (Can also be found in the assests folder)

![Sample Video](https://github.com/Sendecki-Krzysztof/Reddit_Bot/blob/master/assets/QuickSampleVideo.mp4)

## Authors

- [@Krzysztof Sendecki](https://github.com/Sendecki-Krzysztof)
