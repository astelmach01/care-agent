# ML Project

This project is a full-stack application with a React frontend and a Python backend.

## Structure

- `/frontend`: Contains the React frontend application.
- `/backend`: Contains the Python backend services.

See the README files in each directory for setup and running instructions.

You'll need 3 terminals open: 1 for the flask app, 1 for the main backend server that handles the agent, and another for the frontend.

## Environment Variables

Create a `.env` file in the root directory with the following content (based on `.env.example`):

```
OPENAI_API_KEY=your_openai_api_key_here
```

You can copy the example file and fill in your actual API key:

```bash
cp .env.example .env
# Then edit .env with your actual OpenAI API key
```
