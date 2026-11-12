# Workshop environment

This workspace is Ward Supplies, an ordering site for hospital ward supplies, deployed to Google Cloud for a hands-on workshop. All data is fictional.

## Google Cloud

- gcloud is already configured for this workshop: the project, the region (`europe-west4`) and the service account you act as. Read them with `gcloud config list`.
- The app runs on Cloud Run as service `ward-supplies`. Read its logs with `gcloud logging read` or `gcloud run services logs read ward-supplies`.
- Deploy from source with `gcloud run deploy ward-supplies --source .` from this folder. Existing settings (service account, secrets, memory) are kept unless you change them.
- New Cloud Run services must run as `app-runtime@<project>.iam.gserviceaccount.com` and use `--max-instances 3`.
- gcloud may warn that the project lacks an `environment` tag. Ignore it: it isn't part of the workshop, and you can't change tags.

## This laptop

- Only read and change files inside this folder. Don't touch anything else on the laptop. One exception: you may add MCP servers to Antigravity's global MCP config, `~/.gemini/config/mcp_config.json`, keeping the existing entries.
- Put Python environments in `.venv` in this folder. Don't install anything outside it: no `brew`, `sudo`, `npm -g` or `pip` outside `.venv`.
- Ask before deleting files.

## Boundaries

- Never run `gcloud auth ...`, `gcloud config configurations ...`, `gcloud config set` or `gcloud config unset`, and never pass `--account`, `--configuration` or `--impersonate-service-account` flags.
- Never create service account keys. If you hit a permission error, stop and report it instead of working around it.
- Ask before deleting any cloud resource.

## Antigravity customizations

- In a custom agent's `tools` list, use Antigravity's exact tool names, such as `view_file`, `list_dir`, `grep_search`, `write_to_file`, `replace_file_content`, `run_command`, `manage_task` and `read_url_content`. Names like `read_file` or `edit_file` don't exist, and the docs warn that an unknown name can make the agent hang.
