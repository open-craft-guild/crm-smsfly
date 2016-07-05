[![Stories in Ready](https://badge.waffle.io/wk-tech/crm-smsfly.png?label=ready&title=Ready)](https://waffle.io/wk-tech/crm-smsfly) [![Build Status](https://travis-ci.org/wk-tech/crm-smsfly.svg?branch=master)](https://travis-ci.org/wk-tech/crm-smsfly) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/eeaedf06e82a4bceaf8a75423885a796)](https://www.codacy.com/app/webknjaz/crm-smsfly?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wk-tech/crm-smsfly&amp;utm_campaign=Badge_Grade) [![Requirements Status](https://requires.io/github/wk-tech/crm-smsfly/requirements.svg?branch=master)](https://requires.io/github/wk-tech/crm-smsfly/requirements/?branch=master)
# crm-smsfly
Embedded integration of some CRM with SMS-Fly gateway via iframe.

# Development

## Prerequisites
- If you use OS X or Windows, first install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [vagrant](https://www.vagrantup.com/docs/installation/) and then install `vargant-vagga` plugin (`vagrant plugin install vagrant-vagga`). After that run `vagrant up` to populate VM image.
- If you use GNU/Linux based OS, just install [vagga](https://vagga.readthedocs.io/en/latest/installation.html)
- Populate `.env` file with environment variables, such as `DEBUG`, `DATABASE_URL`, `CRM_DB_URL`, `SMSFLY_ID`, `SMSFLY_PASS`, `DJANGO_DEBUG_LOG`, `DJANGO_LOG_LEVEL`
- Install `pre-commit` with `pip intall pre-commit; pre-commit install` in your environment to make sure your code conforms basic rules


## Running the app
Navigate to repo root in your terminal and then run:
```shell
$ vagga run-cached
```
N.B. in case of non-linux installation, prepend that with `vagrant`.

Now you should be able to [open the /app in browser](http://localhost:8000/app)

# Production
Just check `deploy/` folder and run corresponding playbook with [ansible](http://docs.ansible.com/ansible/intro_installation.html). Store environment variables in `deploy/roles/smsapp/templates/smsapp.env` first (see `smsapp.env.example`).

# Notes
Please remember to pass `crm_user_id` GET param in order to identify current user of an external CRM.
