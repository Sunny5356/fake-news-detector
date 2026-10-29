"""
Academic Content for Chapter 4: Proposed Methodology
Covers 4.1 System Architecture to 4.10 ER Model
"""

CHAPTER_4_CONTENT = {
    "title": "CHAPTER FOUR: PROPOSED METHODOLOGY",
    "system_architecture": {
        "heading": "4.1 SYSTEM ARCHITECTURE",
        "paragraphs": [
            "The proposed Fake News Detection and Credibility Assessment Engine is architected upon a modular, decoupled, "
            "three-tier enterprise software architecture comprising:",
            "1. Presentation Tier (Client Single-Page Application): Engineered in React 18 with Tailwind CSS, this layer manages user "
            "interactions, local component state orchestration, real-time input validation, asynchronous network requests to the API backend, "
            "and reactive rendering of the Antigravity glassmorphic dashboard.",
            "2. Application & API Services Tier (FastAPI Microservice): Engineered in Python utilizing the asynchronous ASGI FastAPI framework, "
            "this middle tier coordinates request validation via Pydantic schemas, manages in-memory machine learning artifact caching via "
            "lifespan context managers, executes heuristic sentiment evaluation, and dispatches vectorized payloads to the classifier.",
            "3. Machine Learning Inference Engine Tier (Scikit-Learn Pipeline): The computational data layer consists of serialized "
            "joblib artifacts encapsulating the trained 50,000-dimensional TF-IDF vectorizer and the regularized Passive-Aggressive Classifier.",
            "The lifecycle of a verification request proceeds through the following sequential stages:",
            "• Stage 1 (Client Ingestion & Validation): The user pastes an unverified news article or headline into the multi-line textarea of the "
            "React client. The client validates that the input string satisfies the minimum semantic length constraint (length >= 15 characters). "
            "Upon triggering 'Analyze Credibility', the interface toggles an animated loading state and issues an asynchronous HTTP POST request "
            "with a JSON payload to `http://localhost:8000/predict`.",
            "• Stage 2 (API Gateway & Ingestion): The FastAPI gateway intercepts the HTTP request, enforces CORS policies, and validates the "
            "incoming payload against the `PredictRequest` Pydantic model. If validation passes, the raw text is dispatched concurrently to "
            "the text cleaning pipeline and the heuristic sentiment analyzer.",
            "• Stage 3 (NLP Normalization & TF-IDF Vectorization): The text preprocessing function normalizes the input: converting to lowercase, "
            "stripping URLs, scrubbing HTML tags, eliminating punctuation, removing numeric tokens, and filtering standard English stopwords. "
            "The sanitized string is transformed into a sparse term-frequency inverse-document-frequency vector using the pre-loaded vectorizer.",
            "• Stage 4 (Passive-Aggressive Inference & Margin Calibration): The vector is submitted to the Passive-Aggressive Classifier. The model "
            "calculates the dot product with its trained weight vector, generating both the predicted class ('REAL' vs 'FAKE') and the signed "
            "geometric distance to the separating hyperplane. The decision margin is passed into the sigmoid calibration function, yielding a "
            "normalized confidence percentage.",
            "• Stage 5 (Heuristic Sentiment & Risk Extraction): Concurrently, the heuristic module evaluates emotional intensity, sensationalism buzzword "
            "density, typographic all-caps ratios, and punctuation anomalies, classifying the content into 'Low', 'Moderate', or 'High' risk tiers.",
            "• Stage 6 (JSON Serialization & Reactive Dashboard Render): The API constructs a structured `PredictResponse` JSON payload and transmits "
            "it back to the client. The React dashboard animates into view, rendering the Verdict hero badge, SVG confidence gauge, progress meter, "
            "diagnostic metric cards, and flagged linguistic trigger tags."
        ],
        "diagram": (
            "+-----------------------------------------------------------------------------------------+\n"
            "|                          TIER 1: PRESENTATION TIER (REACT 18)                           |\n"
            "|  +-----------------------------------------------------------------------------------+  |\n"
            "|  | [User Article Textarea]  -->  [Local Validation]  -->  [Async Fetch HTTP POST]     |  |\n"
            "|  | [Verdict Banner] <-- [Circular SVG Gauge] <-- [Heuristic Cards] <-- [Keyword Tags] |  |\n"
            "|  +-----------------------------------------------------------------------------------+  |\n"
            "+--------------------------------------------+--------------------------------------------+\n"
            "                                             | (HTTP POST /predict - JSON Payload)\n"
            "                                             v\n"
            "+-----------------------------------------------------------------------------------------+\n"
            "|                        TIER 2: API SERVICES TIER (FASTAPI / ASGI)                       |\n"
            "|  +-----------------------+     +------------------------+     +----------------------+  |\n"
            "|  |  CORS Middleware      |     | Pydantic Schema Check  |     | Application Lifespan |  |\n"
            "|  |  (Allowed Origins)    | --> | (PredictRequest Model) | --> | (Cached Models in RAM)|  |\n"
            "|  +-----------------------+     +------------------------+     +----------------------+  |\n"
            "|                                            |                                            |\n"
            "|                   +------------------------+------------------------+                   |\n"
            "|                   |                                                 |                   |\n"
            "|                   v                                                 v                   |\n"
            "|  +---------------------------------+               +---------------------------------+  |\n"
            "|  |     NLP PREPROCESSING PIPELINE  |               |  HEURISTIC SENTIMENT ANALYZER   |  |\n"
            "|  |  - Lowercase Conversion         |               |  - Sensationalism Score (0-100) |  |\n"
            "|  |  - Regex URL & HTML Stripping   |               |  - Emotional Charge (0-100)     |  |\n"
            "|  |  - Punctuation & Digit Removal  |               |  - All-Caps Density Analysis    |  |\n"
            "|  |  - Stopword Filtering (>2 chars)|               |  - Punctuation Spike Detector   |  |\n"
            "|  +---------------------------------+               |  - Clickbait Lexicon Matcher    |  |\n"
            "|                   |                                +---------------------------------+  |\n"
            "+-------------------|-------------------------------------------------|-------------------+\n"
            "                    |                                                 |\n"
            "                    v                                                 |\n"
            "+---------------------------------------------------------------------|-------------------+\n"
            "|                    TIER 3: MACHINE LEARNING ENGINE TIER (SCIKIT-LEARN)                  |\n"
            "|  +-----------------------------------+     +------------------------v----------------+  |\n"
            "|  | TF-IDF VECTORIZER (50,000 N-Grams)|     | PASSIVE-AGGRESSIVE CLASSIFIER (C=0.5)   |  |\n"
            "|  | Sparse Matrix Feature Extraction  | --> | Dot Product Decision Boundary Margin    |  |\n"
            "|  +-----------------------------------+     +-----------------------------------------+  |\n"
            "|                                                                 |                       |\n"
            "|                                            +--------------------+                       |\n"
            "|                                            v                                            |\n"
            "|                            +---------------------------------+                          |\n"
            "|                            | SIGMOID PROBABILITY CALIBRATION |                          |\n"
            "|                            | Conf % = 1 / (1 + exp(-|margin|))|                         |\n"
            "|                            +---------------------------------+                          |\n"
            "+--------------------------------------------+--------------------------------------------+\n"
            "                                             | (Assembled PredictResponse JSON)\n"
            "                                             v\n"
            "                            [Response Returned to Client UI]"
        ),
        "caption": "Figure 4.1: High-Level End-to-End System Architecture of the Credibility Assessment Engine"
    },
    "physical_design": {
        "heading": "4.2 PHYSICAL DESIGN",
        "paragraphs": [
            "The physical network and infrastructure topology governs how system software components are hosted, networked, and executed across "
            "hardware nodes. The platform is designed to operate seamlessly across both local development environments and multi-container "
            "cloud production topologies.",
            "1. Client Node (Web Browser Tier):",
            "The client application executes entirely within modern desktop and mobile browsers supporting ECMAScript 6+ and HTML5. The React "
            "bundle is served statically (via Vite or standard Nginx reverse proxy on port 3000/5173). All user interface interactions, local state "
            "transitions, and DOM rendering occur client-side on the user's host CPU, eliminating UI rendering load on backend servers.",
            "2. Host Server Node (FastAPI Execution Environment):",
            "The backend application runs as an asynchronous Python ASGI service managed by the Uvicorn high-performance server listening on "
            "TCP port 8000. Uvicorn leverages uvloop (an ultra-fast asyncio event loop written in Cython) and httptools to maximize request "
            "throughput. The application process requires standard commodity hardware (minimum 2 CPU cores, 4 GB RAM) and does not require "
            "GPU accelerators.",
            "3. Storage Node (Model Artifact & Dataset Repository):",
            "Serialized model weights (`model.joblib`) and vocabulary matrices (`vectorizer.joblib`) reside on local solid-state storage. During "
            "application startup, these files are deserialized and loaded into RAM once, where they persist across the service lifespan.",
            "4. Network & Security Boundaries:",
            "Network communication between the client and host server occurs over standard HTTP/1.1 or HTTP/2 protocols utilizing JSON payloads. "
            "Cross-Origin Resource Sharing (CORS) middleware restricts access to authorized origin domains (`http://localhost:3000`, `http://127.0.0.1:3000`). "
            "All incoming strings are sanitized to prevent injection attacks and memory exhaustion."
        ],
        "diagram": (
            "+---------------------------------------------------------------------------------+\n"
            "|                               CLIENT PHYSICAL NODE                              |\n"
            "|  +---------------------------------------------------------------------------+  |\n"
            "|  | Hardware: User PC / Laptop / Mobile Device (Any OS: Win/macOS/Linux/Android) |  |\n"
            "|  | Software: Modern Web Browser (Brave, Chrome, Firefox, Safari, Edge)       |  |\n"
            "|  | Runtime:  V8 JavaScript Engine executing React 18 SPA                     |  |\n"
            "|  +---------------------------------------------------------------------------+  |\n"
            "+----------------------------------------+----------------------------------------+\n"
            "                                         | TCP/IP (HTTP/2 / HTTPS)\n"
            "                                         | Port 8000 (REST API / CORS Protected)\n"
            "                                         v\n"
            "+---------------------------------------------------------------------------------+\n"
            "|                            APPLICATION SERVER PHYSICAL NODE                     |\n"
            "|  +---------------------------------------------------------------------------+  |\n"
            "|  | Hardware: Commodity CPU Server / Localhost (e.g. Intel i5/i7/Ryzen, 8GB)  |  |\n"
            "|  | OS:       Windows 11 / Ubuntu Linux 22.04 LTS                             |  |\n"
            "|  | Process:  Uvicorn ASGI Server (uvloop event loop, Python 3.10+)           |  |\n"
            "|  | Memory:   Resident Model Cache: ~45 MB RAM (model + vectorizer)           |  |\n"
            "|  +---------------------------------------------------------------------------+  |\n"
            "                                         |\n"
            "                                         v Local High-Speed Bus (NVMe / SSD)\n"
            "+---------------------------------------------------------------------------------+\n"
            "|                            PERSISTENT STORAGE SUBSYSTEM                         |\n"
            "|  +--------------------------+  +--------------------------+  +---------------+  |\n"
            "|  | model.joblib (PAC Model) |  | vectorizer.joblib (TFIDF)|  | news.csv Data |  |\n"
            "|  | File Size: ~1.2 MB       |  | File Size: ~4.8 MB       |  | Labeled News  |  |\n"
            "|  +--------------------------+  +--------------------------+  +---------------+  |\n"
            "+---------------------------------------------------------------------------------+"
        ),
        "caption": "Figure 4.2: Physical Network and Deployment Topology"
    },
    "database_design": {
        "heading": "4.3 DATABASE DESIGN",
        "paragraphs": [
            "In high-throughput Natural Language Processing inference systems, traditional relational database transactions (e.g. disk-bound "
            "SQL row queries) introduce unacceptable latency penalties for real-time scoring. Consequently, this platform utilizes a hybrid "
            "storage architecture combining serialized high-speed in-memory data structures for real-time classification, flat-file tabular storage "
            "for training datasets, and an optional relational schema for verification auditing and telemetry logging.",
            "1. In-Memory Joblib Binary Serialization:",
            "The primary operational data store comprises two pre-compiled, optimized binary artifacts:",
            "• `vectorizer.joblib`: Serializes the Scikit-learn `TfidfVectorizer` instance containing the fitted vocabulary dictionary (mapping "
            "over 50,000 N-gram string tokens to integer column indices), document frequency IDF weight vectors, and tokenization configuration "
            "parameters. Serialized size: ~4.8 megabytes.",
            "• `model.joblib`: Serializes the trained `PassiveAggressiveClassifier` instance, consisting of the learned 50,000-dimensional coefficient "
            "weight array ($w \\in \\mathbb{R}^{50000}$), intercept scalar ($b \\in \\mathbb{R}$), and target class labels (['FAKE', 'REAL']). "
            "Serialized size: ~1.2 megabytes.",
            "2. Flat-File Training Dataset Architecture (`news.csv`):",
            "The training and benchmark dataset resides as a standardized comma-separated values (CSV) document structured under two mandatory "
            "columns:",
            "• `text` (Type: Text/VARCHAR, Constraints: Non-null, Length: 50 to 50,000 characters): Contains the full textual body of the news article, "
            "headline, or editorial passage.",
            "• `label` (Type: Categorical String, Constraints: Values in {'REAL', 'FAKE', '1', '0'}): Defines the ground-truth veracity target.",
            "3. Verification Auditing Schema (Relational Telemetry):",
            "To support enterprise accountability and performance monitoring, the system defines an audit logging schema capable of persisting "
            "to SQLite or PostgreSQL:",
            "• Table: `prediction_logs` | Primary Key: `id` (UUID), `input_text` (TEXT), `prediction` (VARCHAR(10)), `confidence_score` (FLOAT), "
            "`sensationalism_score` (FLOAT), `emotional_charge` (FLOAT), `all_caps_ratio` (FLOAT), `exclamation_count` (INTEGER), "
            "`risk_level` (VARCHAR(10)), `client_ip` (VARCHAR(45)), `latency_ms` (FLOAT), `timestamp` (DATETIME)."
        ]
    },
    "project_schedule": {
        "heading": "4.4 PROJECT SCHEDULE",
        "paragraphs": [
            "The engineering lifecycle for this minor project was structured across a 16-week timeline, following an Agile iterative development "
            "methodology divided into six distinct operational phases:",
            "• Phase 1: Problem Formulation, Domain Literature Survey & Dataset Acquisition (Weeks 1-3)",
            "Comprehensive investigation of state-of-the-art NLP literature; comparative benchmarking of fact-checking systems; acquisition, "
            "cleaning, and exploratory data analysis of labeled fake news corpora.",
            "• Phase 2: Algorithm Selection, Prototyping & Pipeline Engineering (Weeks 4-6)",
            "Design and implementation of text normalization pipelines; comparative evaluation of Naive Bayes, Logistic Regression, SVM, and "
            "Passive-Aggressive algorithms; tuning TF-IDF hyper-parameters (N-gram ranges, max features, document frequencies).",
            "• Phase 3: Model Calibration & Heuristic Sentiment Engine Construction (Weeks 7-9)",
            "Mathematical formulation of decision margin sigmoid calibration; development of the clickbait keyword lexicon and multi-dimensional "
            "sentiment scoring heuristics (sensationalism index, emotional charge, all-caps ratios); model serialization via joblib.",
            "• Phase 4: High-Performance FastAPI Backend Microservice Development (Weeks 10-12)",
            "Creation of asynchronous FastAPI application; configuration of lifespan startup handlers for in-memory artifact caching; "
            "implementation of Pydantic validation schemas, health check routes, and CORS middleware; API unit testing.",
            "• Phase 5: Antigravity React Client Interface Development (Weeks 13-14)",
            "Architecting the React 18 frontend; configuring Tailwind CSS cosmic dark-mode themes and glassmorphism styling; integrating Lucide icons; "
            "building the interactive article input card, SVG radial progress gauge, animated results dashboard, and error handling states.",
            "• Phase 6: System Integration, Performance Benchmarking & Dissertation Documentation (Weeks 15-16)",
            "End-to-end integration between React frontend and FastAPI backend; latency and throughput stress testing; final dissertation "
            "compilation, plagiarism screening, and presentation preparation."
        ]
    },
    "wbs": {
        "heading": "4.5 WORK BREAKDOWN STRUCTURE",
        "paragraphs": [
            "The Work Breakdown Structure (WBS) decomposes the project into hierarchical work packages to guarantee rigorous engineering quality:",
            "1.0 Research & Data Engineering Subsystem:",
            "  1.1 Literature Review & Algorithmic Benchmarking",
            "  1.2 Dataset Acquisition & Cleaning (`news.csv`)",
            "  1.3 Text Preprocessing Subsystem (Regex, Punctuation, Stopword Stripping)",
            "  1.4 TF-IDF Vectorization Engine (50,000 N-gram Vocabulary Mapping)",
            "2.0 Machine Learning Core Engine:",
            "  2.1 Passive-Aggressive Classifier Model Training & Hyperparameter Tuning",
            "  2.2 Train/Test Stratified Split & Evaluation (Confusion Matrix, F1-Score)",
            "  2.3 Sigmoid Decision Margin Probability Calibration",
            "  2.4 Binary Serialization Subsystem (`model.joblib`, `vectorizer.joblib`)",
            "3.0 Heuristic Linguistic Subsystem:",
            "  3.1 Clickbait & Sensationalism Lexicon Formulation",
            "  3.2 Emotional Outrage Intensity Scoring Algorithm",
            "  3.3 Typographic Anomaly & Capitalization Density Evaluator",
            "4.0 Backend API Microservice:",
            "  4.1 Asynchronous FastAPI Framework Architecture & Event Loop Management",
            "  4.2 Pydantic Data Contract & Schema Validation Implementation",
            "  4.3 Cross-Origin Resource Sharing (CORS) Security Enforcement",
            "  4.4 Sub-Millisecond Inference Pipeline Integration",
            "5.0 Frontend Client Application:",
            "  5.1 Antigravity Cosmic Dark-Mode UI Theme Engineering",
            "  5.2 Multi-Line Article Ingestion Component with Real-Time Counter",
            "  5.3 Dynamic SVG Radial Confidence Gauge & Metric Progress Bars",
            "  5.4 Responsive State Management (Idle, Loading, Success, Error)",
            "6.0 Quality Assurance & Deployment:",
            "  6.1 Automated Unit & Integration Testing",
            "  6.2 Latency Profiling & Memory Optimization",
            "  6.3 Project Documentation & Plagiarism Verification"
        ],
        "diagram": (
            "                                +-------------------------------------------+\n"
            "                                |   FAKE NEWS CREDIBILITY ASSESSMENT ENGINE |\n"
            "                                +---------------------+---------------------+\n"
            "                                                      |\n"
            "        +-------------------+-------------------------+-------------------------+-------------------+\n"
            "        |                   |                         |                         |                   |\n"
            "        v                   v                         v                         v                   v\n"
            " +---------------+   +---------------+         +---------------+         +---------------+   +---------------+\n"
            " | 1.0 DATA ENG  |   | 2.0 ML CORE   |         | 3.0 HEURISTICS|         | 4.0 BACKEND   |   | 5.0 FRONTEND  |\n"
            " +-------+-------+   +-------+-------+         +-------+-------+         +-------+-------+   +-------+-------+\n"
            "         |                   |                         |                         |                   |\n"
            " +-------+-------+   +-------+-------+         +-------+-------+         +-------+-------+   +-------+-------+\n"
            " | 1.1 Dataset   |   | 2.1 PAC Model |         | 3.1 Clickbait |         | 4.1 FastAPI   |   | 5.1 Dark Theme|\n"
            " | 1.2 Cleaning  |   | 2.2 Eval/Test |         | 3.2 Emotion   |         | 4.2 Pydantic  |   | 5.2 Input Area|\n"
            " | 1.3 Stopwords |   | 2.3 Sigmoid   |         | 3.3 All-Caps  |         | 4.3 CORS Middleware| 5.3 SVG Gauge |\n"
            " | 1.4 TF-IDF    |   | 2.4 Joblib    |         | 3.4 Triggers  |         | 4.4 Async Run |   | 5.4 State Mgmt|\n"
            " +---------------+   +---------------+         +---------------+         +---------------+   +---------------+"
        ),
        "caption": "Figure 4.3: Work Breakdown Structure (WBS) Hierarchical Decomposition"
    },
    "gantt_chart": {
        "heading": "4.6 GANTT CHART",
        "paragraphs": [
            "The Gantt chart illustrates the temporal scheduling, task concurrency, and deliverable milestones across the 16-week project execution "
            "cycle. Critical path activities included model hyperparameter tuning, FastAPI asynchronous endpoint engineering, and client-server "
            "integration."
        ],
        "diagram": (
            "+--------------------+-----------------------------------------------------------------------------------+\n"
            "| Task Activity Name | W01 | W02 | W03 | W04 | W05 | W06 | W07 | W08 | W09 | W10 | W11 | W12 | W13 | W14 | W15 | W16 |\n"
            "+--------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n"
            "| Literature Review  | [X]   [X]   [X]   .     .     .     .     .     .     .     .     .     .     .     .     .   |\n"
            "| Dataset Gathering  | .     [X]   [X]   [X]   .     .     .     .     .     .     .     .     .     .     .     .   |\n"
            "| Text Preprocessing | .     .     .     [X]   [X]   .     .     .     .     .     .     .     .     .     .     .   |\n"
            "| Model Training PAC | .     .     .     .     [X]   [X]   [X]   .     .     .     .     .     .     .     .     .   |\n"
            "| Model Evaluation   | .     .     .     .     .     .     [X]   [X]   .     .     .     .     .     .     .     .   |\n"
            "| Sentiment Analyzer | .     .     .     .     .     .     .     [X]   [X]   .     .     .     .     .     .     .   |\n"
            "| FastAPI Backend    | .     .     .     .     .     .     .     .     .     [X]   [X]   [X]   .     .     .     .   |\n"
            "| React Frontend UI  | .     .     .     .     .     .     .     .     .     .     .     [X]   [X]   [X]   .     .   |\n"
            "| System Integration | .     .     .     .     .     .     .     .     .     .     .     .     .     [X]   [X]   .   |\n"
            "| Testing & Report   | .     .     .     .     .     .     .     .     .     .     .     .     .     .     [X]   [X] |\n"
            "+--------------------+-----------------------------------------------------------------------------------+"
        ),
        "caption": "Figure 4.4: Project Lifecycle Gantt Chart"
    },
    "requirements": {
        "heading": "4.7 HARDWARE AND SOFTWARE REQUIREMENTS",
        "paragraphs": [
            "The system is deliberately engineered to maximize operational accessibility by maintaining minimal hardware requirements while "
            "leveraging modern, standards-compliant software dependencies.",
            "Hardware Requirements (Development & Production Host):",
            "• Processor: Intel Core i3/i5/i7 (8th Gen or newer) or AMD Ryzen 3/5/7; Apple Silicon M1/M2/M3. Minimum 2 physical cores @ 2.0 GHz.",
            "• System Memory (RAM): Minimum 4.0 GB RAM (Recommended: 8.0 GB or higher).",
            "• Storage: Minimum 2.0 GB free SSD storage for Python virtual environment, Node modules, and serialized joblib binaries.",
            "• Network Interface: Standard 10/100/1000 Mbps Ethernet or 802.11ac Wi-Fi for client-server communication.",
            "Software Requirements:",
            "• Operating System: Windows 10/11 (64-bit), Ubuntu Linux 20.04/22.04 LTS, or macOS 12+.",
            "• Programming Languages: Python 3.10.x / 3.11.x / 3.13.x; JavaScript ECMAScript 2022+ / JSX.",
            "• Core Machine Learning Libraries: Scikit-learn (>=1.3.0), Pandas (>=2.0.0), NumPy (>=1.24.0), Joblib (>=1.3.0).",
            "• Backend Framework: FastAPI (>=0.100.0), Uvicorn ASGI Server (>=0.23.0), Pydantic (>=2.0.0).",
            "• Frontend Framework: React 18.2+, Node.js (>=18.x) & npm/pnpm, Tailwind CSS (>=3.3.0), Lucide React (>=0.263.0).",
            "• Version Control & Development: Git, GitHub repository hosting, Microsoft Visual Studio Code."
        ]
    },
    "dfd": {
        "heading": "4.8 DATAFLOW DIAGRAMS",
        "paragraphs": [
            "Data Flow Diagrams (DFDs) provide structural graphical representations of information movement, process transformations, and "
            "data stores across the platform at multiple levels of abstraction.",
            "• Level 0 DFD (Context Diagram): Models the high-level boundary of the entire system as a single process interacting with external "
            "entities (the User).",
            "• Level 1 DFD: Deconstructs the system into six primary operational sub-processes: Text Submission, Data Sanitization, Feature Vectorization, "
            "Passive-Aggressive Classification, Heuristic Sentiment Analysis, and Dashboard Visualization.",
            "• Level 2 DFD: Details the internal algorithmic mechanics of the Machine Learning Classification and Decision Margin Calibration process."
        ],
        "diagram_l0": (
            "  +--------------+               Raw Article Text / Headline                +---------------------------------------+\n"
            "  |              | -------------------------------------------------------> |                                       |\n"
            "  |     USER     |                                                          |   0.0 FAKE NEWS CREDIBILITY ENGINE    |\n"
            "  |  (CONSUMER)  | <------------------------------------------------------- |                                       |\n"
            "  +--------------+        Verdict, Confidence Score, Sentiment Risk Factors +---------------------------------------+"
        ),
        "caption_l0": "Figure 4.5: Level 0 Context Data Flow Diagram",
        "diagram_l1": (
            "                                             [USER]\n"
            "                                               |\n"
            "                                               | Raw Article Text (JSON)\n"
            "                                               v\n"
            "                             +-----------------------------------+\n"
            "                             |  1.0 INGESTION & VALIDATION       |\n"
            "                             +-----------------+-----------------+\n"
            "                                               |\n"
            "                                               v Validated Text String\n"
            "                             +-----------------------------------+\n"
            "                             |  2.0 TEXT SANITIZATION PIPELINE   |\n"
            "                             |  (Lowercase, URL/HTML/Punct Strip)|\n"
            "                             +-----------------+-----------------+\n"
            "                                               |\n"
            "                       +-----------------------+-----------------------+\n"
            "                       | Cleaned Tokens                                | Raw Text\n"
            "                       v                                               v\n"
            "        +------------------------------+                +------------------------------+\n"
            "        | 3.0 TF-IDF VECTORIZATION     |                | 5.0 HEURISTIC SENTIMENT      |\n"
            "        | (50,000 Dimension Mapping)   |                | - Sensationalism Index       |\n"
            "        +--------------+---------------+                | - Emotional Charge           |\n"
            "                       | Sparse Vector                  | - All-Caps / Punct Spikes    |\n"
            "                       v                                +--------------+---------------+\n"
            "        +------------------------------+                               |\n"
            "        | 4.0 PAC CLASSIFICATION       |                               |\n"
            "        | - Hyperplane Distance Score  |                               |\n"
            "        | - Sigmoid Probability Calc   |                               |\n"
            "        +--------------+---------------+                               |\n"
            "                       | Prediction & Conf %                           |\n"
            "                       +-----------------------+-----------------------+\n"
            "                                               | Combined Verification Payload\n"
            "                                               v\n"
            "                             +-----------------------------------+\n"
            "                             |  6.0 JSON RESPONSE AGGREGATOR     |\n"
            "                             +-----------------+-----------------+\n"
            "                                               | JSON Response\n"
            "                                               v\n"
            "                                        [USER DASHBOARD]"
        ),
        "caption_l1": "Figure 4.6: Level 1 Detailed Processing Data Flow Diagram",
        "diagram_l2": (
            "                            [Sparse TF-IDF Vector: x]\n"
            "                                       |\n"
            "                                       v\n"
            "                     +-----------------------------------+\n"
            "                     | 4.1 HYPERPLANE PROJECTION         |\n"
            "                     |   Margin z = (w * x) + b          |\n"
            "                     +-----------------+-----------------+\n"
            "                                       |\n"
            "                       +---------------+---------------+\n"
            "                       | Signed Margin z               | Continuous Value z\n"
            "                       v                               v\n"
            "        +------------------------------+     +----------------------------------+\n"
            "        | 4.2 BINARY SIGN DISCRIMINATOR|     | 4.3 SIGMOID PROBABILITY MAPPING  |\n"
            "        |   If z >= 0.0 --> 'REAL'     |     |   Prob = 1 / (1 + exp(-|z|))     |\n"
            "        |   If z <  0.0 --> 'FAKE'     |     |   Scale: [52.0% to 99.4%]        |\n"
            "        +--------------+---------------+     +-----------------+----------------+\n"
            "                       | Class Label                           | Calibrated Confidence %\n"
            "                       +---------------+-----------------------+\n"
            "                                       |\n"
            "                                       v\n"
            "                           [To Output Aggregator 6.0]"
        ),
        "caption_l2": "Figure 4.7: Level 2 Mathematical Inference Pipeline DFD"
    },
    "data_dictionary": {
        "heading": "4.9 DATA DICTIONARY",
        "paragraphs": [
            "The data dictionary establishes formal semantic definitions, data types, lengths, constraints, and operational descriptions for all "
            "information elements utilized across the application programming interface and internal processing pipelines.",
            "Table 4.3 enumerates the complete system data dictionary."
        ]
    },
    "er_model": {
        "heading": "4.10 ER MODEL",
        "paragraphs": [
            "The Entity-Relationship (ER) model conceptualizes the structural associations between entities in the credibility assessment "
            "ecosystem, capturing user sessions, raw article submissions, prediction records, heuristic sentiment evaluations, and flagged keyword "
            "occurrences.",
            "Primary Entities & Attributes:",
            "1. USER_SESSION: `session_id` (PK), `ip_address`, `user_agent`, `created_at`.",
            "2. ARTICLE_SUBMISSION: `article_id` (PK), `session_id` (FK), `raw_text`, `char_count`, `submitted_at`.",
            "3. PREDICTION_RECORD: `prediction_id` (PK), `article_id` (FK), `verdict` ('REAL'/'FAKE'), `confidence_score`, `margin_distance`, `inference_latency_ms`.",
            "4. SENTIMENT_ANALYSIS: `sentiment_id` (PK), `prediction_id` (FK), `sensationalism_score`, `emotional_charge`, `all_caps_ratio`, `exclamation_count`, `risk_level` ('Low'/'Moderate'/'High').",
            "5. FLAGGED_KEYWORD: `keyword_id` (PK), `sentiment_id` (FK), `keyword_text`, `category` ('sensational'/'emotional').",
            "Cardinality Relationships: A USER_SESSION can submit 1 to Many ARTICLE_SUBMISSIONs (1:N). Each ARTICLE_SUBMISSION generates exactly "
            "one PREDICTION_RECORD (1:1). Each PREDICTION_RECORD produces exactly one SENTIMENT_ANALYSIS (1:1). Each SENTIMENT_ANALYSIS identifies "
            "0 to Many FLAGGED_KEYWORDs (1:N)."
        ],
        "diagram": (
            "+------------------+        1:N        +-----------------------+\n"
            "|   USER_SESSION   |-------------------|   ARTICLE_SUBMISSION  |\n"
            "|------------------|                   |-----------------------|\n"
            "| PK session_id    |                   | PK article_id         |\n"
            "|    ip_address    |                   | FK session_id         |\n"
            "|    user_agent    |                   |    raw_text           |\n"
            "|    created_at    |                   |    char_count         |\n"
            "+------------------+                   +-----------+-----------+\n"
            "                                                   |\n"
            "                                                   | 1:1\n"
            "                                                   v\n"
            "                                       +-----------------------+\n"
            "                                       |   PREDICTION_RECORD   |\n"
            "                                       |-----------------------|\n"
            "                                       | PK prediction_id      |\n"
            "                                       | FK article_id         |\n"
            "                                       |    verdict (REAL/FAKE)|\n"
            "                                       |    confidence_score   |\n"
            "                                       |    margin_distance    |\n"
            "                                       |    latency_ms         |\n"
            "                                       +-----------+-----------+\n"
            "                                                   |\n"
            "                                                   | 1:1\n"
            "                                                   v\n"
            "+------------------+        1:N        +-----------------------+\n"
            "|  FLAGGED_KEYWORD |-------------------|   SENTIMENT_ANALYSIS  |\n"
            "|------------------|                   |-----------------------|\n"
            "| PK keyword_id    |                   | PK sentiment_id       |\n"
            "| FK sentiment_id  |                   | FK prediction_id      |\n"
            "|    keyword_text  |                   |    sensational_score  |\n"
            "|    category      |                   |    emotional_charge   |\n"
            "+------------------+                   |    all_caps_ratio     |\n"
            "                                       |    exclamation_count  |\n"
            "                                       |    risk_level         |\n"
            "                                       +-----------------------+"
        ),
        "caption": "Figure 4.8: Entity-Relationship (ER) Conceptual Schema"
    }
}

print("[*] Chapter 4 content compiled.")
