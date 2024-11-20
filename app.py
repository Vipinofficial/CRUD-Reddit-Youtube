import os
import streamlit as st
from dotenv import load_dotenv
from youtube import YouTubeOperations
from reddit import RedditOperations

# Load environment variables
load_dotenv()

# Sidebar navigation
platform = st.sidebar.selectbox("Choose Platform", ["Home", "Reddit", "YouTube"])

# Home Page
if platform == "Home":
    st.title("Welcome to the App!")
    st.write("Select a platform (Reddit or YouTube) from the sidebar to perform CRUD operations.")

# Reddit Section
elif platform == "Reddit":
    st.title("Reddit CRUD Operations")
    reddit = None
    try:
        reddit = RedditOperations()
        st.success("Authenticated with Reddit successfully!")
    except Exception as e:
        st.error(f"Failed to authenticate with Reddit: {e}")

    if reddit:
        operation = st.radio("Select Reddit Operation", ["Create Post", "Read Post", "Update Post", "Delete Post"])

        if operation == "Create Post":
            subreddit_name = st.text_input("Subreddit")
            post_type = st.radio("Post Type", ["Text", "Image", "Video"])
            title = st.text_input("Post Title")
            if post_type == "Text":
                content = st.text_area("Content")
                if st.button("Create Text Post"):
                    try:
                        post_id = reddit.create_text_post(subreddit_name, title, content)
                        st.success(f"Post created successfully! ID: {post_id}")
                    except Exception as e:
                        st.error(f"Failed to create post: {e}")
            elif post_type == "Image":
                image_path = st.text_input("Image Path")
                if st.button("Create Image Post"):
                    try:
                        post_id = reddit.create_image_post(subreddit_name, title, image_path)
                        st.success(f"Image post created successfully! ID: {post_id}")
                    except Exception as e:
                        st.error(f"Failed to create image post: {e}")
            elif post_type == "Video":
                video_path = st.text_input("Video Path")
                if st.button("Create Video Post"):
                    try:
                        post_id = reddit.create_video_post(subreddit_name, title, video_path)
                        st.success(f"Video post created successfully! ID: {post_id}")
                    except Exception as e:
                        st.error(f"Failed to create video post: {e}")

# YouTube Section
elif platform == "YouTube":
    st.title("YouTube CRUD Operations")

    # Sidebar selectbox to choose the operation
    operation = st.sidebar.selectbox("Select YouTube Operation", ["Upload Video", "Read Video", "Update Video", "Delete Video","List Videos"])

    youtube = None
    try:
        youtube = YouTubeOperations()
        st.success("Authenticated with YouTube successfully!")
    except Exception as e:
        st.error(f"Failed to authenticate with YouTube: {e}")

    if youtube:
        if operation == "Upload Video":
            st.subheader("Upload Video")
            video_path = st.text_input("Video File Path")
            title = st.text_input("Title")
            description = st.text_area("Description")
            privacy_status = st.selectbox("Privacy Status", ["public", "private", "unlisted"])
            if st.button("Upload Video"):
                try:
                    response = youtube.create_video(title, description, privacy_status, video_path)
                    st.success(f"Video uploaded successfully! Video ID: {response['id']}")
                except Exception as e:
                    st.error(f"Failed to upload video: {e}")

        elif operation == "Read Video":
            st.subheader("Read Video Details")
            video_id = st.text_input("Video ID")
            if st.button("Get Video Details"):
                try:
                    video_details = youtube.read_video(video_id)
                    st.json(video_details)
                except Exception as e:
                    st.error(f"Failed to fetch video details: {e}")

        elif operation == "Update Video":
            st.subheader("Update Video Details")
            video_id = st.text_input("Video ID")
            title = st.text_input("New Title")
            description = st.text_area("New Description")
            if st.button("Update Video"):
                try:
                    response = youtube.update_video(video_id, title, description)
                    st.success(f"Video updated successfully! Video ID: {response['id']}")
                except Exception as e:
                    st.error(f"Failed to update video: {e}")

        elif operation == "Delete Video":
            st.subheader("Delete Video")
            video_id = st.text_input("Video ID")
            if st.button("Delete Video"):
                try:
                    youtube.delete_video(video_id)
                    st.success("Video deleted successfully!")
                except Exception as e:
                    st.error(f"Failed to delete video: {e}")
        # List user's recent videos to help choose one for deletion
        try:
            videos = yt.list_my_videos(max_results=5)
            video_options = {}
            
            if videos.get('items'):
                for item in videos['items']:
                    title = item['snippet']['title']
                    video_id = item['id']['videoId']
                    video_options[title] = video_id
                
                if video_options:
                    selected_title = st.selectbox("Choose a Video to Delete", options=list(video_options.keys()))
                    video_id = video_options[selected_title]
                    
                    # Show video details before deletion
                    st.warning(f"You are about to delete: {selected_title}")
                    st.markdown(f"Video ID: {video_id}")
                    
                    confirm = st.checkbox("I understand that this action cannot be undone")
                    if st.button("Delete Video") and confirm:
                        try:
                            yt.delete_video(video_id)
                            st.success("Video deleted successfully!")
                            # Add a rerun button to refresh the video list
                            if st.button("Refresh Video List"):
                                st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Failed to delete video: {e}")
                else:
                    st.warning("No videos found in your channel.")
            else:
                st.warning("No videos found in your channel.")
                
        except Exception as e:
            st.error(f"Failed to fetch videos: {e}")
