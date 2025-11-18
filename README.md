# Web Scraper + Alert Engine

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/yourusername/yourrepo)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Goal
Monitor specific data (e.g., weather changes) and send notifications when conditions are met.

---

## Tech Stack
- **Requests** – for HTTP requests  
- **Playwright** – handling JS-heavy pages  
- **BeautifulSoup4** – parsing HTML  
- **SQLite** – lightweight database  
- **Schedule** – for automated scraping intervals  
- **Email API** – sending notifications  

---

## Core Challenges
- Build modular scraping pipelines  
- Handle JS-heavy pages (Playwright async)  
- Add deduplication + alert logic  

---

### Stretch Goals
- Add a small dashboard with Flask or Streamlit  
- Dockerize it and deploy to Render/Heroku  

---

## Demo
![Demo GIF](https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif)

---

## Usage
```bash
# Clone the repo
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

# Install dependencies
python3 -m pip install -r requirements.txt

# Run the scraper
python3 main.py
