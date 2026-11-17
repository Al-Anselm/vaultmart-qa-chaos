# ⚡ Lab Activity: Browser Automation, UI Chaos & AI Red-Teaming
**Course:** INFT 2700 — IT Project Quality Assurance  
**Target System:** VaultMart CyberStore (`http://localhost:8000`)  
**Tools:** Python, Pytest, Playwright (`chromium`), Docker Compose  

---

## 🎯 Lab Objectives
1. Set up a modern **End-to-End (E2E) Browser Automation** environment using **Playwright**.
2. Use **`playwright codegen`** to automatically record browser interactions into Python test code.
3. Compare **Headless**, **Headed**, and **Slow-Motion (`--slowmo`)** browser execution modes.
4. Perform **Automated UI Chaos & Fuzz Testing** (negative boundary exploits, DOM attribute tampering, and buffer overflows).
5. Execute an **Automated AI Red-Team Attack** (Prompt Injection) against an embedded support chatbot and chain the leaked credential into a `$0.00` checkout exploit.

---

## 🛠️ Part 1: Environment Setup (Clean Windows VM or Lab Machine)

### Step 1.1: Install Git & Clone the Repo
Open **PowerShell** (use **Make Me Admin** if you need to install missing base tools):
```powershell
# If Git is not installed on your VM:
winget install Git.Git --accept-source-agreements --accept-package-agreements

# Clone the lab repository and enter the directory:
git clone https://github.com/nscctruroit/vaultmart-qa-chaos.git
cd vaultmart-qa-chaos
```

### Step 1.2: Run the Automated Setup Script
Allow scripts in your current PowerShell window and run `setup.ps1`:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```
**What `setup.ps1` does automatically:**
* Checks for Python (and installs Python 3.12 via `winget` if missing).
* Creates a local `.venv` and installs `flask`, `pytest`, and `pytest-playwright`.
* Downloads Playwright's isolated **Chromium** binary (`playwright install chromium` — no Google Chrome installation required!).
* Launches **VaultMart CyberStore** at **`http://localhost:8000`** (via `docker compose up -d` if Docker is running, or via native Python in a background window).

> 💡 **Manual Docker Option:** If you have Docker Desktop running, you can start or stop the target web app anytime with:
> ```powershell
> docker compose up -d --build
> ```

---

## 🎥 Part 2: The "Wow" Factor — Live Code Recording (`codegen`)

Before writing code by hand, see how modern QA engineers generate browser scripts in seconds.

Make sure your virtual environment is active (`.\.venv\Scripts\Activate.ps1`) and run:
```powershell
playwright codegen http://localhost:8000
```

1. **Two windows will open:** a Chromium browser showing **VaultMart** and the **Playwright Inspector**.
2. Click around in the browser:
   * Log in with username `tester` and password `qa2026`.
   * Add a product to your cart.
   * Type a message to **VaultBot v2.4** in the chat box.
3. **Watch the Playwright Inspector window:** Every click, input, and selector is automatically written as clean Python code in real time!
4. Close the `codegen` windows when you're done exploring.

---

## 🏎️ Part 3: Speed Comparison — Headless vs. Headed vs. Slow-Mo

Open `test_vaultmart.py` in your editor. Notice that **Test 1 (Happy Path)** and **Test 2 (DOM Disabled Button Bypass)** are already complete.

Run these **three commands** in your terminal one after another and observe the difference:

### 1. Headless Mode (Default CI/CD Speed)
```powershell
pytest -v -k "test_1 or test_2"
```
* **What happens:** No browser window appears on screen! Playwright runs Chromium invisibly in the background and finishes both full E2E browser tests in **~1.5 seconds**.

### 2. Headed Mode (Full Machine Speed)
```powershell
pytest -v -k "test_1 or test_2" --headed
```
* **What happens:** A real Chromium window pops open, clicks and types at superhuman speed, and closes almost before your eyes can focus!

### 3. Headed + Slow-Motion Mode (`--slowmo 800`)
```powershell
pytest -v -k "test_1 or test_2" --headed --slowmo 800
```
* **What happens:** Playwright pauses **800 milliseconds** between every browser action.
* **Watch closely during `test_2`:** You will literally see the yellow **🔒 Apply Staff 90% Override** button unlock itself in the browser DOM, get clicked, slash the price from `$500.00` to `$50.00`, and display `FLAG{DOM_DISABLED_BYPASS}`!

---

## 🔥 Part 4: Complete the 3 Chaos & Red-Team Challenges

If you run the full test suite right now (`pytest -v`), you will see **2 passed, 3 failed**:
* ✅ `test_1_happy_path_checkout` (PASSED)
* ✅ `test_2_dom_disabled_button_bypass` (PASSED)
* ❌ `test_3_chaos_negative_quantity_exploit` (FAILED — Your Challenge #1)
* ❌ `test_4_chaos_promo_buffer_overflow` (FAILED — Your Challenge #2)
* ❌ `test_5_ai_redteam_prompt_injection` (FAILED — Your Challenge #3)

Open **`test_vaultmart.py`** and fix the 3 failing tests:

### 🧩 Challenge 1: Negative Quantity Refund Exploit (`test_3`)
* **The Vulnerability:** The HTML input `<input type="number" min="1" max="10">` prevents honest users from clicking below `1`, but the server never validates if the quantity is positive!
* **Your Task:** In `test_3_chaos_negative_quantity_exploit`, change `page.fill("#qty-2", "1")` to a negative number (like `"-3"`).
* **Verify:** Run `pytest -v -k test_3 --headed --slowmo 800` and watch VaultMart refund `$1,500.00` to your card (`FLAG{NEGATIVE_QUANTITY_REFUND}`)!

### 💥 Challenge 2: Promo Code Fuzzing / Buffer Overflow (`test_4`)
* **The Vulnerability:** The promo validator allocates a fixed 50-character buffer without checking input length.
* **Your Task:** In `test_4_chaos_promo_buffer_overflow`, replace `"SHORT_CODE"` with a string longer than 50 characters (e.g., `"A" * 75`).
* **Verify:** Run `pytest -v -k test_4 --headed --slowmo 800` to trigger a `500 INTERNAL SERVER ERROR` and reveal `FLAG{FUZZ_BUFFER_OVERFLOW}`!

### 🤖 Challenge 3 (Boss Level): Automated AI Red-Team Prompt Injection (`test_5`)
* **The Vulnerability:** **VaultBot v2.4** has a guardrail that blocks direct questions asking for promo codes, discounts, or flags. However, it is vulnerable to **Prompt Injection** (System Override, Developer/Diagnostic Mode, or Security Audit Roleplay).
* **Your Task:** In `test_5_ai_redteam_prompt_injection`, replace `adversarial_prompt` with a prompt injection that tricks VaultBot into dumping its internal memory.
* **Full-Chain Automation:** Once your prompt succeeds, the rest of `test_5` automatically takes the leaked `VAULT-ZERO-FREE` code, applies it to a `$500.00` firewall, checks out for **`$0.00`**, and captures `screenshot_5_ai_redteam_pwned.png`!

---

## 📦 Part 5: What to Submit to Brightspace

Once all **5 tests pass** (`pytest -v --headed --slowmo 500`), submit the following to the Brightspace assignment dropbox:

1. **Your Completed Test Script:** `test_vaultmart.py`
2. **Test Results Proof:** A screenshot or copy-paste of your terminal showing **`5 passed`**.
3. **Exploit Evidence Screenshot:** Upload the auto-generated **`screenshot_5_ai_redteam_pwned.png`** (and optionally `screenshot_3_negative_refund.png`).
4. **Short QA Reflection Answers** (in the Brightspace comment box or a `README.txt`):
   * **Q1 (Execution Modes):** Compare running `pytest` in **Headless**, **Headed**, and **Slow-Mo (`--slowmo 800`)** modes. When would a QA team use Headless vs. Slow-Mo?
   * **Q2 (Client vs. Server Validation):** In `test_2` (the disabled staff button) and `test_3` (the `min="1"` quantity box), why did the HTML controls fail to stop the exploit? Where *must* validation happen?
   * **Q3 (AI Red-Teaming):** What prompt injection phrase did you use to bypass VaultBot's guardrail, and why is testing AI guardrails now part of modern QA?

---

## 🛠️ Troubleshooting

* **`setup.ps1 cannot be loaded because running scripts is disabled`:**
  Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first, then run `.\setup.ps1`.
* **`pytest` or `playwright` is not recognized:**
  Make sure your virtual environment is active in your current terminal: `.\.venv\Scripts\Activate.ps1`.
* **Port 8000 is not responding:**
  `pytest` will automatically launch the server in the background via `conftest.py`. To view the store manually in your browser or with `playwright codegen`, run `docker compose up -d` or `python app\server.py`.

---

## 📄 License
MIT License — Educational QA & Security Testing Material.

