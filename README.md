# Home-Nexus
Real Estate App
A flask web application for a platform pertaining to the real estate market in Oxford, OH. This application allows the user to
search for properties based on various criteria such as: Listing price, Square feet, the year the establishment was built, number
of beds, number of baths, and number of days on site. This application also provides the user with a favorites page to add any properties
that may catch their eye as well as a sign up page to create an account and manage the properties they wish to view further. 

Features:
- User Authentication (both login and sign up)
- Property search which includes various filters 
- Advanced search based on address of property
- Favorites page which includes adding and removing
- View favorites
- Profile settings

Installation:
- clone the repository
- Navigate to project directory
- create python environment: using these
    - python -m venv env
    - source env/bin/activate  # On Windows, use `env\Scripts\activate`
- install dependencies: flask and sqlalchemy
    - pip install flask
    - pip install flask_sqlalchemy
- you should now be able to run start.py

Usage:
- Navigate to the webpage after running start.py and clicking on http://localhost:5000/
- create an account on the page and now you should be able to search up various properties


## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.csi.miamioh.edu/maricafm/real-estate-app.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.csi.miamioh.edu/maricafm/real-estate-app/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***
