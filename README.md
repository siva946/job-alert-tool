
# 🧭 Job Alert Tool

A Python-based automation tool that scrapes multiple job listing websites (Unstop, Cuvette Tech, and Indeed) for recent software development opportunities—particularly targeting freshers, entry-level, and full stack developer roles—and sends curated listings via email every hour.

---

## 📑 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Supported Platforms](#supported-platforms)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Features

- Scrapes job listings from:
  - ✅ **Cuvette Tech**
  - ✅ **Unstop**
  - ✅ **Indeed**
- (Optional) Support for **Remotive API** (currently commented)
- Filters jobs using custom **keyword matching**
- Automatically sends an **HTML-formatted email** with job listings every hour
- Includes pre-filled **LinkedIn message templates** for each job
- Configurable using environment variables

---

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/siva946/job-alert-tool.git
   cd job-alert-tool
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**

   ```env
   YOUR_EMAIL=your_email@example.com
   APP_PASSWORD=your_email_app_password
   TO_EMAIL=recipient_email@example.com
   ```

4. **Run the script**

   ```bash
   python job_alert.py
   ```

---

## ⚙️ Configuration

The following environment variables are required:

| Variable       | Description                                  |
|----------------|----------------------------------------------|
| `YOUR_EMAIL`   | Your Gmail address (used to send emails)     |
| `APP_PASSWORD` | Gmail App Password (not your real password)  |
| `TO_EMAIL`     | Recipient's email address                    |

**Note:** Enable "Less secure app access" or use Gmail App Passwords.

---

## ▶️ Usage

Once running, the tool will:

- Fetch jobs from supported platforms every hour
- Filter listings based on the following keywords:
  - `full stack`, `developer`, `fresher`, `entry level`
- Send email alerts for matching jobs in a clean HTML format

---

## 🌐 Supported Platforms

- [Indeed India](https://www.indeed.co.in)
- [Cuvette Tech](https://www.cuvette.tech/internships)
- [Unstop](https://unstop.com/jobs)
- *(Remotive API support is available but currently commented out)*

---

## 🧪 Examples

Email body includes:

- ✅ Job title & company
- 🔗 Direct application link
- ✍️ Pre-written LinkedIn outreach message
- 🔍 Job source (Indeed, Unstop, etc.)

---

## 🧯 Troubleshooting

| Issue                              | Solution                                                              |
|-----------------------------------|-----------------------------------------------------------------------|
| No emails received                | Check SMTP settings and `.env` variables                              |
| Email login failure               | Make sure you're using a **Gmail App Password**                       |
| Websites not returning data       | Ensure the site structure hasn't changed; inspect using browser tools |
| Rate-limiting or blocks           | Add delays, rotate IPs, or use proxies                                |

---

## 👥 Contributing

Feel free to fork the repo and submit PRs to add:

- More job platforms (e.g. LinkedIn, AngelList)
- GUI/CLI interface
- Notification methods (Telegram, WhatsApp)
- Advanced keyword filtering

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
