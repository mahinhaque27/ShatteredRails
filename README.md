# Shattered Rails Capstone Project

## Description
This repo displays all the files associated with the senior capstone project Shattered Rails.
This includes the source code and technical documents such as SRS, Design Document, and Test Plan.

This project created two text based adventure games. The first game features a branching storyline with different endings depending on the choices the user makes and the second game is a combat focused game with more battle mechanics compared to the first game. This project features full login/authentication and saving where the user last left off in the game.

## Group Members
* Mahin Haque
* Ankith Goutham
* Jayanth Nama
* Lilac Sabri

## How to Run For the First Time
* Clone repo: `git clone https://github.com/gouthama320/Capstone-Project-4996.git`
* Change into TextAdventure directory: `cd  TextAdventure`
* Ensure you have **Python 3.12.1** or higher installed ([Python Download](https://www.python.org/downloads/))
* Ensure you have **Django 5.0.1** and **six 1.10** or higher, if not installed run `pip install Django` and/or `pip install six`
* Run command to update local database schema after doing git pull: `python manage.py makemigrations`
* Also run `python manage.py migrate`
* To run project use command: `python manage.py runserver`
* In your chrome browser go to: `http://127.0.0.1:8000/`

## Pages
* Landing page: `http://127.0.0.1:8000/`
* Game selection page: `http://127.0.0.1:8000/index2`
* Login page: `http://127.0.0.1:8000/login`
* Register page: `http://127.0.0.1:8000/register`
* Game 1 page: `http://127.0.0.1:8000/game`
* Game 2 page: `http://127.0.0.1:8000/game2`
* Start page before game 1: `http://127.0.0.1:8000/start`
* Start page before game 2: `http://127.0.0.1:8000/start1`
* Profile page: `http://127.0.0.1:8000/profile`
* Admin page: `http://127.0.0.1:8000/admin`

### After Merging a Branch
* Change into TextAdventure directory: `cd  TextAdventure`
* Run command to update local database schema after doing git pull: `python manage.py makemigrations`
* Also run `python manage.py migrate`
* To run project use command: `python manage.py runserver`

### To view database
* Go to admin page `http://127.0.0.1:8000/admin`
* Login with credentials:
   Username: `mahin27`
   Password: `textadventure`
