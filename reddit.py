import praw
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RedditOperations:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )

    def create_text_post(self, subreddit_name, title, content):
        subreddit = self.reddit.subreddit(subreddit_name)
        submission = subreddit.submit(title=title, selftext=content)
        return submission.id

    def create_image_post(self, subreddit_name, title, image_path):
        subreddit = self.reddit.subreddit(subreddit_name)
        submission = subreddit.submit_image(title=title, image_path=image_path)
        return submission.id

    def create_video_post(self, subreddit_name, title, video_path):
        subreddit = self.reddit.subreddit(subreddit_name)
        submission = subreddit.submit_video(title=title, video_path=video_path)
        return submission.id

    def read_post(self, post_id):
        submission = self.reddit.submission(id=post_id)
        return {
            "title": submission.title,
            "content": submission.selftext,
            "comments": [comment.body for comment in submission.comments],
        }

    def update_post(self, post_id, new_content):
        submission = self.reddit.submission(id=post_id)
        submission.edit(new_content)

    def delete_post(self, post_id):
        submission = self.reddit.submission(id=post_id)
        submission.delete()
