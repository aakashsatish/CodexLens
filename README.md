# CodexLens: Smart AI Code Review Assistant

## What is CodexLens?

CodexLens is an automated code review system I built to solve a real problem I faced during my software engineering projects. As a third-year student working on team projects, I noticed how much time we spent manually reviewing pull requests - it was tedious, error-prone, and took away from actual development time.

I wanted to create something that could automatically analyze code and provide intelligent feedback, so developers could quickly glance over PRs instead of doing deep manual reviews. This project was born from that frustration and my desire to learn modern web development technologies.

## The Problem I Wanted to Solve

- **Manual PR reviews are time-consuming** - Developers spend hours reviewing code that could be automated
- **Inconsistent feedback** - Different reviewers focus on different things, leading to inconsistent code quality
- **Human error** - Easy to miss security vulnerabilities, style issues, or best practices
- **Learning curve** - New developers often don't know what to look for in code reviews

## How CodexLens Works

CodexLens integrates directly with GitHub and automatically:

1. **Detects when a PR is created** via GitHub webhooks
2. **Analyzes the code** using static analysis tools (Ruff, Bandit)
3. **Generates intelligent feedback** with specific suggestions
4. **Posts comments directly to the PR** with actionable advice
5. **Stores findings in a database** for tracking and analytics

## Tech Stack I Learned

This project taught me a lot about modern web development:

- **FastAPI** - Building REST APIs with Python
- **Celery** - Background task processing and job queues
- **PostgreSQL** - Database design and management
- **Redis** - Caching and message brokering
- **GitHub Apps** - OAuth, webhooks, and API integration
- **Docker** - Containerization and deployment
- **Static Analysis** - Code quality tools and security scanning

## Current Features

**Automated PR Analysis** - Analyzes every PR automatically  
**Static Code Analysis** - Uses Ruff for Python linting and Bandit for security  
**Intelligent Comments** - Generates helpful, actionable feedback  
**GitHub Integration** - Posts comments directly to PRs  
**Database Storage** - Tracks all findings and analysis history  
**Real-time Processing** - Webhook-based instant analysis  

## Future Plans

I'm excited to expand this project! Here's what I want to add:

- **Multi-language Support** - JavaScript, TypeScript, Java, Go, etc.
- **Advanced AI Analysis** - Integration with GPT or similar APIs for detailed code explanations
- **Pattern Recognition** - Identify common code smells and architectural issues
- **Custom Rules Engine** - Allow teams to define their own coding standards
- **Dashboard** - Web interface to view analysis history and trends
- **Team Analytics** - Track code quality improvements over time

## Why I Built This

As a student, I wanted to:
- **Solve a real problem** that I and other developers face daily
- **Learn modern technologies** used in industry
- **Build something useful** that others can actually use
- **Understand system architecture** - APIs, databases, background jobs, etc.
- **Practice DevOps skills** - Docker, deployment, monitoring

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- GitHub App (for webhook integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CodexLens.git
   cd CodexLens
   ```

2. **Set up your environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure your GitHub App**
   - Create a GitHub App in your repository settings
   - Set the webhook URL to your ngrok tunnel
   - Configure the necessary permissions

4. **Set up the database**
   ```bash
   cd infra
   alembic upgrade head
   ```

5. **Start the services**
   ```bash
   # Terminal 1: Start Redis
   redis-server
   
   # Terminal 2: Start the API
   uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 3: Start the Celery worker
   celery -A apps.worker.celery_app worker --loglevel=info
   ```

6. **Expose your local server**
   ```bash
   ngrok http 8000
   ```

## Project Structure

```
CodexLens/
├── apps/
│   ├── api/                 # FastAPI application
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── models.py       # Database models
│   └── worker/             # Celery background tasks
├── infra/                  # Infrastructure files
│   ├── docker-compose.yml  # Local development setup
│   └── alembic/           # Database migrations
└── tests/                 # Test files
```

## Contributing

I'd love to see this project grow! If you're a student like me or just interested in automated code review, feel free to:

- **Report bugs** or suggest features
- **Submit pull requests** with improvements
- **Share your use cases** - I want to know how you'd use this
- **Help with documentation** or testing

## Learning Journey

This project has been an incredible learning experience. I went from knowing basic Python to understanding:

- **Asynchronous programming** with async/await
- **Microservices architecture** with separate API and worker services
- **Database design** and migration management
- **API integration** with third-party services
- **DevOps practices** like containerization and deployment
- **Security considerations** like webhook verification and OAuth

---
