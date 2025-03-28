from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
import pandas as pd
import re
import nltk
from deep_translator import GoogleTranslator
from nltk.sentiment import SentimentIntensityAnalyzer
import os

# Download VADER lexicon
nltk.download('vader_lexicon')

app = Flask(__name__)

# API Configuration (IMPORTANT: Replace with your actual API key)
API_KEY = 'AIzaSyAc2Z3XBQs5-gGe4gYognTnTBTNHkmGZUA'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_video_id(youtube_url):
    """Extract video ID from YouTube URL"""
    pattern = r"v=([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, youtube_url)
    return match.group(1) if match else None

def fetch_all_comments(video_id):
    """Fetch ALL comments from YouTube video"""
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    comments = []
    next_page_token = None

    try:
        while True:
            # Use page token for pagination
            request_params = {
                'part': 'snippet',
                'videoId': video_id,
                'maxResults': 100,  # Max allowed by API per request
                'textFormat': 'plainText'
            }
            
            # Add page token for subsequent requests
            if next_page_token:
                request_params['pageToken'] = next_page_token

            response = youtube.commentThreads().list(**request_params).execute()
            
            # Extract comments
            for item in response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            
            # Check for next page token
            next_page_token = response.get('nextPageToken')
            
            # Break if no more pages
            if not next_page_token:
                break
    
    except Exception as e:
        print(f"Error fetching comments: {e}")
    
    return comments

def translate_comments(comments):
    """Translate comments to English"""
    converted_comments = []
    for comment in comments:
        try:
            translated_text = GoogleTranslator(source='auto', target='en').translate(comment)
            converted_comments.append(translated_text)
        except Exception as e:
            print(f"Translation error: {e}")
    return converted_comments

def analyze_sentiments(converted_comments):
    """Analyze sentiments of translated comments"""
    sia = SentimentIntensityAnalyzer()
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    detailed_sentiments = []
    
    for comment in converted_comments:
        if comment:
            sentiment = sia.polarity_scores(comment)
            sentiment_detail = {
                'text': comment,
                'sentiment': ('Positive' if sentiment['compound'] > 0.05 
                              else 'Negative' if sentiment['compound'] < -0.05 
                              else 'Neutral')
            }
            detailed_sentiments.append(sentiment_detail)
            
            if sentiment['compound'] > 0.05:
                sentiment_counts["Positive"] += 1
            elif sentiment['compound'] < -0.05:
                sentiment_counts["Negative"] += 1
            else:
                sentiment_counts["Neutral"] += 1
    
    return sentiment_counts, detailed_sentiments

def generate_conclusion(results):
    """Generate a conclusion based on sentiment analysis"""
    total_comments = sum(results['sentiments'].values())
    positive_percent = (results['sentiments']['Positive'] / total_comments) * 100
    negative_percent = (results['sentiments']['Negative'] / total_comments) * 100
    
    if positive_percent > 70:
        return "Wonderful! The video has received overwhelmingly positive feedback. The community seems highly engaged and supportive!"
    elif positive_percent > 50:
        return "Great insights! The video has received mostly positive comments, indicating a successful and well-received content."
    elif positive_percent > 30:
        return "Interesting mix of sentiments. While not entirely positive, the video has sparked diverse reactions and discussions."
    elif negative_percent > 50:
        return "There might be room for improvement. The comments suggest some critical views about the video content."
    else:
        return "Neutral reception. The video seems to have evoked a balanced range of responses from viewers."

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route to handle YouTube URL input and sentiment analysis"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_video():
    """Route to perform sentiment analysis"""
    youtube_url = request.form.get('youtube_url')
    
    # Validate URL
    video_id = get_video_id(youtube_url)
    if not video_id:
        return jsonify({'error': "Invalid YouTube URL. Please enter a valid video URL."})
    
    try:
        # Fetch and analyze comments
        comments = fetch_all_comments(video_id)
        if not comments:
            return jsonify({'error': "No comments found for this video."})
        
        translated_comments = translate_comments(comments)
        sentiment_counts, detailed_sentiments = analyze_sentiments(translated_comments)
        
        results = {
            'total_comments': len(comments),
            'translated_comments': len(translated_comments),
            'sentiments': sentiment_counts,
            'conclusion': generate_conclusion({
                'sentiments': sentiment_counts
            }),
            'sample_comments': detailed_sentiments[:10]  # First 10 comments for display
        }
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the Render-assigned port
    app.run(debug=True, host='0.0.0.0', port=port)
