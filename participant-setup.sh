#!/usr/bin/env bash
# One-time setup on a participant's laptop (macOS or Linux).
#
#   ./participant-setup.sh PROJECT_ID [REGION]
#
# Creates a gcloud configuration called antigravity-workshop and makes it the
# active one, so Antigravity's agent picks it up. Everything gcloud and the SDKs
# do then runs as the agent service account in the participant's project.
# The participant's own gcloud setup stays in its own configuration.
set -euo pipefail

PROJECT_ID="${1:?usage: participant-setup.sh PROJECT_ID [REGION]}"
REGION="${2:-europe-west4}"
CONFIG="antigravity-workshop"
AGENT_SA="antigravity-agent@${PROJECT_ID}.iam.gserviceaccount.com"

if ! gcloud config configurations describe "$CONFIG" >/dev/null 2>&1; then
  gcloud config configurations create "$CONFIG" --no-activate
fi

# Sign in before activating: activating refreshes the saved login, and an
# expired one asks for a password in the terminal instead of the browser.
echo "==> Sign in with your workshop Google account."
gcloud auth login --configuration "$CONFIG"
gcloud config configurations activate "$CONFIG"

gcloud config set project "$PROJECT_ID"
gcloud config set run/region "$REGION"
gcloud config set auth/impersonate_service_account "$AGENT_SA"

echo "==> Sign in once more, for the credentials that SDKs and MCP servers use."
gcloud auth application-default login --impersonate-service-account "$AGENT_SA"

echo "==> Checking access."
URL="$(gcloud run services describe ward-supplies --format 'value(status.url)')"

cat <<EOF

Done. gcloud now acts as $AGENT_SA in $PROJECT_ID
(configuration: $CONFIG). Your website is reachable at $URL

After the workshop, follow "After the workshop" in SETUP.md.
EOF
