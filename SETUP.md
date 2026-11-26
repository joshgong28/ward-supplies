# Workshop setup: Antigravity on Google Cloud

In this workshop you work with an AI agent, Antigravity, on a small app that runs in your own Google Cloud project. This page gets you ready at the start of the workshop.

Your facilitator gives you:
- A **project ID**. Use it wherever this page says `YOUR_PROJECT_ID`.
- A **workshop Google account**. You sign in with it in steps 3 and 4.

**On your own laptop:** start at step 1.

**On a virtual machine:** if you can't install software on your laptop (on a Chromebook, for example), you work on a virtual machine instead, and your facilitator also gives you a PIN. Open your virtual machine first, just below, then go on at step 2.

## Open your virtual machine

The virtual machine is a Linux computer in Google Cloud. You use it in Chrome, through Chrome Remote Desktop. Everything from step 1 is already installed on it.

1. In Chrome, open [remotedesktop.google.com/access](https://remotedesktop.google.com/access) and sign in with your workshop Google account. If Chrome picks another account, choose "Use another account".
2. Click **workshop-vm** and enter your PIN. The virtual machine opens in the tab.
3. Open **Terminal** from the start menu (bottom left). To paste in it, press **Ctrl+Shift+V**.
4. If a "Choose password for new keyring" window appears, now or later: leave both fields empty, click **Continue**, then **Continue** again. It won't ask again.

Now go to step 2, and do everything from there on the virtual machine. Where the slides say Cmd+Q, press Ctrl+Q.

## 1. Install the tools

**Where to type the commands on this page:** on macOS, in **Terminal** (press Cmd+Space and type "Terminal"). On Windows, in **Git Bash**, which comes with git: open the Start menu and type "Git Bash". Not Command Prompt or PowerShell.

Install them in this order. If you already have one, just do its check. Run each check in a new terminal: a terminal that was already open may not find a tool you just installed. On Linux, follow the instructions on each download page.

### git

- **macOS:** in Terminal, run `git --version`. If git isn't installed, macOS offers to install the command line developer tools: click **Install**.
- **Windows:** download git from [git-scm.com/install](https://git-scm.com/install/) and run the installer. Keep the default on every screen. This also installs Git Bash.
- **Check:** `git --version` shows a version number.

### Python 3.10 or newer

- **macOS:** if you have [Homebrew](https://brew.sh), run `brew install python@3.14`. If not, open [python.org's macOS page](https://www.python.org/downloads/macos/), find the newest **Python 3.14** under **Stable Releases**, click **macOS installer** and run it. When it's done, a Finder window opens: double-click **Install Certificates.command** in it. The Python that comes with macOS (3.9) is too old.
- **Windows:** open [python.org's Windows page](https://www.python.org/downloads/windows/). Under **Stable Releases**, find the newest **Python 3.14** and click **Windows installer (64-bit)**. On the first screen, tick **Add python.exe to PATH**, then click **Install Now**.
- **Check:** `python3 --version` shows 3.10 or newer. On Windows, `python --version`.

### Google Cloud CLI (gcloud)

Open [the install page](https://docs.cloud.google.com/sdk/docs/install-sdk) and choose your operating system.

- **macOS:** download the package for your Mac: ARM64 for Apple silicon (M1 or newer), x86_64 for Intel. Double-click it to unpack it, move the `google-cloud-sdk` folder to your home folder, then run `~/google-cloud-sdk/install.sh` in Terminal. Answer **Y** when it asks to update your PATH.
- **Windows:** download and run the Google Cloud CLI installer, and keep the defaults. On the last screen, untick **Start Google Cloud SDK Shell** and untick **Run 'gcloud init'**: the setup script in step 3 signs you in.
- **Check:** `gcloud --version` shows a version number.

### Antigravity

Download it from [antigravity.google/download](https://antigravity.google/download#antigravity-2) and install it. On macOS, open the downloaded file and drag Antigravity to Applications.

- **Check:** it opens. Signing in comes in step 4.

## 2. Get the workshop files

1. Open a new terminal: **Terminal** on macOS and on the virtual machine, **Git Bash** on Windows.
2. Go to your home folder:

   ```bash
   cd ~
   ```

3. Download the workshop files:

   ```bash
   git clone https://github.com/joshgong28/ward-supplies ward-supplies
   ```

4. Go into the new `ward-supplies` folder:

   ```bash
   cd ward-supplies
   ```

Keep this terminal open: step 3 runs in this folder.

## 3. Connect gcloud to your project

```bash
./participant-setup.sh YOUR_PROJECT_ID
```

On the virtual machine, gcloud first warns that you're running on a Google Compute Engine virtual machine and asks whether to continue: type **y** and press Enter.

Your browser opens twice. **Both times, sign in with your workshop Google account**, not your work account. If the browser picks an account automatically, choose "Use another account". If Chrome then offers to sign in to Chrome with this account, choose **Use Chrome without an account**: don't sign in to Chrome itself with the workshop account.

When it's done, the script prints the address of your app. Keep it: you need it in the labs.

## 4. Sign in to Antigravity and open the app

Open Antigravity and sign in:
1. Choose **Use Business Account**, then **Continue with Google Cloud**. Not "Continue with Google".
2. In the browser, choose your workshop Google account. If Chrome offers to sign in to Chrome, choose **Use Chrome without an account** again.
3. Choose **Subscription**. Under **Choose a Subscription**, pick **Gemini Enterprise Plus** from the **healthcare demo** project with location **global**.
4. When Antigravity asks what best describes your work, click **Skip**.

Then create a project for the app. In the sidebar, next to **Projects**, click the **Create New Project** button (a folder with a +) and choose the `ward-supplies` folder.

The chat box now shows `ward-supplies` at the top left. Set it up:
1. **Model:** click the model button next to the **+** on the left, and choose **Gemini 4 Neon** at **Medium**.
2. **Mode:** click the mode button next to the microphone on the right, and choose **Turbo**: the agent then runs its commands without asking you first. If you're not comfortable with that, choose **Request Review** (you approve every command) or **Default** (you approve the sensitive ones) instead. You'll then be asked to approve many commands, especially in lab 2.

## 5. Set the agent's limits

Open Antigravity's settings, then **General**, and set **Outside of folders file access policy** to **Always Ask**. Choosing Turbo sets it to Allow; with Always Ask, the agent asks before it reads or changes files outside the workshop folder. If Allow is disabled by your organisation, it already says Always Ask.

Then go to **Tool Permissions → Open → Terminal Commands**. For each rule below, click **Add**, pick the type in the dropdown, and type the command:

| Type | Command |
|---|---|
| Deny | `gcloud config configurations` |
| Deny | `gcloud config set` |
| Deny | `gcloud iam service-accounts keys create` |
| Ask | `rm` |

The Deny rules stop the agent from switching to another account or project, and from creating long-lived keys. The Ask rule makes it ask before it deletes files.

Don't change the mode in the chat box after this: choosing a mode resets the settings above.

## 6. Check that it works

Start a new conversation and type:

> run gcloud run services list

It should run without asking, list the service `ward-supplies`, and print a warning that calls are "executed as `antigravity-agent@YOUR_PROJECT_ID…`". That's correct: the agent works through a service account that only has access to your workshop project.

## If something goes wrong

| You see | What to do |
|---|---|
| The setup script fails with a permission error | You probably signed in with another account. Run the script again and choose your workshop account both times |
| Antigravity doesn't offer the Gemini Enterprise Plus licence | You signed in with another account. Sign out (Settings → your profile, bottom left → Sign out) and sign in again with your workshop account |
| Antigravity asks before running commands, though you chose Turbo | Choose Turbo again in the chat box, then do step 5 again |
| The agent's gcloud shows your own email instead of the workshop account | In a terminal, run `gcloud config configurations activate antigravity-workshop` |
| gcloud warns that the project lacks an "environment" tag | Ignore it |
| gcloud says your login has expired | In the `ward-supplies` folder, run `./participant-setup.sh YOUR_PROJECT_ID` again |

## What the setup changes on your laptop

- **gcloud:** adds a configuration called `antigravity-workshop` and makes it active. Your own configurations stay as they are.
- **Application default credentials** (what SDKs use): replaced with workshop ones.
- **Antigravity:** signed in with your workshop account, and the settings from steps 4 and 5.

In Turbo, the agent's commands run on your laptop without asking. What keeps it in check: the rules from step 5, the workshop rules in `AGENTS.md`, and the service account it works through, which only has access to your workshop project.

The agent can technically use any account gcloud is logged in with on your laptop. If you're logged in with an account that has access to production systems, log it out for the day with `gcloud auth revoke ACCOUNT`.

## After the workshop

Remove the workshop login from gcloud, with your workshop account's email:

```bash
gcloud auth revoke YOUR_WORKSHOP_ACCOUNT
```

```bash
gcloud auth application-default revoke
```

**Optional**, only if you used gcloud with your own account before the workshop: switch back to it.

```bash
gcloud config configurations activate default
```

```bash
gcloud auth application-default login
```

Then:
- In Antigravity: Settings → Customizations → Installed MCP Servers. Delete the servers you built: they point into your workshop folders.
- Stop the lab 4 app if it still runs on your laptop.
- Sign out of Antigravity: Settings → your profile, bottom left → Sign out.
- Put Antigravity's settings back the way you like them.
- Your Google Cloud project: your facilitator cleans it up.
