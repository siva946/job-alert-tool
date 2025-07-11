import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

KEYWORDS = ['full stack', 'developer', 'fresher', 'entry level']

def matches_keywords(text):
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

# ----- Remotive Jobs -----
# def fetch_remotive_jobs():
#     job_list = []
#     print("🔍 Fetching from Remotive...")
#     url = 'https://remotive.io/api/remote-jobs?category=software-dev'
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code != 200:
#             print(f"❌ Remotive API error: Status {response.status_code}")
#             return []

#         try:
#             data = response.json()
#         except Exception as parse_err:
#             print("❌ JSON parsing failed. Raw response:")
#             print(response.text[:500])
#             return []

#         for job in data['jobs']:
#             pub_date = datetime.strptime(job['publication_date'], '%Y-%m-%dT%H:%M:%S')
#             if datetime.utcnow() - pub_date <= timedelta(hours=1):
#                 if matches_keywords(job['title']):
#                     job_list.append({
#                         'title': job['title'],
#                         'company': job['company_name'],
#                         'link': job['url'],
#                         'description': job['description'][:200] + "...",
#                         'linkedin_msg': f"Hi [Recruiter], I found the {job['title']} role at {job['company_name']} on Remotive. I'm a fresher with full stack experience (React, Node, etc.) and would love to connect!",
#                         'source': 'Remotive'
#                     })
#     except Exception as e:
#         print("❌ Remotive scraping failed:", e)
#     return job_list

# ----- Cuvette Tech -----
def fetch_cuvette_jobs():
    job_list = []
    print("🔍 Fetching from Cuvette Tech...")
    try:
        response = requests.get('https://www.cuvette.tech/internships', timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        job_cards = soup.find_all('div', class_='MuiBox-root')

        for card in job_cards:
            title = card.get_text()
            if matches_keywords(title):
                job_list.append({
                    'title': title[:40],
                    'company': "Cuvette Tech",
                    'link': 'https://www.cuvette.tech/internships',
                    'description': 'Listing from Cuvette Tech (visit to apply)',
                    'linkedin_msg': f"Hi [Recruiter], I came across an opportunity on Cuvette. As a fresher full stack developer, I’d love to be considered!",
                    'source': 'Cuvette'
                })
    except Exception as e:
        print("❌ Cuvette scraping failed:", e)
    return job_list

# ----- Unstop -----
def fetch_unstop_jobs():
    job_list = []
    print("🔍 Fetching from Unstop...")
    try:
        url = 'https://unstop.com/jobs'
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.select('.listing-event-card')

        for card in cards:
            title = card.get_text()
            link_tag = card.find('a', href=True)
            if matches_keywords(title) and link_tag:
                job_list.append({
                    'title': title[:60],
                    'company': "Unstop",
                    'link': 'https://unstop.com' + link_tag['href'],
                    'description': 'Listing from Unstop platform',
                    'linkedin_msg': f"Hi [Recruiter], I came across this opportunity via Unstop. I'm an entry-level developer eager to apply my skills. Would love to connect!",
                    'source': 'Unstop'
                })
    except Exception as e:
        print("❌ Unstop scraping failed:", e)
    return job_list

# ----- Indeed -----
def fetch_indeed_jobs():
    job_list = []
    print("🔍 Fetching from Indeed...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        search_url = "https://www.indeed.co.in/jobs?q=full+stack+developer+fresher&l=&fromage=1&sort=date"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        cards = soup.find_all('a', attrs={'data-jk': True})[:10]
        for card in cards:
            title = card.text.strip()
            link = "https://www.indeed.co.in" + card['href']
            if matches_keywords(title):
                job_list.append({
                    'title': title[:60],
                    'company': 'Unknown',
                    'link': link,
                    'description': "Listed on Indeed - posted within 24hrs.",
                    'linkedin_msg': f"Hi [Recruiter], I found the {title} opening on Indeed. I'm a fresher full stack dev ready to contribute and learn. Would love to connect!",
                    'source': 'Indeed'
                })
    except Exception as e:
        print("❌ Indeed scraping failed:", e)
    return job_list

# ----- Email Sender -----
def send_email(job_list):
    if not job_list:
        print("No new jobs found in the last hour.")
        return

    html = "<h2>🚀 Jobs Found in the Last Hour</h2><ul>"
    for job in job_list:
        html += f"<li><strong>{job['title']} – {job['company']}</strong><br>"
        html += f"<a href='{job['link']}'>Apply Here</a><br>"
        html += f"{job['description']}<br>"
        html += f"<strong>LinkedIn Msg:</strong> {job['linkedin_msg']}<br>"
        html += f"<em>Source: {job['source']}</em><br><br></li>"
    html += "</ul>"

    msg = MIMEText(html, 'html')
    msg['Subject'] = "🧾 Hourly Full Stack Fresher Jobs"
    msg['From'] = YOUR_EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(YOUR_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Email failed:", e)

# ----- Main Job -----
def job_run():
    print(f"⏰ Running job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    jobs = []
    # jobs += fetch_remotive_jobs()
    jobs += fetch_cuvette_jobs()
    jobs += fetch_unstop_jobs()
    jobs += fetch_indeed_jobs()
    send_email(jobs)

# ----- Scheduler -----
schedule.every().hour.at(":00").do(job_run)
#schedule.every().day.at("22:25").do(job_run)

print("📅 Hourly Job Alert Scheduler Running...")
while True:
    schedule.run_pending()
    time.sleep(60)
