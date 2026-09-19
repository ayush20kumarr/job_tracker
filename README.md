# Job Application Tracker

A simple, no-login web app to track job applications — company, position, status, dates, and notes. Built with Flask and SQLite.

## Features

- Add, edit, and delete job applications
- Track status: Applied, Interviewing, Offer, Rejected, Withdrawn
- Filter applications by status
- Follow-up date tracking with a "due" indicator
- Dashboard stats (total applications + count per status)
- No authentication — single-user, local-first tool

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** Jinja2 templates, vanilla CSS
- **Production server:** Gunicorn
- **Containerization:** Docker

## Project Structure

```
job_tracker/
├── app.py                 # Flask app, routes, and models
├── requirements.txt       # Python dependencies
├── Dockerfile
├── .dockerignore
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   └── form.html
└── static/
    └── style.css
```

## Running Locally (without Docker)

**1. Clone the repo**
```bash
git clone git@github.com:ayush20kumarr/job_tracker.git
cd job_tracker
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate.bat     # Windows (cmd)
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python app.py
```

Visit `http://localhost:5001` in your browser. A `jobs.db` SQLite file is created automatically on first run.

## Running with Docker

**1. Build the image**
```bash
docker build -t job-tracker .
```

**2. Run the container**
```bash
docker run -p 5001:5001 job-tracker
```

Visit `http://localhost:5001`.

> **Note:** Data stored in `jobs.db` currently lives inside the container's filesystem and will be lost when the container is removed. Persistent storage via Docker volumes is planned — see Roadmap below.

## Roadmap

- [ ] Persist `jobs.db` using a Docker volume
- [ ] Add Docker Compose for simplified local setup
- [ ] Explore multi-container networking

## License

Personal project — no license specified.
