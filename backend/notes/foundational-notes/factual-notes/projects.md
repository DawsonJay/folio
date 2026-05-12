# Projects - Factual Notes

**Purpose**: Single source of truth for all projects with tech stacks, timelines, outcomes, and deployment links. This will be used as the foundation for direct answer notes.

**Sources**: 
- `atomic-notes/projects/` (57 project files)
- `atomic-notes/resources/project-links-all.md`
- `linked-in-job-hunter/profile-documents/` (project files)
- `/home/james/Documents/portfolio-profile/records/` (chat records for project timelines)

---

## Jam Hot - Computer Vision Project (Abandoned)

### Basic Information
- **Name**: Jam Hot
- **Type**: Computer vision project (fruit recognition)
- **Status**: Abandoned (data quality issues)
- **Timeline**: Pre-October 2025 (before WhatNow)
- **Source**: `/home/james/Documents/portfolio-profile/records/whatnow/chat-record-2025-10-04-1620.md`

### Description
Computer vision project for fruit recognition that was abandoned due to dataset quality issues. Used Fruit-360 dataset which achieved 86% validation accuracy but 0% real-world accuracy due to controlled environment training data.

### Why Abandoned
- Dataset quality issues: Fruit-360 dataset trained in controlled environment
- Real-world accuracy: 86% validation accuracy → 0% real-world accuracy
- Pattern recognition: Part of learning journey about data quality in computer vision projects
- Led to insight: Need AI approaches that don't require large image datasets or generate their own training data

### Learning Impact
- Demonstrated importance of data quality validation
- Led to WhatNow project which generates its own training data through usage
- Part of learning journey: Jam Hot (failed) → Cirrus (cancelled) → WhatNow (successful)
- **Source**: `/home/james/Documents/portfolio-profile/records/whatnow/chat-record-2025-10-04-1620.md`

---

## WhatNow - AI Activity Recommendation System

### Basic Information
- **Name**: WhatNow
- **Type**: AI-powered activity recommendation system
- **Status**: Production-deployed, actively used
- **Timeline**: 
  - **Start**: October 4, 2025 (project ideation and specification)
  - **Development**: October 4-16, 2025 (intensive development period)
  - **Deployment**: October 15, 2025 (frontend deployed to Render, backend already deployed)
  - **Completion**: October 16, 2025 (polished, production-ready)
- **Source**: `atomic-notes/projects/whatnow-overview-and-motivation.md`, `/home/james/Documents/portfolio-profile/records/whatnow/`

### Description
AI-powered activity recommendation system that helps decide what to do when feeling stuck or unmotivated. Production-deployed application that provides real value. Built after learning from Jam Hot and Cirrus projects about data quality issues - designed to generate its own training data through usage rather than relying on external datasets.

### Technologies
- **Frontend**: React, TypeScript
- **Backend**: FastAPI, PostgreSQL
- **AI/ML**: Contextual bandits, reinforcement learning, two-layer learning architecture (Session AI and Base AI)
- **Deployment**: Render (migrated from Railway)
- **Source**: `atomic-notes/projects/whatnow-overview-and-motivation.md`, `atomic-notes/resources/project-links-all.md`

### Links
- **Live Application**: https://whatnow.jamesfolio.dev
- **Frontend Repository**: https://github.com/DawsonJay/whatnow-frontend
- **Backend Repository**: https://github.com/DawsonJay/whatnow-backend
- **Source**: `atomic-notes/resources/project-links-all.md`

### Key Features
- Context input using sliders (mood, energy level, social preference, available time, weather)
- Generates 50 personalized activity suggestions from database of 1,249 activities (originally 1,258, cleaned to 1,249)
- Semantic embeddings for activity matching
- Continuous learning that improves over time
- User can pick top 3 favorites and regenerate for more options
- Mobile-first responsive design (fits perfectly on iPhone SE without scrolling)
- **Source**: `atomic-notes/projects/whatnow-overview-and-motivation.md`, `/home/james/Documents/portfolio-profile/records/whatnow/`

### Outcomes
- Production-deployed system
- Actually used in daily life
- Demonstrates complete end-to-end machine learning system
- Shows reinforcement learning and contextual bandits implementation
- **Source**: `atomic-notes/projects/whatnow-overview-and-motivation.md`

### Iterations
- From manual metadata to AI embeddings
- From vanilla JavaScript to professional React architecture
- From Railway to Render for hosting (migrated due to pricing changes)
- From scikit-learn to custom lightweight implementations
- Database population: Generated 1,258 activities through AI generation, image extraction, and manual curation
- Design evolution: From functional prototype to polished professional design with centralized theme system
- **Source**: `atomic-notes/projects/whatnow-overview-and-motivation.md`, `/home/james/Documents/portfolio-profile/records/whatnow/`

---

## moh-ami - French Learning Translation Tool

### Basic Information
- **Name**: moh-ami (pronounced "moh-ah-mee", from "mot ami" meaning "word friend")
- **Type**: French learning translation tool with LLM integration
- **Status**: Production-deployed
- **Timeline**: 
  - **Start**: January 11, 2026 (built from scratch)
  - **Development**: January 11, 2026 (rapid full-stack development)
  - **Deployment**: January 11, 2026 (deployed to Railway same day)
  - **Completion**: January 11, 2026 (production-ready)
- **Source**: `atomic-notes/projects/moh-ami-overview-and-motivation.md`, `/home/james/Documents/portfolio-profile/records/moh-ami/`

### Description
French learning translation tool that provides detailed educational explanations for language learners, not just simple translations.

### Technologies
- **Frontend**: Next.js 14 (App Router), React 19, TypeScript, Redux Toolkit, Tailwind CSS
- **Backend**: GraphQL API (Apollo Server), PostgreSQL, Prisma ORM (Prisma 6.19.1)
- **AI/ML**: OpenAI GPT-4o-mini for LLM integration (originally GPT-3.5-turbo, upgraded)
- **Deployment**: Railway (via GitHub integration)
- **Development**: Built from scratch in single intensive session
- **Source**: `atomic-notes/projects/moh-ami-overview-and-motivation.md`, `atomic-notes/resources/project-links-all.md`, `/home/james/Documents/portfolio-profile/records/moh-ami/`

### Links
- **Live Application**: https://moh-ami.jamesfolio.dev
- **Source Code**: https://github.com/DawsonJay/moh-ami
- **Source**: `atomic-notes/resources/project-links-all.md`

### Key Features
- Word-by-word mappings
- Grammar rule explanations
- Cultural context notes
- Alternative translations with explanations
- Synchronized side-by-side text comparison
- Interactive chunk selection
- Hover highlighting
- Expandable explanation panels
- Structured LLM integration with JSON schema outputs
- Semantic chunking (50-150 characters)
- **Source**: `atomic-notes/projects/moh-ami-overview-and-motivation.md`

### Outcomes
- Production-deployed application
- Actually used for learning French
- Demonstrates end-to-end LLM integration
- Shows full-stack development with modern frameworks
- **Source**: `atomic-notes/projects/moh-ami-overview-and-motivation.md`

---

## Folio - RAG-Powered Portfolio Chatbot

### Basic Information
- **Name**: Folio
- **Type**: AI-powered RAG portfolio chatbot
- **Status**: MVP complete, ongoing improvements
- **Timeline**: 
  - **Start**: January 24, 2026
  - **MVP Completion**: February 2026 (MVP complete, ongoing improvements)
  - **Status**: MVP complete, work ongoing to make it better
- **Source**: `atomic-notes/projects/folio-overview-and-motivation.md`

### Description
AI-powered portfolio chatbot that uses Retrieval Augmented Generation (RAG) to answer questions about background, skills, and projects. Makes portfolio conversational and interactive.

### Technologies
- **Frontend**: React, TypeScript
- **Backend**: FastAPI
- **AI/ML**: 
  - FastAPI orchestration with OpenAI SDK (tiered embeddings, cosine similarity search over local vectors, GPT-4o-mini for replies)
  - OpenAI text-embedding-3-small (1536 dimensions) for embeddings
  - Local JSON embedding store with NumPy similarity calculations
  - OpenAI GPT-4o-mini for chat responses
- **Knowledge Base**: Atomic notes (200-500 token self-contained notes)
- **Source**: `atomic-notes/projects/folio-overview-and-motivation.md`, `atomic-notes/projects/folio-rag-system-architecture.md`

### Links
- **Status**: MVP complete, source code will be published (ongoing improvements)
- **Source**: `atomic-notes/resources/project-links-all.md`

### Key Features
- Natural language questions about background, skills, projects
- Retrieves relevant information from atomic notes knowledge base
- Generates personalized answers maintaining first-person voice
- Follow-up questions drill deeper
- Different employers get different information based on what they care about
- **Source**: `atomic-notes/projects/folio-overview-and-motivation.md`

### Outcomes
- Demonstrates modern RAG system architecture
- Shows semantic embeddings and vector similarity search
- Proves LLM prompt engineering
- Demonstrates test-driven development approach
- **Source**: `atomic-notes/projects/folio-overview-and-motivation.md`

### Development Approach
- Started with 20 notes (10 general background, 10 WhatNow deep-dive)
- Tested retrieval precision and answer quality
- Expanded incrementally (added 10 moh-ami notes)
- Validated multi-project behavior
- **Source**: `atomic-notes/projects/folio-overview-and-motivation.md`

---

## Atlantis - Lake Bed Mapping System

### Basic Information
- **Name**: Atlantis (formally known as "The Momo")
- **Type**: Lake bed mapping system (hardware/embedded systems)
- **Status**: Ongoing project (underwent major pivot)
- **Timeline**: 
  - **Start**: September 4, 2025 (components ordered, arriving August 31, 2025)
  - **Original Concept**: Underwater drone development (September-October 2025)
  - **Pivot Date**: October 29, 2025 (strategic pivot to surface boat + probe)
  - **Post-Pivot**: October 29 - December 20, 2025 (controller enclosure, electronics development)
  - **Latest Activity**: December 20, 2025
- **Source**: `atomic-notes/projects/atlantis-overview-and-pivot.md`, `/home/james/Documents/portfolio-profile/records/atlantis-project/`

### Description
Lake bed mapping system demonstrating advanced engineering for impossible-to-reach places. Underwent major strategic pivot from underwater drone to surface boat with towed probe mapping system.

### Technologies
- **Hardware**: Raspberry Pi 3B, Raspberry Pi Pico, ultrasonic sensors (8 sensors in hemispherical array), GPS positioning, winch system, LoRa long-range communication
- **Software**: Python (high-level AI), C++ (low-level hardware control)
- **Communication**: LoRa RF communication protocols
- **Source**: `atomic-notes/projects/atlantis-overview-and-pivot.md`

### Links
- **Source Code**: https://github.com/DawsonJay/atlantis-project
- **Source**: `atomic-notes/resources/project-links-all.md`

### Key Features
- Remote-controlled surface boat
- Towed weighted probe with 8 ultrasonic sensors
- GPS positioning
- Winch system to control probe depth
- LoRa communication for data transmission
- Creates highly accurate 3D maps of lake beds
- **Source**: `atomic-notes/projects/atlantis-overview-and-pivot.md`

### Pivot Details
- **Original Concept**: Underwater drone with Raspberry Pi 4, brushless motors, IMU sensors, pressure sensors, camera system
- **Pivot Date**: October 29, 2025
- **New Approach**: Surface boat with towed probe
- **Reason**: Waterproofing challenges, communication complexity, safety concerns
- **Advantages**: Simpler, more reliable, better suited to actual goal
- **Post-Pivot Development**: Controller enclosure design (e-paper display, Arduino Nano retention system), LoRa communication, electronics integration
- **Source**: `atomic-notes/projects/atlantis-overview-and-pivot.md`, `/home/james/Documents/portfolio-profile/records/atlantis-project/`

### Outcomes
- Demonstrates hardware integration skills
- Shows embedded systems programming
- Proves strategic pivot capability
- Technical innovation: aims for accuracy of ±1-2cm vs professional equipment ±10-50cm
- Cost: $500-$2,000 vs professional equipment $50,000-$200,000
- **Source**: `atomic-notes/projects/atlantis-overview-and-pivot.md`

### Documentation
- 63 chat records spanning September through December 2025
- Comprehensive documentation of technical decisions, challenges, solutions
- **Source**: `atomic-notes/projects/atlantis-overview-and-pivot.md`

---

## Cirrus - Wildfire Prediction System (Cancelled)

### Basic Information
- **Name**: Cirrus
- **Type**: Canadian weather AI prediction system
- **Status**: Cancelled (not completed)
- **Timeline**: 
  - **Proto Project**: weather-data-service (led to Cirrus development)
  - **Start**: January 6, 2025 (frontend map development)
  - **Development**: January 6 - September 21, 2025
  - **Cancellation Date**: September 21, 2025
  - **Duration**: ~8.5 months of development before cancellation
- **Source**: `atomic-notes/projects/cirrus-overview-cancellation.md`, `/home/james/Documents/portfolio-profile/records/cirrus-project/`

### Description
Ambitious Canadian weather AI prediction system combining machine learning, spatial data processing, and complex data visualization. Cancelled before completion but demonstrates technical depth.

### Technologies
- **Frontend**: TypeScript, React
- **Backend**: Python (machine learning, data processing)
- **AI/ML**: Machine learning models, spatial data processing, spatial algorithms
- **Data**: Weather datasets from Canadian sources
- **Source**: `atomic-notes/projects/cirrus-overview-cancellation.md`

### Links
- **Source Code**: https://github.com/DawsonJay/cirrus-project
- **Source**: `atomic-notes/resources/project-links-all.md`

### Key Features (Planned)
- Intelligent weather prediction system for Canadian geography
- Machine learning analysis of historical weather data
- Regional pattern identification
- Spatial data processing for geographic analysis
- Data visualization dashboard with Canada SVG map
- **Source**: `atomic-notes/projects/cirrus-overview-cancellation.md`

### Why Cancelled
- **Primary Reason**: Data quality too poor - 31% precipitation coverage insufficient, 0% wind speed and humidity data
- **Secondary Reasons**: 
  - Interpolation logic failures (field-specific search not finding available stations)
  - Significant data loss during interpolation process
  - Project scope exceeded realistic completion as solo personal project
  - Weather prediction is fundamentally hard
  - Validation complexity
  - Domain expertise required beyond background
- **Data Coverage Issues Discovered**:
  - Temperature: 83% coverage (acceptable)
  - Precipitation: 31% coverage (poor - interpolation failing)
  - Snow depth: 20% coverage (poor)
  - Wind speed: 0% coverage (missing entirely)
  - Humidity: 0% coverage (missing entirely)
- **Source**: `atomic-notes/projects/cirrus-overview-cancellation.md`, `/home/james/Documents/portfolio-profile/records/cirrus-project/`

### Outcomes
- Demonstrates willingness to tackle ambitious technical problems
- Shows experience with machine learning and AI systems
- Proves spatial data processing capability
- Demonstrates judgment to recognize when to cancel projects
- Technical skills transferred to subsequent projects
- **Source**: `atomic-notes/projects/cirrus-overview-cancellation.md`

---

## Portfolio Website

### Basic Information
- **Name**: Portfolio Website
- **Type**: Personal portfolio website
- **Status**: Live (current site)
- **Timeline**: 
  - **Start**: December 19, 2024 (data gathering system and project structure)
  - **Development**: December 19, 2024 - January 11, 2026 (ongoing refinements)
  - **Latest Updates**: January 11, 2026 (project page refinements)
- **Source**: `atomic-notes/resources/project-links-all.md`, `/home/james/Documents/portfolio-profile/records/portfolio-website/`

### Description
Portfolio website featuring theatrical diorama design system with layered SVG animations.

### Technologies
- **Frontend**: React, TypeScript, styled-components
- **Design**: Theatrical diorama design system, layered SVG animations
- **Features**: Article reader with reusable block components, responsive two-panel layouts
- **Source**: `atomic-notes/resources/project-links-all.md`

### Links
- **Live Demo**: Current site (you're viewing it)
- **Source Code**: https://github.com/DawsonJay/portfolio-website
- **Source**: `atomic-notes/resources/project-links-all.md`

### Key Features
- Theatrical diorama design system
- Layered SVG animations
- React and TypeScript architecture
- Styled-components theme system
- Article reader with reusable block components
- Responsive two-panel layouts
- **Source**: `atomic-notes/resources/project-links-all.md`

---

## Professional Work Projects (Nurtur)

### Integrations Dashboard
- **Type**: Internal production system
- **Status**: Still in production (2+ years later)
- **Users**: the sales team (daily use)
- **Technologies**: React/TypeScript (frontend), API endpoints, PostgreSQL (backend)
- **Outcomes**: Zero maintenance, zero crashes, zero bug reports
- **Source Code**: Proprietary (cannot share)
- **Source**: `linked-in-job-hunter/profile-documents/experience.md`, `atomic-notes/resources/project-links-all.md`

### Nexus Dashboard
- **Type**: Enterprise component system / React/TypeScript microfrontend
- **Status**: Project cancelled/team made redundant (February 2026) - wasn't showing results fast enough, considered experimental project
- **Timeline**: July 2022 - February 2026 (primary project), with focused development period October 2025 - February 2026
- **Technologies**: React/TypeScript, foundation block architecture, React Query (for caching), Material UI, Module Federation, TypeSpec, .NET BFF/API
- **Architecture**: Microfrontend integrated into Nexus platform using Module Federation
- **Team**: 2-person team (frontend developer + backend engineer collaboration)
- **Description**: Modern React/TypeScript microfrontend replacing legacy "Robocop" interface for distributed job processing system (Job Dispatcher + Job Managers + multi-tenant queues). Provides real-time visibility and control over a distributed, multi-tenant job processing platform.
- **Key Features**: 
  - Real-time monitoring and control of distributed job processing
  - Multi-tenant queue management with hierarchical organization
  - Job manager control and status monitoring
  - Visual dashboards emphasizing patterns (backlogs, spikes, stuck jobs) rather than raw metrics
  - Drill-down navigation by instance/tenant, queue type, and environment
- **Achievements**: 
  - Reduced load time from 15+ seconds to sub-5 seconds through React Query caching, strategic loading patterns, buffer systems
  - Replaced legacy "Robocop" interface with modern, intuitive UI
  - Improved operations team efficiency and reduced dependency on people who "knew the old screens"
  - Designed reusable component architecture enabling rapid iteration (new graphs in ~10 minutes, new pages in ~30 minutes)
  - Smoothed out complex multi-service local development environment (SQL Server, IIS, .NET 8 APIs, React)
- **Testing**: Playwright e2e tests covering navigation, queue management, error/loading states, and optimistic updates
- **Source Code**: Proprietary (cannot share)
- **Source**: `linked-in-job-hunter/profile-documents/experience.md`, `atomic-notes/resources/project-links-all.md`, `atomic-notes/work/nexus-performance-optimization.md`, `/home/james/Downloads/job-manager-interview-notes.md`, `/home/james/Downloads/cv-project-description.txt`, `/home/james/Downloads/dev_log/`

### Email Editor
- **Type**: Core product rebuild
- **Team Size**: 4-person team
- **Role**: Not leading - worked on creating small components (specifically link editor component using Lexical framework)
- **Timeline**: Worked on it, then left to work on Nexus Dashboard (project continued without me)
- **Status**: Project continued on without me (likely still in development or production)
- **Technologies**: React/TypeScript, Redux Toolkit, Lexical framework (link editor component)
- **Description**: Drag-and-drop email template system for client campaigns
- **Source Code**: Proprietary (cannot share)
- **Source**: `linked-in-job-hunter/profile-documents/experience.md`, `atomic-notes/resources/project-links-all.md`, User feedback 2026-02-07

---

## Project Relationships & Learning Journey

### AI/ML Learning Path
- **Jam Hot** (abandoned) → **Cirrus** (cancelled) → **WhatNow** (successful)
  - Jam Hot: Learned about dataset quality issues (86% validation → 0% real-world accuracy)
  - Cirrus: Applied lessons about data quality, discovered fundamental data coverage problems
  - WhatNow: Solved the dataset problem by generating training data through usage

### Proto Projects
- **weather-data-service** → **Cirrus**
  - weather-data-service was a proto project that led to the development of Cirrus

### Internal Tooling
- **data-core-system**: Internal tooling project (black box for dev logs) - precursor to chat record template system

---

## Early Career Work (Not Documented as Separate Projects)

### BriefYourMarket.com (October 2020 - February 2021)
- **Role**: Junior Developer
- **Work Type**: Debugging and small features
- **Note**: Early career work, nothing especially notable to document as separate projects
- **Source**: `linked-in-job-hunter/profile-documents/experience.md`

### Freelance Work (March 2021 - June 2022)
- **Project**: Client online shop (e-commerce)
- **Technologies**: React, TypeScript, Stripe, Firebase Hosting, Firestore
- **Delivery**: Production-ready build; payments and critical user flows verified end-to-end before handover
- **Client go-live**: Client did not launch the shop to customers after handover (business/adoption decision outside engineering scope)
- **Note**: Substantive client work during freelance period; not packaged as a public portfolio demo
- **Source**: `foundational-notes/factual-notes/work-experience.md`, User feedback 2026-02-07

---

## Gaps to Fill

- [x] WhatNow start date and completion date (October 4-16, 2025)
- [x] moh-ami start date and completion date (January 11, 2026 - rapid build)
- [x] Folio timeline and status (started January 24, 2026, MVP complete, ongoing improvements)
- [x] Atlantis start date (September 4, 2025, pivot October 29, 2025)
- [x] Cirrus start date and cancellation date (January 6, 2025 - September 21, 2025)
- [x] Portfolio website start date (December 19, 2024, ongoing)
- [x] Nexus Dashboard current status (Project cancelled/team redundant February 2026)
- [x] Email Editor current status (Left project to work on Nexus, project continued without me, not leading role - worked on small components)
- [x] Jam Hot project added (predecessor to WhatNow, shows learning journey)
- [x] Other projects assessed: treat-train, lunascope-project, app-forge, lora-evolution, tarot-site-project
  - **lunascope-project**: Fascinating design idea but no practical work yet - not significant enough to document as a project
  - **treat-train, app-forge, lora-evolution, tarot-site-project**: Not significant enough to include
- [x] weather-data-service (proto project that led to Cirrus, not significant enough to document separately)
- [x] Specific metrics/outcomes for each project
  - **WhatNow & moh-ami**: Portfolio projects to demonstrate skills/ideas - no usage metrics (not community-used, made as portfolio pieces)
  - **Integrations Dashboard**: 15+ users (sales team, daily use) - sufficient context documented for factual notes
  - **Nexus Dashboard**: Performance metrics documented (15+ seconds → sub-5 seconds) - sufficient context documented for factual notes
  - **Note**: Usage metrics not available/not applicable for portfolio projects; professional work metrics are sufficient for factual notes. Additional deep-dive documentation could be created later if needed for direct answer notes.

---

## Notes

- All dates should be verified for accuracy
- Project timelines should be comprehensive
- Technologies should match languages-technologies.md file
- Links should be verified and kept up to date
- Status should be current (ongoing, completed, cancelled)

