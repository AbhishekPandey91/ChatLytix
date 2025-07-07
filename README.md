# 📊 ChatLytix

**ChatLytix** is a real-time chat analytics platform that lets users upload their personal or group chat files (e.g., WhatsApp `.txt`) and instantly gain powerful insights through visualizations, statistics, and sentiment analysis.


---

## 🚀 Purpose

The goal of ChatLytix is to help users explore their chat behavior and patterns over time. Whether you're curious about your most active group member, emoji usage, or conversation mood swings — ChatLytix uncovers it all effortlessly.

---

## 🛠️ Built With

- **Frontend**:  
  - [Streamlit](https://streamlit.io/) – for fast interactive UI

- **Backend / Data Analysis**:
  - Python
  - pandas
  - matplotlib / seaborn
  - re / datetime (for parsing)
  - optional: `nltk`, `textblob`, or `vaderSentiment` for sentiment analysis

- **Deployment**:
  - Hosted on [Render](https://render.com)

---
 ## 🧪 How to Use
Export your WhatsApp chat as a .txt file (without media)

Open ChatLytix Live App

Upload the file and explore:

📈 Message activity over days/months

🧑‍🤝‍🧑 Most active participants

📸 Media, links, and emoji usage

☁️ Word clouds

😊 Sentiment analysis (if enabled)

 ## 🌟 Key Features
Upload & Analyze .txt chats (WhatsApp, Telegram, etc.)

Visualize trends, top contributors, and message spikes

Emoji & Word Cloud breakdowns

Sentiment Analysis (optional)

Fully browser-based — no installation required for users

## ⚙️ Prerequisites & Setup

To run locally:

```bash
# Clone the repository
git clone https://github.com/your-username/ChatLytix.git
cd ChatLytix

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate



# Install required packages
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
