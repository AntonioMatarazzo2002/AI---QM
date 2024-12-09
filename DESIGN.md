```markdown
# DESIGN.md

## Overview

This design document provides a technical look into how Kria’s code is structured and why certain decisions were made. Kria is a local-only demonstration of a horse-rider match analysis tool originally developed in Portuguese. The English version you have here is meant to be tested and run locally, not deployed online, due to time constraints and the desire to maintain the original production environment in Portuguese.

## Architectural Choices

- **Flask as the Core Framework:**  
  Flask’s simplicity and flexibility allow a clean separation of routing and logic. We keep routes in `app.py` and core logic in `helpers.py`, ensuring maintainability. This also makes adding new features or analyses straightforward.

- **SQLite Databases:**  
  Both `app.db` and `novabase.db` are SQLite files. This choice was made for simplicity—no external database servers are needed. This is ideal for local testing and demonstration. While platforms like Heroku offer Postgres, we are not deploying this version online, so SQLite’s out-of-the-box support in Python is sufficient.

- **Real Data Integration:**  
  The `novabase.db` file includes real horse performance data scraped from [sdpsistema.com](https://www.sdpsistema.com). This authentic data adds complexity and realism to the analysis. By using a simple SQL schema (`horses` and `race_results` tables), we can easily query average times, check consistency, and identify “paleteador” patterns.

## Logic and Structure

- **app.py:**  
  Contains Flask routes and session management. It receives user input from forms (e.g., for login, creating accounts, checking matches), calls the logic functions in `helpers.py`, and renders templates.

- **helpers.py:**  
  Houses the core business logic. Functions for analyzing horse performance, generating user profiles, and producing the final report are all here. This keeps `app.py` focused on HTTP concerns and `helpers.py` on analytics and computations.

- **Templates and Static Files:**  
  Templates use Jinja2 for HTML rendering. The static CSS file attempts to follow a color scheme that might match the main Kria branding in the future, though the final design is still in flux. Since the Portuguese production version is under active design refinement, we haven’t locked in the exact colors yet.

## Deployment Decisions

- **Local-Only Execution:**
  Initially, we considered platforms like Heroku or VPS deployments, but Heroku does not support SQLite without additional steps, and we are short on time to reconfigure or test a new database system. This English version remains local-only, allowing straightforward testing without dealing with cloud configurations.

- **No Online Version for the English Build:**
  The original version is in Portuguese, aligned with our brand and target audience. We present this English version to demonstrate functionality only. Without the constraints of adapting the database or re-deploying under time pressure, the local environment suffices.

## Future Considerations

- **Branding and Color Scheme:**
  The CSS and color palette are placeholders. We have an Instagram presence (@kria_qm) that hints at future brand directions, but as of now, we’ve not finalized the visual identity. Once the brand colors and logo are set, we can update the CSS to match them more closely.

- **Scalability and Database Upgrades:**
  If we were to deploy this English version online or scale up, we’d likely migrate from SQLite to a more robust database like PostgreSQL and adjust the code accordingly. For now, the simplicity of SQLite suits local demos.

- **Additional Features:**
  Future iterations might integrate more metrics or improve performance analysis. The current modular design makes it easy to add new columns in `novabase.db` or more logic in `helpers.py`.

## Conclusion

The Kria application’s design prioritizes clarity, maintainability, and ease of local demonstration. By using simple tools (Flask, SQLite) and keeping logic separated from routing, we ensure that anyone exploring the code can easily understand how it works and how to adapt it in the future. The offline, English-only version provided here is a technical demonstration, reflecting our design philosophy without the complexities of a full production deployment.
