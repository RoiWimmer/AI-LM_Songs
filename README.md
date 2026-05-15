# AI-LM Songs Agent

## Project Goal
Build an AI-based music agent that can search and analyze a dataset of ~5,000 songs, 
identify relevant songs based on user queries, 
and use Google Gemini API to generate smart explanations and recommendations.

## Current Architecture
- **Frontend:** Static website hosted on Render Static Site.
- **Data Source:** Local `songs.json` file generated from the original Excel dataset.
- **Search Logic:** JavaScript loads `songs.json` and filters/ranks relevant songs according to the user query.
- **AI Layer:** Google Gemini API is used to generate natural-language answers based on the relevant songs found.
- **Backend/API Proxy:** Google Apps Script is planned as a lightweight backend to call Gemini securely without exposing the API key in the frontend.

## What Needs To Be Done

1. Convert the Excel songs dataset into `songs.json`.
2. Add `songs.json` to the GitHub repository.
3. Update `index.html` / JavaScript to load the songs data with `fetch("songs.json")`.
4. Implement local search/filter logic over the songs dataset.
5. Send only the most relevant results to the AI layer, not the entire dataset.
6. Create a Google Apps Script endpoint that receives the user question and relevant songs.
7. Store the Gemini API key inside Apps Script, not inside the frontend.
8. Connect the frontend to the Apps Script endpoint.
9. Display the AI response inside the chat interface.
10. Deploy the site on Render as a Static Site.

## Important Notes
- No database is needed because the dataset is small (~1MB).
- Do not call Gemini directly from `index.html`, because the API key would be exposed.
- Render Static Site is enough for the frontend, but it cannot run backend API code.
- If a real backend is needed later, create a separate Render Web Service.
