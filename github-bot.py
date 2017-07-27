import os
import time
from slackclient import SlackClient
import github_scrapper

# starterbot's ID as an environment variable
BOT_ID ="Insert Bot ID"

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "github"

# instantiate Slack clients
slack_client = SlackClient('Insert Slack Client Token')

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        request=command.split(' ',1)[1]
        msg1,repos,followers,url,commits,langs,others,pred=github_scrapper.gitScrape(request)
        "Converting dictionary returned to string"
        
        if(msg1==1):
            y=", ".join([": ".join([key, str(val)]) for key, val in langs.items()])
            #response2="\nRepositories:"+str(repos)+"\nFollowers:"+str(followers)+"\nCommits:"+str(commits)+"\nTop Language Proficiency:"+y+"\nOther Technologies:"+', '.join(others)+"\nCommits Prediction(100th week):"+str(pred)  
            attachments=attachments=[
                {
                    "color": "#36a64f",
                    "author_name": request,
                    "text":" " ,
                    "fields": [
                        {
                            "title": "Repositories",
                            "value": str(repos),
                            "short": "false"
                        },
                        {
                            "title": "Followers",
                            "value": str(followers),
                            "short": "false"
                        },
                        {
                            "title": "Commits",
                            "value": str(commits),
                            "short": "false"
                        },
                        {
                            "title": "Top Technologies",
                            "value": y,
                            "short": "false"
                        },
                        {
                            "title": "Other Technologies",
                            "value": ', '.join(others),
                            "short": "false"
                        },
                        {
                            "title": "Commits Prediction(100th week)",
                            "value": str(pred),
                            "short": "false"
                        },],
                    "thumb_url": "http://example.com/path/to/thumb.png"
            
             }]
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=url,attachments=attachments, as_user=True)

        else:
             response=msg1
             attachments=attachments= [
                 {
                     "text": " ",
                     "fields": [
                         {
                             "title": "Error",
                             "value": response,
                             "short": "true"
                             }
                         ],
                     "color": "#F35A00"
                     }]
             slack_client.api_call("chat.postMessage", channel=channel,
                          attachments=attachments, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("GitBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
