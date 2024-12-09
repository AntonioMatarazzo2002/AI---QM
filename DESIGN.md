# DESIGN.md

## Overview

The Kria project is a Flask-based web application that analyzes horse performance data to provide riders with tailored advice. Under the hood, our focus has been on achieving a clean separation of concerns, ensuring ease of maintenance, and enabling future scalability. The application’s structure, database schema, and component interactions reflect these priorities.

We’ve chosen a straightforward, minimal stack:  
- **Flask**: Serves as the main framework for routing, session management, and templating.  
- **SQLite**: Chosen for simplicity and portability for both `app.db` (users) and `novabase.db` (horses and race results).  
- **Gunicorn + Nginx (Production)**: Recommended for reliable and secure handling of requests in a production environment.  
- **Git LFS (if needed)**: Ensures that large `.db` files can be efficiently managed and versioned without running into GitHub’s size limitations.

## Project Structure

**Key Files:**
- `app.py`: Defines routes, initializes Flask, manages sessions, handles form submissions, and generates user-oriented pages.
- `helpers.py`: Contains business logic functions (e.g., `analyze_horse_performance`, `generate_report`, `get_horse_id_by_name`). By centralizing logic here, `app.py` remains cleaner and more focused on HTTP request/response handling.
- `templates/`: Jinja2 HTML templates. They keep the front-end separate from the back-end logic, simplifying maintenance.
- `static/`: Holds `styles.css` and other static assets. The CSS attempts to align with a consistent color palette that matches the Kria brand’s aesthetic and evolving logo design (colors may be updated as branding matures).
- `requirements.txt`: Lists external dependencies (Flask, gunicorn).
- `Procfile`: For deployment on platforms like Heroku, specifying `gunicorn` as the WSGI server.

**Database Design:**
- `app.db`: User table stores `email`, `hashed password`, `name`, `sex`, `age`, and `experience`. The schema is intentionally simple, relying on basic SQL operations. Indexes can be added if scaling requires more efficient lookups.
- `novabase.db`: Horses and race_results tables.  
  - **horses**: `horse_id` (PK), `animal_name` (unique).  
  - **race_results**: references `horse_id`, stores `competitor_name` and `time_to_complete`.  
  The data was web scraped from [sdpsistema.com](https://www.sdpsistema.com), ensuring realism. This schema allows easy queries for average times, variance in performance, and checks for patterns (like “paleteador” behavior).

## Design Decisions

1. **Separation of Concerns:**
   The routing logic (in `app.py`) is kept distinct from the business logic (in `helpers.py`). This makes the code more testable and maintainable. Should we decide to add new forms of analysis (e.g., weather conditions, different competition types), we can extend `helpers.py` without cluttering the routing.

2. **User Experience:**
   The front end uses HTML forms and Jinja2 templates. Horse name suggestions rely on a quick AJAX-style request triggered after the user types four characters. This approach reduces friction for the user—no one wants to struggle guessing the correct horse name.

3. **Branding and Aesthetics:**
   While we have not fully finalized the color scheme (and may adjust it as branding evolves), we’ve attempted to keep the application’s design consistent with Kria’s nascent branding. The CSS currently uses colors inspired by the future logo, but these may change after finalizing the logo design. The brand’s Instagram handle, [@kria_qm](https://www.instagram.com/kria_qm), gives an idea of our brand direction and community engagement, even though the final color palette may not be fully established.

4. **Scalability and Performance:**
   For initial deployments, SQLite suffices given the project’s scope. Should the platform grow, we can migrate to a more robust RDBMS like PostgreSQL with minimal code changes, since the logic is encapsulated behind a simple SQL interface. Gunicorn handles concurrency well enough for the current scale, and pairing it with Nginx on a VPS or Heroku ensures stable, performant hosting.

5. **Security Considerations:**
   Passwords are hashed using Werkzeug’s built-in hashing utilities. Session management follows Flask’s recommended best practices. Future enhancements could include adding HTTPS by default, environment variable management for secret keys, and rate limiting to improve security and resilience.

6. **Large File Handling:**
   If we need to commit large `.db` files or other assets, we rely on Git LFS. This keeps the repository manageable and prevents hitting GitHub’s file-size cap. It also sets us up well for maintaining a historical record of performance data without clogging the main repo history.

## Future Directions

- **Refined Branding and Styling:**
  As the Kria brand and logo mature, we will align CSS and templates more closely with the finalized color schemes and design guidelines. Current colors are placeholders that match an early version of the logo and our Instagram presence (check and like it if you can! @kria_qm).

- **Additional Data Points:**
  Future versions might integrate more metrics—like weather or competition type—into `novabase.db`. This could necessitate schema changes and new analysis functions in `helpers.py`.

- **Enhanced User Profiles and Recommendations:**
  With more data, we could offer personalized suggestions, track user history, or integrate a recommendation engine. The current design can evolve by adding new tables (e.g., `user_horse_matches`) and caching aggregate results.

In summary, the design decisions center on keeping the code clean, maintainable, and scalable. We’ve chosen simple tools, consistent logic separation, and a forward-compatible architecture. The brand and design aesthetics will continue to evolve, but the technical foundation is laid for easy adaptation as Kria grows, refining its identity and features to better serve users.
