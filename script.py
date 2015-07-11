#!python3
__author__ = 'iPlain'

import sys
import time
import praw
import OAuth2Util


r = praw.Reddit('Script:postScraperAndCssEditor:v1.0 (by /u/iPlain')
r.set_oauth_app_info(client_id='sTLbAOLV4XE5-Q', client_secret='JIbIazTjD_L5fmFcwAT0y1tGk_0',
                     redirect_uri='http://127.0.0.1:65010/' 'authorize_callback')
o = OAuth2Util.OAuth2Util(r)
o.refresh()

colors = {
    '!AMEXblue': '.author[href$="/{0}"]:before {{ content: ""; background-position: 0px 0px; width: 32px;height: 20px; margin-top: 0px; }}',
    '!AMEXgreen': '.author[href$="/{0}"]:before {{ content: ""; background-position: 0px -20px; width: 32px;height: 20px; margin-top: 0px; }}',
    '!AMEXgold': '.author[href$="/{0}"]:before {{ content: ""; background-position: 0px -40px; width: 32px;height: 20px; margin-top: 0px; }}',
    '!AMEXred': '.author[href$="/{0}"]:before {{ content: ""; background-position: 0px -60px; width: 32px;height: 20px; margin-top: 0px; }}',
    '!AMEXplatinum': '.author[href$="/{0}"]:before {{ content: ""; background-position: 0px -80px; width: 32px;height: 20px; margin-top: 0px; }}',
    '!AMEXcenturion': '.author[href$="/{0}"]:before {{ content: ""; background-position: 0px -100px; width: 32px;height: 20px; margin-top: 0px; }}'}

css_block_start = '/*AMEX_START*/' #Starting comment in CSS to define area for !AMEX CSS, note that any CSS within the start and end comments will be deleted.
css_block_end = '/*AMEX_END*/' #Defines the end of the CSS block for above
sleep_time = 60 * 10 #Amount of time the bot should wait until running again, in seconds
uptime = 24 * 60 * 60 #How long the bot should update from a single post, in seconds
subid = 'iPlain' #SubReddit to scrape from
flair_string = 'test' #The flair that defines a thread to scrape from

subreddit = r.get_subreddit(subid)


def loopcomments(thread):
    submission = r.get_submission(submission_id=thread)
    css_toadd = ''
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    for comment in flat_comments:
        if '!AMEX' in comment.body and 'imgur.com' in comment.body:
            username = comment.author.name
            for color in colors:
                if comment.body.find(color) != -1:
                    css_toadd += '\n' + colors[color].format(username)
    return css_toadd


def editcss(css_toadd):
    css = subreddit.get_stylesheet()['stylesheet']
    if css.find(css_block_start) == -1 and css.find(css_block_end) == -1:
        css += '\n\n' + css_block_start + css_toadd + '\n' + css_block_end

    elif css.find(css_block_start) != -1 and css.find(css_block_end) != -1:
        css = css[:css.find(css_block_start) + 14] + css_toadd + '\n' + css[css.find(css_block_end):]
    else:
        print('''
        Incorrectly formatted CSS, please fix before restarting.
        This is caused by having either {0} or {1}, but not both'''.format(css_block_start, css_block_end))
        sys.exit()
    subreddit.set_stylesheet(css)
    print("Edited CSS")


def getthread():
    posts = subreddit.get_new()
    for post in posts:
        if time.time() - post.created_utc < uptime and post.link_flair_text == flair_string:
            return post.id
    print("No valid post right now")
    return None


while True:
    o.refresh()
    thread = getthread()
    if thread:
        css_toadd = loopcomments(thread)
        editcss(css_toadd)
    time.sleep(sleep_time)
