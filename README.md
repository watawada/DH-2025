# Study Buddy
---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Setup](#setup)
4. [Contributors](#contributors)

## Project Overview
---
Study Buddy is an app designed to streamline the studying process for students. The app leverages Google Gemini's API to create prompts for flashcards and quizzes for any text PDF you choose to upload as well as Auth0 for secure logins. 

## Technologies Used
---
- Gemini
- MongoDB
- React
- Node.js
- FastAPI
- Bootstrap
- Axios

## Setup
---
**Requirements**

- Install Node and npm
- Either Python or Python3
- Create a venv in the server (optional but recommended)
- Create a Mongodb cluster, either locally or deployed
- Create an Auth0 app (https://auth0.com/)

1. Setup dotenv file to hold important keys. Inside the dotenv file, include the following:
   - Gemini API Key
   - Auth0 Client ID, Domain, Client Secret
   - MongoURI
2. Install dependencies on clientside with
   ```bash
   npm install
   ```
   Start client by running
   ```bash
   npm run dev
   ```
3. Install dependencies on serverside with
   ```bash
   pip install -r requirements.txt
   ```
   For Python 3, run
   ```
   pip3 install -r requirements.txt
   ```
   Start the client by running
   ```bash
   uvicorn main:app --reload
   ```
4. Navigate to http://localhost:8001 to view the web app.

## Contributors
---
Kelvin Mai (https://github.com/watawada) - Backend Developer

Richard Gabel (https://github.com/RichardGabel) - Backend Developer

Johnathon Ty (https://github.com/jonathan-ty) - Frontend Developer

Kevin Yang (https://github.com/yuankaikevinyang) - Frontend Developer


