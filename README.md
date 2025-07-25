# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/4da3b2a5-fba6-4640-89af-26f5958213c1

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/4da3b2a5-fba6-4640-89af-26f5958213c1) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## Environment Setup

This project requires specific environment variables for both the backend and frontend to function properly. Since this is a monorepo with both backend and frontend in the same repository, all environment variables are combined in a single `.env` file.

### Environment Variables (.env)

Create a `.env` file in the project root (where main.py and vite.config.ts are located) with the following content:

```
# Backend variables
DATABASE_URL=postgresql://postgres:Drijfveer123!@localhost:5432/song_scribe_local
API_KEY=jouwsong2025
LOG_LEVEL=INFO
PLUGPAY_API_KEY=<vul-zaak-specifieke-waarde-in>
PLUGPAY_SECRET=<vul-zaak-specifieke-waarde-in>

# Frontend variables
VITE_API_URL=https://jouwsong-api.onrender.com
```

### Configuration Check

- Backend: The project uses `python-dotenv` to load environment variables via `load_dotenv()` in various files including `main.py`, `app/db/session.py`, and `app/auth/token.py`.
- Frontend: The Vite configuration uses `loadEnv` to load environment variables, making them available via `import.meta.env.VITE_API_URL`.

### Security Note

The `.env` file is included in `.gitignore` to prevent committing sensitive information to the repository.

### Debugging

#### Viewing Raw API Responses

To view raw JSON responses from external APIs (like Plug&Pay):

1. Set the `LOG_LEVEL` environment variable to `DEBUG` in your `.env` file:
   ```
   LOG_LEVEL=DEBUG
   ```

2. Restart the application to apply the new log level.

3. When the application makes API calls, the raw JSON responses will be logged to the console or log files.

4. For production deployments on Render, you can set the `LOG_LEVEL` environment variable in the Render dashboard under Environment Variables.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/4da3b2a5-fba6-4640-89af-26f5958213c1) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/tips-tricks/custom-domain#step-by-step-guide)
