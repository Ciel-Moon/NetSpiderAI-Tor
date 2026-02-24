# NetSpiderAI-Tor

Declaration：
👋 Hi, I'm the author
Hello! I'm an 8th grader from China, and this is my personal project — I'm working hard on the coding part 🚀
Since I'm still learning, the code might not be perfect, and updates may be a bit slow (school comes first 😅), but I'll do my best to maintain it.
If you spot any issues or have suggestions, feel free to reach out. Thanks so much for your understanding and support!
📧 Contact: Cedric-Shadow@outlook.com

Now,the main text follows below.

NetSpiderAI-Tor: The Next-Generation Anonymous Web Crawler Browser

NetSpiderAI-Tor is a revolutionary, enterprise-grade web crawler that combines the privacy architecture of the Tor Browser with advanced AI‑driven crawling capabilities. It provides a clean, browser-like graphical interface, robust anonymity features, and a full suite of tools for large‑scale data extraction.

---

🌟 Key Features

· Tor Network Integration
    Full onion routing with automatic IP rotation, bridge support, and identity renewal. Your real IP stays hidden.
· Dual Rendering Engines
    Choose between Playwright (faster) and Selenium (wider compatibility) to crawl JavaScript‑heavy sites.
· Intelligent Compliance
    Respects robots.txt and HTTP 403/401 errors by prompting the user – with an option to force‑crawl if desired.
· Automated Proxy Pool
    Continuously fetches, validates, and rotates free proxies. Falls back to a local pool when Tor is not used.
· Distributed Task Scheduling
    RabbitMQ‑based queue allows multiple crawler nodes to work together. Built‑in backpressure control.
· Resumable Downloads
    Large files (images, videos) are downloaded in chunks and can be resumed after interruption.
· Modern GUI
    Built with CustomTkinter – clean, responsive, and supports system‑theme switching (dark/light).
· Data Persistence
    SQLite/MySQL storage for crawled content, with JSON/CSV export. Deduplication and incremental updates.

---

🚀 Quick Start

Prerequisites

· Python 3.8+
· Tor service (optional, for anonymous mode)
· RabbitMQ server (optional, for distributed mode)

Installation

```bash
# Clone the repository
git clone https://github.com/yourname/NetSpiderAI-Tor.git
cd NetSpiderAI-Tor

# Install Python dependencies
pip install -r requirements.txt

# Install Tor (Ubuntu/Debian)
sudo apt-get install tor
sudo systemctl start tor

# Install RabbitMQ (Ubuntu/Debian)
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
```

Running the Application

```bash
python main.py
```

First-Time Setup

1. Go to Settings tab.
2. Configure Tor ports (default SOCKS 9050, Control 9051).
3. Choose the rendering engine (Playwright recommended).
4. Set download directory and database path.

---

📖 User Guide

Basic Crawling

1. Enter a URL in the address bar.
2. Select a privacy mode:
   · Normal – direct connection (no proxy)
   · Anonymous – uses the proxy pool
   · Tor – routes all traffic through the Tor network
3. Click Crawl.
4. Extracted text appears in the main panel; images and videos are automatically saved to downloads/.

Handling Dynamic Content

If the target site relies on JavaScript, enable the Dynamic Rendering checkbox before crawling. The engine will wait for the page to fully render.

Task Monitoring

Switch to the Task Monitor tab to see all running and completed tasks. You can pause, resume, or cancel individual jobs.

Data Export

In the Settings tab, click Export Data to save crawled content as JSON or CSV. You can also export by task ID.

---

🔧 Architecture Overview

```
NetSpiderAI-Tor/
│
├── main.py                 # Entry point
├── config/                 # Global configuration
├── core/                   # Core modules
│   ├── tor_manager.py      # Tor circuit management
│   ├── crawler_engine.py   # Playwright/Selenium engines
│   ├── proxy_pool.py       # Automatic proxy collector/validator
│   ├── downloader.py       # Resumable file downloader
│   ├── scheduler.py        # RabbitMQ task scheduler
│   └── robots_checker.py   # robots.txt parser
├── gui/                     # CustomTkinter interface
├── storage/                 # Database and file management
├── utils/                   # Helpers (User‑Agent, logger, etc.)
└── data/                    # Downloads, logs, database
```

Core Components

· TorManager – starts/stops Tor, renews identity, provides a SOCKS5 proxy session.
· DynamicCrawler – unified interface for Playwright/Selenium; randomises browser fingerprint.
· ProxyPool – fetches from public proxy lists, validates them, and serves reliable proxies.
· ResumableDownloader – splits large files into chunks, supports Range headers.
· DistributedScheduler – RabbitMQ producer/consumer with priority queues and worker coordination.
· Database – SQLite (default) with optional MySQL support; stores tasks, content, and media records.

---

⚙️ Configuration

All settings are managed through config/settings.py or the GUI. Key options:

Setting Description Default
TOR_SOCKS_PORT Tor SOCKS5 port 9050
TOR_CONTROL_PORT Tor control port 9051
RENDERING_ENGINE playwright / selenium / requests playwright
PROXY_TEST_URL URL used to validate proxies httpbin.org/ip
DOWNLOAD_DIR Where media files are saved ./data/downloads
DATABASE_URL SQLite path or MySQL connection string sqlite:///data/db/spider.db
RABBITMQ_HOST RabbitMQ server address localhost

---

🤝 Contributing

We welcome contributions of all kinds – bug reports, feature requests, documentation improvements, and code.

1. Fork the repository.
2. Create a feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a Pull Request.

Please ensure your code passes existing tests and, if adding new functionality, include appropriate tests.

---

📄 License

Distributed under the MIT License. See LICENSE for more information.

---

🙏 Acknowledgements

· Tor Project – for the onion routing technology.
· CustomTkinter – for the modern GUI toolkit.
· Playwright – for reliable browser automation.
· RabbitMQ – for the distributed messaging system.

---

NetSpiderAI-Tor is more than a crawler – it's a privacy‑first, enterprise‑ready data acquisition platform. Start using it today and experience the next generation of web intelligence.
