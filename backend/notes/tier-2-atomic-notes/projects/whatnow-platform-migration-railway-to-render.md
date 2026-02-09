# WhatNow: Platform Migration from Railway to Render

WhatNow was originally deployed to Railway, but I migrated it to Render due to changing platform economics and pricing structures. This migration demonstrates my ability to handle infrastructure changes, manage database transitions, and maintain application reliability through platform switches.

Railway was my initial choice for deployment because it offered generous free tier resources and extremely simple deployment workflows - connect your GitHub repository, Railway detects it's a Python or Node.js project, and it deploys automatically. The platform handled environment variables cleanly, provided managed PostgreSQL, and made deployments feel effortless. For getting WhatNow to production quickly, Railway was perfect.

The problems started when Railway changed their pricing model. What had been generous free tier resources became limited, and the costs for running both frontend and backend services with a PostgreSQL database were going to be significantly higher than I wanted to pay for a personal project. I evaluated alternatives and settled on Render, which offered similar managed services with better pricing for my specific usage patterns.

The migration required careful planning to avoid data loss and downtime. The most critical aspect was the PostgreSQL database, which contained all user accounts, activity data, user preference histories, and the Base AI model weights. Losing that data would mean losing all the learning the system had accumulated through real usage.

The database migration process involved creating a dump of the Railway PostgreSQL database, setting up a new managed PostgreSQL instance on Render, importing the data to the new database, verifying data integrity after migration, updating application environment variables to point to the new database, and testing thoroughly before switching over the frontend. Having a clear migration checklist and rollback plan meant I could execute the migration confidently.

Configuration differences between platforms required some adjustments. Railway and Render have different ways of handling build commands, environment variables, health checks, and deployment triggers. I had to update the configuration files and deployment settings to work with Render's expectations while maintaining the same application behavior.

One challenge was the PostgreSQL connection string format. Railway and Render use slightly different formats for database URLs, particularly around SSL configuration and connection pooling. I had to adjust the database connection code to handle these differences without changing application logic. Using environment variables for all configuration made this manageable - I could test different connection patterns locally before deploying.

The frontend static site deployment was more straightforward than the backend. React builds generate static files that can be hosted anywhere. I configured Render to build the frontend from the GitHub repository, generate the production bundle, and serve it through their CDN. The main consideration was ensuring the API URLs pointed to the new backend location.

Testing the migration was crucial. I set up the entire stack on Render before switching over from Railway - backend API deployed, database imported and verified, frontend deployed and configured. I tested all functionality: context input, activity generation, favorites marking, regeneration, final selection, Session AI learning, Base AI updates, and user account operations. Only after confirming everything worked correctly did I update DNS and consider the migration complete.

The experience taught me several lessons about platform dependencies. First, abstracting infrastructure dependencies makes migrations easier - using environment variables for configuration, avoiding platform-specific features unless necessary, and designing for portability even when you don't immediately need it. Second, managed services are convenient but create platform lock-in - the easier a platform makes things, the harder it can be to leave. Third, having clear migration procedures and testing processes reduces risk when changes are necessary.

Post-migration, WhatNow runs reliably on Render with no noticeable differences in performance or functionality from the user perspective. The backend API responds quickly, the database handles queries efficiently, and the frontend loads fast. From a user's perspective, nothing changed - which is exactly what you want from a successful migration.

What makes this notable is that it demonstrates infrastructure maturity. Many developers build projects that work on one specific platform and would be difficult to move. I built WhatNow in a way that allowed platform migration with manageable effort when business needs (in this case, cost considerations) required it. That's the kind of forward-thinking that matters in production systems.

For employers, this shows several capabilities: I can handle infrastructure and deployment beyond just writing application code, I make pragmatic decisions about platform choices based on real constraints, I execute complex migrations including data migration and configuration updates, I test thoroughly to ensure reliability through changes, and I can adapt systems to changing infrastructure requirements. These are skills that separate developers who build applications from developers who maintain production systems over time.

The Railway to Render migration is in the GitHub commit history, and the current live deployment on Render shows the successful outcome. This transparency means potential employers can verify that the migration happened and worked, not just take my word for it.

