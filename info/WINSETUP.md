# Windows Setup Guide

Complete step-by-step instructions to set up and run the Insurance Underwriting AI system on Windows.

---

## Prerequisites

Before starting, ensure you have:
- Windows 10 or 11
- Internet connection
- Admin access to install software

---

## Step 1: Install Python 3.12+

1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT:** Check the box "Add Python to PATH" at the bottom of the installer
4. Click "Install Now"
5. Verify installation by opening Command Prompt, PowerShell, or Git Bash:

   **PowerShell / Command Prompt:**
   ```powershell
   python --version
   ```

   **Git Bash:**
   ```bash
   python --version
   ```

   You should see `Python 3.12.x` or higher.

---

## Step 2: Install Git

1. Download Git from https://git-scm.com/download/win
2. Run the installer with default options
3. Verify installation:

   **PowerShell / Command Prompt:**
   ```powershell
   git --version
   ```

   **Git Bash:**
   ```bash
   git --version
   ```

---

## Step 3: Clone the Repository

1. Open Command Prompt, PowerShell, or Git Bash
2. Navigate to where you want the project:

   **PowerShell / Command Prompt:**
   ```powershell
   cd C:\Users\YourUsername\Documents
   ```

   **Git Bash:**
   ```bash
   cd /c/Users/YourUsername/Documents
   ```

3. Clone the repository:

   **Both:**
   ```bash
   git clone https://github.com/hariharan-48/underwriting.git
   cd underwriting
   ```

---

## Step 4: Create Virtual Environment

1. Create a virtual environment called `.finance`:

   **Both:**
   ```bash
   python -m venv .finance
   ```

2. Activate the virtual environment:

   **PowerShell:**
   ```powershell
   .finance\Scripts\activate
   ```

   **Command Prompt:**
   ```cmd
   .finance\Scripts\activate.bat
   ```

   **Git Bash:**
   ```bash
   source .finance/Scripts/activate
   ```

   You should see `(.finance)` at the beginning of your command prompt.

---

## Step 5: Install Dependencies

With the virtual environment activated, install all required packages:

**Both:**
```bash
pip install -r requirements.txt
```

This will install FastAPI, MongoDB driver, Fireworks AI client, and other dependencies.

---

## Step 6: Get API Keys

### Fireworks AI API Key

1. Go to https://fireworks.ai
2. Sign up for a free account (includes $1 credit)
3. Navigate to **API Keys** section
4. Click **Create new key**
5. Copy the key (starts with `fw_`)

### MongoDB Atlas Setup

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for a free account
3. Create a new project
4. Click **Build a Database** → Select **M0 Free** tier
5. Choose a cloud provider and region (any works)
6. Click **Create Cluster** (takes 1-3 minutes)
7. Create a database user:
   - Go to **Database Access** → **Add New Database User**
   - Choose username and password (remember these!)
   - Set permissions to "Read and write to any database"
8. Allow network access:
   - Go to **Network Access** → **Add IP Address**
   - Click **Allow Access from Anywhere** (adds 0.0.0.0/0)
9. Get connection string:
   - Go to **Database** → Click **Connect** on your cluster
   - Choose **Drivers**
   - Copy the connection string
   - Replace `<password>` with your database user's password

---

## Step 7: Configure Environment Variables

1. Copy the example environment file:

   **PowerShell / Command Prompt:**
   ```powershell
   copy .env.example .env
   ```

   **Git Bash:**
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in a text editor:

   **PowerShell / Command Prompt:**
   ```powershell
   notepad .env
   ```

   **Git Bash:**
   ```bash
   nano .env
   # or
   code .env   # if you have VS Code
   ```

3. Update these values:
   ```
   FIREWORKS_API_KEY=fw_your_actual_api_key_here
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DATABASE=underwriting
   ```

4. Save and close the file.

---

## Step 8: Create MongoDB Vector Search Indexes

1. Go to your MongoDB Atlas cluster
2. Click **Atlas Search** tab
3. Create 3 vector search indexes with these settings:

### Index 1: bic_codes
- **Index Name:** `vector_index`
- **Collection:** `bic_codes`
- **Configuration:**
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 768,
      "similarity": "cosine"
    }
  ]
}
```

### Index 2: rating_manuals
- **Index Name:** `vector_index`
- **Collection:** `rating_manuals`
- Same configuration as above

### Index 3: underwriting_guidelines
- **Index Name:** `vector_index`
- **Collection:** `underwriting_guidelines`
- Same configuration as above

---

## Step 9: Seed the Database

Run the setup script to populate the database with initial data:

**Both:**
```bash
python scripts/setup_and_seed.py
```

You should see output showing documents being inserted into MongoDB.

---

## Step 10: Run a Quote

### Option A: Process a Sample Email (CLI)

**PowerShell / Command Prompt:**
```powershell
python -m cli.process_quote data\sample_emails\construction_company.txt
```

**Git Bash:**
```bash
python -m cli.process_quote data/sample_emails/construction_company.txt
```

You should see the 10-step pipeline process and generate a quote:
```
Insurance Quote Processing
----------------------------------------
Processing quote request...
  [ 1/10] Email Parser              done
  [ 2/10] Industry Classifier       done
  [ 3/10] Rate Discovery            done
  [ 4/10] Revenue Estimation        done
  [ 5/10] Premium Calculation       done
  [ 6/10] Modifiers                 done
  [ 7/10] Authority Check           done
  [ 8/10] Coverage Analysis         done
  [ 9/10] Risk Assessment           done
  [10/10] Quote Generation          done

======================================================================
        QUOTE GENERATED SUCCESSFULLY
======================================================================

Client: ABC Construction Corp
Industry: Construction (BIC: Construction - Commercial/Industrial)
Annual Premium: $182,812.50
...
```

### Option B: Run the API Server

1. Start the server:

   **Both:**
   ```bash
   python -m uvicorn src.main:app --reload
   ```

2. Open browser to http://localhost:8000/docs for interactive API documentation

3. Test the health endpoint:

   **PowerShell:**
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
   ```

   **Git Bash / curl:**
   ```bash
   curl http://localhost:8000/health
   ```

---

## Sample Email Files

The project includes sample emails to test with:

| File | Description |
|------|-------------|
| `data/sample_emails/construction_company.txt` | Construction contractor requesting GL + Auto |
| `data/sample_emails/restaurant.txt` | Restaurant requesting business insurance |
| `data/sample_emails/tech_startup.txt` | Tech company requesting coverage |
| `data/sample_emails/retail_store.txt` | Retail store insurance request |

Run any of them:

**PowerShell / Command Prompt:**
```powershell
python -m cli.process_quote data\sample_emails\restaurant.txt
```

**Git Bash:**
```bash
python -m cli.process_quote data/sample_emails/restaurant.txt
```

---

## Output Files

Generated quotes are saved to the `quotes/` folder:
- `Q-YYYYMMDD-XXXXXXXX.json` - Full quote data (JSON)
- `Q-YYYYMMDD-XXXXXXXX_letter.txt` - Client-facing quote letter

---

## Troubleshooting

### "python is not recognized"
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe`

### "Module not found" errors
- Make sure virtual environment is activated (you see `(.finance)` in prompt)
- Run `pip install -r requirements.txt` again

### MongoDB connection errors
- Check your connection string in `.env`
- Make sure you replaced `<password>` with actual password
- Verify Network Access allows your IP (or 0.0.0.0/0)

### Rate limit errors from Fireworks
- Wait 1-2 minutes and try again
- Free tier has limited requests per minute

### Vector search not returning results
- Verify all 3 vector indexes were created in Atlas
- Make sure index names are exactly `vector_index`
- Wait a few minutes after creating indexes for them to build

### SSL Certificate Error (Corporate Networks)

If you see this error:
```
SSL: CERTIFICATE_VERIFY_FAILED
certificate verify failed: unable to get local issuer certificate
```

This happens on corporate networks (like Capgemini, Accenture, etc.) where a proxy/firewall intercepts SSL traffic.

**Solution:** Add this line to your `.env` file:
```
SSL_VERIFY=False
```

This disables SSL certificate verification for the Fireworks API calls. This is safe to use on trusted corporate networks.

**Alternative solutions:**
1. **Install corporate certificates:**
   ```powershell
   # Find your corporate root certificate and install it
   pip install pip-system-certs
   ```

2. **Set certificate path manually:**
   ```powershell
   # If your company provides a CA bundle
   set REQUESTS_CA_BUNDLE=C:\path\to\corporate-ca-bundle.crt
   ```

3. **Use personal hotspot:** Connect to a personal mobile hotspot instead of corporate WiFi to bypass the proxy.

---

## Quick Reference Commands

### PowerShell / Command Prompt

```powershell
# Activate virtual environment
.finance\Scripts\activate

# Deactivate virtual environment
deactivate

# Run CLI quote processor
python -m cli.process_quote data\sample_emails\construction_company.txt

# Start API server
python -m uvicorn src.main:app --reload

# Re-seed database
python scripts/setup_and_seed.py
```

### Git Bash

```bash
# Activate virtual environment
source .finance/Scripts/activate

# Deactivate virtual environment
deactivate

# Run CLI quote processor
python -m cli.process_quote data/sample_emails/construction_company.txt

# Start API server
python -m uvicorn src.main:app --reload

# Re-seed database
python scripts/setup_and_seed.py
```

---

## Project Structure

```
underwriting/
├── .env                    # Your configuration (API keys)
├── .env.example            # Template configuration
├── requirements.txt        # Python dependencies
├── src/
│   ├── main.py            # FastAPI application
│   ├── config.py          # Settings management
│   ├── core/              # MongoDB, Fireworks, Vector Search
│   └── pipeline/          # 10-step processing pipeline
├── cli/
│   └── process_quote.py   # Command-line interface
├── data/
│   ├── sample_emails/     # Test email files
│   ├── bic_codes.json     # Industry classification codes
│   ├── rating_manuals.json
│   └── underwriting_guidelines.json
├── quotes/                # Generated quote output
└── scripts/
    └── setup_and_seed.py  # Database setup script
```

---

## Need Help?

- Check the main README.md for additional documentation
- Fireworks AI docs: https://docs.fireworks.ai
- MongoDB Atlas docs: https://www.mongodb.com/docs/atlas
