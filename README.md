# Vehicle Safety Dashboard with Vehicle Recall Notification
* **Author**: Joseph Shifman, github: [jshifman](https://github.com/jshifman)
* **Major**: B.S. Computer Science
* **Year**: 2022

# Type of project
A Django-based web application utilizing a free and open-source database API from the National Highway Traffic Safety Administration.
Hosted on http://35.227.169.250/ (as of December 2022, best viewed on a computer browser)

# Purpose (including intended audience)
For any car or vehicle owner who wants to know if their vehicle requires a recall service.

# Explanation of files

* `apps/` - Contains configurations for each application
    - `authentication/` - Contains Django-specific files for authentication, adding users, and changing password
    - `home/` - Contains Django-specific files for dashboard, search pages, adding vehicle model to users, and account page
        - `tasks.py` - Outlines instructions for celery beat worker to send emails every 24 hours if there are new recalls for user's vehicles
        - `views.py` - Back-end logic for all screens on the home application, includes dashboard and search page logic with API requests
* `core/` - Contains base Django configurations
* `nginx/` - Contains configurations for Nginx web application
* `commands.txt` - Celery command line instructions to start celery worker and celery beat
* `Dockerfile` - Django web application docker configuration
* `docker-compose.yml` - Docker configuration for starting all services in single container

# Completion status

## Enhancements:

- [ ] Celery beat task for updating dashboard data periodically instead of dynamically
- [ ] Recall search results page display all on one page without sideways scroll

# Can someone else work on this project?
No

# Public Display/dissemination
- Fall 2022 CSU Chico College of Engineering, Computer Science, and Construction Management Design Expo

# License
