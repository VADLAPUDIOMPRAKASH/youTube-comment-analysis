# YouTube Comments Sentiment Analyzer

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Key Management](#api-key-management)
- [How it Works](#how-it-works)
- [Features in Detail](#features-in-detail)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview
The **YouTube Comments Sentiment Analyzer** is a web application that retrieves comments from a YouTube video, translates them to English (if needed), and performs sentiment analysis to determine whether the comments are Positive, Negative, or Neutral. This tool provides insights into how viewers feel about the video and visualizes the sentiment distribution.

## Features
- Fetch YouTube video details and comments using the YouTube Data API.
- Translate comments to English using Google Translate.
- Analyze sentiments using VADER (Valence Aware Dictionary for Sentiment Reasoning).
- Dynamic visualization of sentiment distribution.
- Display a summary of results and sample comments.
- User-friendly interface with loading animations and error handling.

## Tech Stack
### Frontend:
- **HTML5**, **CSS3**, **JavaScript**
- AJAX for communicating with the backend


![image](https://github.com/user-attachments/assets/49c94d2b-a3fb-48bb-b356-2c100584d66c)


### Backend:
- **Python** (Flask Framework)
- **APIs:** YouTube Data API, Google Translate API
- **Libraries:**
  - `googleapiclient` for YouTube API interaction
  - `googletrans` for comment translation
  - `nltk` (VADER) for sentiment analysis

### Visualization:
- Dynamic bar chart visualization for sentiment distribution.

### Deployment:
- Flask for backend hosting
- Compatible with platforms like Heroku, AWS, or local development.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Access to the YouTube Data API (API key)
- Google Translate API library
- Basic knowledge of Flask and API integration

### Installation
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/vadlapudiomprakash/youtube-comments-analyzer.git
    cd youtube-comments-analyzer
    ```

2. **Set up a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate  # For Windows
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` File:**
    - In the root directory, create a file named `.env` and add your API key:
      ```
      YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
      ```

5. **Run the Application:**
    ```bash
    python app.py
    ```
    The application will be accessible at `http://127.0.0.1:5000/`.

---

## Usage
1. Open the application in your browser.
2. Enter a valid YouTube video URL into the input field.
3. Click on the **Analyze Comments** button.
4. Wait for the analysis to complete. The results will include:
   - Total comments fetched and translated.
   - Sentiment distribution.
   - Sample comments with sentiments.
   - A conclusion summarizing the sentiments.

---

## Project Structure
```plaintext
youtube-comments-analyzer/
├── app.py               # Flask backend
├── templates/
│   └── index.html       # Frontend HTML template
├── static/
│   ├── styles.css       # Custom CSS styles
│   └── script.js        # Frontend JavaScript
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .env                 # API key (not included in the repo)
```

---

## API Key Management
- **YouTube Data API Key:**
  - Obtain your API key from the [Google Cloud Console](https://console.cloud.google.com/).
  - Ensure the key has permissions for the YouTube Data API.
- **Google Translate API:**
  - Install `googletrans` for translation without needing an additional key:
    ```bash
    pip install googletrans==4.0.0-rc1
    ```

---

## How it Works
1. **Input Validation:**
   - The entered URL is validated to ensure it matches the YouTube video format.

2. **Fetching Comments:**
   - The backend uses the YouTube Data API to retrieve comments in batches.

3. **Translation:**
   - Non-English comments are detected and translated to English using Google Translate.

4. **Sentiment Analysis:**
   - VADER analyzes the comments and classifies them as Positive, Negative, or Neutral.

5. **Visualization:**
   - Sentiment results are visualized dynamically in the frontend.

---

## Features in Detail
- **Dynamic Visualization:**
  - Sentiment bars are color-coded (green for Positive, red for Negative, gray for Neutral).

- **Sample Comments:**
  - Randomly selected comments with their detected sentiment are displayed.

- **Error Handling:**
  - Handles invalid URLs, API errors, and unexpected failures with user-friendly messages.

---

## Future Enhancements
- Add support for larger datasets with comment pagination.
- Incorporate a progress bar for real-time feedback on analysis stages.
- Provide options to filter comments by sentiment.
- Allow export of results as a CSV or PDF file.
- Use machine learning models for enhanced sentiment accuracy.
- Integrate with a database for caching results of previously analyzed videos.

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Submit a pull request with a detailed description of your changes.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

