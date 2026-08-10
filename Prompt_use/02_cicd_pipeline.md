Level 1 — CI/CD Pipeline (the ONLY thing this level does)
Goal: a GitHub repo that, on every git push to main, automatically builds a container and deploys it to Google Cloud Run, giving a public URL. No app yet — just a tiny GET /health endpoint, so we prove the pipeline works before building anything.

 git push main ──▶ GitHub Actions ──▶ build image ──▶ push to Artifact Registry ──▶ deploy Cloud Run ──▶ public URL
Follow the parts in order. Parts 1–3 are manual (do them on screen); Part 4 is the Claude Code prompt; Parts 5–6 are the payoff demo.

Part 0 — What you need (accounts & tools)
A GitHub account.
A Google Cloud account with billing enabled (Cloud Run has an always-free tier, but Google still requires a billing account attached; new accounts get $300 free credit).
gcloud CLI installed locally (brew install --cask google-cloud-sdk) — or just use the in-browser Cloud Shell, which has it preinstalled.
Part 1 — Set up the GitHub repo
# in Desktop/saas-app
git init
git branch -M main
gh repo create marketpulse-saas --public --source=. --remote=origin   # or create it in the UI
We'll push actual files in Part 5. Keep the repo empty/minimal for now.

Part 2 — Set up Google Cloud (the "what to get" part — show this live)
Set variables once (pick your own project id; it must be globally unique):

export PROJECT_ID="marketpulse-saas-123"
export REGION="us-central1"
export REPO="app-images"            # Artifact Registry repo name
export SERVICE="marketpulse-api"    # Cloud Run service name
export SA_NAME="gh-deployer"        # service account for GitHub Actions
1. Create the project and set it active

gcloud projects create "$PROJECT_ID"
gcloud config set project "$PROJECT_ID"
# Attach billing (get your account id with: gcloud billing accounts list)
gcloud billing projects link "$PROJECT_ID" --billing-account=XXXXXX-XXXXXX-XXXXXX
2. Enable the APIs we use

gcloud services enable run.googleapis.com artifactregistry.googleapis.com
3. Create an Artifact Registry repo (where our Docker images live)

gcloud artifacts repositories create "$REPO" \
  --repository-format=docker --location="$REGION" \
  --description="MarketPulse container images"
4. Create a service account for GitHub Actions to deploy as

gcloud iam service-accounts create "$SA_NAME" \
  --display-name="GitHub Actions deployer"
export SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
5. Grant it exactly the roles it needs (least privilege — explain each)

# push images to Artifact Registry
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" --role="roles/artifactregistry.writer"
# deploy/update Cloud Run services
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" --role="roles/run.admin"
# allow it to act as the Cloud Run runtime service account
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" --role="roles/iam.serviceAccountUser"
6. Create a key file for that service account (this is the secret GitHub will hold)

gcloud iam service-accounts keys create key.json --iam-account="$SA_EMAIL"
# key.json is a SECRET. It is already git-ignored. Delete it after pasting into GitHub.
More secure alternative (mention, optional): Workload Identity Federation removes the long-lived key entirely. For the class, the JSON key is simpler; note WIF as the prod path.

Part 3 — Put the values into GitHub as secrets
Repo → Settings → Secrets and variables → Actions → New repository secret. Add:

Secret	Value
GCP_PROJECT_ID	your $PROJECT_ID
GCP_REGION	your $REGION (e.g. us-central1)
GCP_SA_KEY	the entire contents of key.json
GCP_AR_REPO	your $REPO (e.g. app-images)
GCP_SERVICE	your $SERVICE (e.g. marketpulse-api)
CLI shortcut (with gh):

gh secret set GCP_PROJECT_ID -b"$PROJECT_ID"
gh secret set GCP_REGION -b"$REGION"
gh secret set GCP_AR_REPO -b"$REPO"
gh secret set GCP_SERVICE -b"$SERVICE"
gh secret set GCP_SA_KEY < key.json
Parts 2–3 (UI version) — do it in the Console instead of the CLI
Same result as the gcloud commands above, but click-by-click — better for showing live. Everything is at console.cloud.google.com.

UI Step 1 — Create the project
Top bar project dropdown → New Project
Name marketpulse-saas → note the auto-generated Project ID → Create → select it in the dropdown.
UI Step 2 — Enable billing
☰ → Billing → Link a billing account (or Manage billing accounts → Add billing account and enter a card).
Confirm the project shows Billing: enabled.
UI Step 3 — Enable the two APIs
☰ → APIs & Services → Library.
Search "Cloud Run Admin API" → Enable.
Search "Artifact Registry API" → Enable.
UI Step 4 — Create the image repository
☰ → Artifact Registry → Repositories → Create Repository.
Name app-images · Format Docker · Mode Standard · Region us-central1 → Create.
UI Step 5 — Create the deploy service account
☰ → IAM & Admin → Service Accounts → Create Service Account.
Name gh-deployer → Create and Continue.
Grant these 3 roles (add one at a time): Artifact Registry Writer, Cloud Run Admin, Service Account User → Done.
UI Step 6 — Download its key (the one real secret)
Service Accounts list → click gh-deployer → Keys tab.
Add Key → Create new key → JSON → Create → key.json downloads.
⚠️ Grants deploy access — don't leave it on screen; paste into GitHub (Part 3) then delete it.
UI Step 7 — Add the GitHub secrets in the UI
Repo → Settings → Secrets and variables → Actions → New repository secret.
Add the 5 from the Part 3 table (GCP_SA_KEY, GCP_PROJECT_ID, GCP_REGION, GCP_AR_REPO, GCP_SERVICE).
Part 4 — Prompt to paste into Claude Code (generates the app + pipeline)
Create the minimum needed to prove a CI/CD pipeline to Google Cloud Run. Do NOT build any
product features.

1. backend/app/main.py: a FastAPI app with a single route GET /health that returns
   {"status": "ok", "version": "v1"}. It must listen on the port from the PORT env var
   (default 8080) because Cloud Run injects PORT.
2. backend/requirements.txt: fastapi and uvicorn[standard].
3. backend/Dockerfile: slim python:3.12 image, install requirements, copy app, and run
   `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}`. No --reload.
4. .dockerignore.
5. .github/workflows/deploy.yml — on push to main:
   - checkout
   - authenticate to Google Cloud with google-github-actions/auth@v2 using
     credentials_json = secrets.GCP_SA_KEY
   - set up gcloud (google-github-actions/setup-gcloud@v2)
   - configure docker for Artifact Registry:
     gcloud auth configure-docker ${{ secrets.GCP_REGION }}-docker.pkg.dev
   - build the image tagged
     ${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/${SERVICE}:${{ github.sha }}
     from ./backend, and push it
   - deploy to Cloud Run with google-github-actions/deploy-cloudrun@v2 (service = GCP_SERVICE,
     region = GCP_REGION, the image above, flags: --allow-unauthenticated)
   - echo the deployed service URL at the end of the job
   Pull project id, region, repo, service from the GitHub secrets. No values hardcoded.
   Add clear comments on each step — students will read this file line by line.

Then commit everything.
For reference, the workflow it produces should look like this:

name: Deploy to Cloud Run
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - id: auth
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      - uses: google-github-actions/setup-gcloud@v2
      - name: Configure Docker for Artifact Registry
        run: gcloud auth configure-docker ${{ secrets.GCP_REGION }}-docker.pkg.dev --quiet
      - name: Build & push image
        run: |
          IMAGE="${{ secrets.GCP_REGION }}-docker.pkg.dev/${{ secrets.GCP_PROJECT_ID }}/${{ secrets.GCP_AR_REPO }}/${{ secrets.GCP_SERVICE }}:${{ github.sha }}"
          docker build -t "$IMAGE" ./backend
          docker push "$IMAGE"
          echo "IMAGE=$IMAGE" >> "$GITHUB_ENV"
      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: ${{ secrets.GCP_SERVICE }}
          region: ${{ secrets.GCP_REGION }}
          image: ${{ env.IMAGE }}
          flags: --allow-unauthenticated
Part 5 — First deploy (prove the sync)
git add -A && git commit -m "chore: CI/CD pipeline + health endpoint"
git push -u origin main
Open the repo's Actions tab → watch the job run. When it's green, the last step prints the Cloud Run URL. Open it at /health → you should see {"status":"ok","version":"v1"}.

Part 6 — The "it syncs!" demo (your class steps 10–11)
Edit backend/app/main.py: change "version": "v1" to "version": "v2 — live from class".
git commit -am "demo: change response" && git push
Watch the Action run again → refresh the Cloud Run URL → the response changed, with no manual deploy. That's continuous deployment.
Troubleshooting (keep handy)
403 / permission denied on deploy → a role from Part 2.5 is missing on the SA.
repository not found on push → Artifact Registry repo name/region mismatch (Part 2.3).
PORT errors / container won't start → app must read PORT env and bind 0.0.0.0.
Billing error enabling APIs → billing account not linked (Part 2.1).
Auth step fails → GCP_SA_KEY secret must be the full JSON, including { }.
Teaching notes
The spine of the course: infra before features. Everything later just rides this pipeline.
Point at each IAM role and say why it exists — least privilege is a real security lesson.
key.json never touches git; it lives only in GitHub Secrets + Cloud Run. Ties to Level 0's "no secrets in code" rule. Delete the local key.json after Part 3.