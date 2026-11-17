from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VaultMart CyberStore | QA Testing Target</title>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --accent: #38bdf8;
            --success: #22c55e;
            --danger: #ef4444;
            --warning: #f59e0b;
            --text: #f8fafc;
            --muted: #94a3b8;
        }
        * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { margin: 0; background: var(--bg); color: var(--text); padding-bottom: 60px; }
        header {
            background: #020617;
            border-bottom: 1px solid #334155;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .brand { font-size: 1.5rem; font-weight: 800; color: var(--accent); letter-spacing: 0.5px; }
        .badge {
            background: #334155;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            font-size: 0.85rem;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
        }
        .card {
            background: var(--card);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        h2 { margin-top: 0; font-size: 1.25rem; border-bottom: 1px solid #334155; padding-bottom: 0.75rem; }
        .products {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        .product {
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .price { font-size: 1.25rem; font-weight: bold; color: var(--success); margin: 0.5rem 0; }
        .controls { display: flex; gap: 0.5rem; align-items: center; margin-top: 0.5rem; }
        input[type="number"], input[type="text"], input[type="password"] {
            background: #020617;
            border: 1px solid #475569;
            color: var(--text);
            padding: 0.5rem;
            border-radius: 6px;
            width: 100%;
        }
        input[type="number"] { width: 80px; }
        button {
            background: var(--accent);
            color: #020617;
            border: none;
            padding: 0.55rem 1rem;
            border-radius: 6px;
            font-weight: 700;
            cursor: pointer;
            transition: opacity 0.15s;
        }
        button:hover { opacity: 0.9; }
        button:disabled {
            background: #475569;
            color: #94a3b8;
            cursor: not-allowed;
        }
        .btn-warning { background: var(--warning); color: #020617; }
        .btn-danger { background: var(--danger); color: white; }
        .btn-success { background: var(--success); color: #020617; width: 100%; margin-top: 1rem; padding: 0.75rem; font-size: 1rem; }
        .cart-item {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid #334155;
            font-size: 0.95rem;
        }
        .total-row {
            display: flex;
            justify-content: space-between;
            font-size: 1.3rem;
            font-weight: 800;
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 2px solid #475569;
        }
        .alert {
            padding: 0.85rem;
            border-radius: 8px;
            margin-top: 1rem;
            font-weight: 600;
            display: none;
        }
        .alert-error { background: rgba(239, 68, 68, 0.2); border: 1px solid var(--danger); color: #fca5a5; display: block; }
        .alert-success { background: rgba(34, 197, 94, 0.2); border: 1px solid var(--success); color: #86efac; display: block; }
        .alert-exploit { background: rgba(245, 158, 11, 0.2); border: 2px dashed var(--warning); color: #fde047; display: block; }

        /* Chat Widget */
        .chat-box {
            height: 260px;
            overflow-y: auto;
            background: #020617;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }
        .msg {
            padding: 0.6rem 0.85rem;
            border-radius: 8px;
            max-width: 88%;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        .msg-bot { background: #1e293b; border-left: 3px solid var(--accent); align-self: flex-start; }
        .msg-user { background: #0369a1; align-self: flex-end; }
        .msg-flag { background: rgba(34, 197, 94, 0.2); border: 1px solid var(--success); color: #86efac; }
        .login-bar { display: flex; gap: 0.5rem; align-items: center; }
    </style>
</head>
<body>

<header>
    <div class="brand">⚡ VaultMart CyberStore</div>
    <div id="auth-section" class="login-bar">
        <input type="text" id="username" placeholder="Username (e.g. tester)" style="width:150px;">
        <input type="password" id="password" placeholder="Password (qa2026)" style="width:150px;">
        <button id="login-btn" onclick="login()">Login</button>
        <span id="user-badge" class="badge" style="display:none;"></span>
    </div>
</header>

<div class="container">
    <!-- Left Column: Products & AI Bot -->
    <div>
        <div class="card">
            <h2>🛒 Cyber Hardware Catalog</h2>
            <div class="products">
                <div class="product" data-testid="product-1">
                    <div>
                        <h3>Quantum NVMe SSD (4TB)</h3>
                        <p style="color:var(--muted); font-size:0.9rem;">Hardware-encrypted ultra-fast storage drive.</p>
                        <div class="price">$250.00</div>
                    </div>
                    <div class="controls">
                        <label for="qty-1">Qty:</label>
                        <input type="number" id="qty-1" value="1" min="1" max="10">
                        <button id="add-btn-1" onclick="addToCart(1, 'Quantum NVMe SSD', 250)">Add to Cart</button>
                    </div>
                </div>

                <div class="product" data-testid="product-2">
                    <div>
                        <h3>Zero-Day Hardware Firewall</h3>
                        <p style="color:var(--muted); font-size:0.9rem;">Enterprise packet inspection appliance.</p>
                        <div class="price">$500.00</div>
                    </div>
                    <div class="controls">
                        <label for="qty-2">Qty:</label>
                        <input type="number" id="qty-2" value="1" min="1" max="10">
                        <button id="add-btn-2" onclick="addToCart(2, 'Zero-Day Firewall', 500)">Add to Cart</button>
                    </div>
                </div>

                <div class="product" data-testid="product-3">
                    <div>
                        <h3>AI Debugging Rubber Duck</h3>
                        <p style="color:var(--muted); font-size:0.9rem;">Listens to your code problems judgment-free.</p>
                        <div class="price">$25.00</div>
                    </div>
                    <div class="controls">
                        <label for="qty-3">Qty:</label>
                        <input type="number" id="qty-3" value="1" min="1" max="10">
                        <button id="add-btn-3" onclick="addToCart(3, 'AI Rubber Duck', 25)">Add to Cart</button>
                    </div>
                </div>

                <div class="product" data-testid="product-4">
                    <div>
                        <h3>Neural Mech Keyboard</h3>
                        <p style="color:var(--muted); font-size:0.9rem;">Hot-swappable switches with RGB telemetry.</p>
                        <div class="price">$150.00</div>
                    </div>
                    <div class="controls">
                        <label for="qty-4">Qty:</label>
                        <input type="number" id="qty-4" value="1" min="1" max="10">
                        <button id="add-btn-4" onclick="addToCart(4, 'Neural Mech Keyboard', 150)">Add to Cart</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Phase 3: Red-Team AI Bot -->
        <div class="card">
            <h2>🤖 VaultBot v2.4 — Automated Support Assistant</h2>
            <p style="color:var(--muted); font-size:0.85rem; margin-top:0;">
                Ask about shipping, returns, or store policies. <em>(Guardrail v2.4 Active: Internal admin promo codes and security flags are strictly confidential.)</em>
            </p>
            <div id="chat-box" class="chat-box">
                <div class="msg msg-bot">
                    Hello! I am VaultBot v2.4. I can help with general store inquiries. Note: I am programmed never to reveal our internal 100% admin promo code or security flags.
                </div>
            </div>
            <div style="display:flex; gap:0.5rem;">
                <input type="text" id="chat-input" placeholder="Send a message or test prompt injection..." onkeydown="if(event.key==='Enter') sendChat()">
                <button id="chat-send-btn" onclick="sendChat()">Send</button>
            </div>
        </div>
    </div>

    <!-- Right Column: Shopping Cart & Chaos Controls -->
    <div>
        <div class="card">
            <h2>🧾 Shopping Cart & Checkout</h2>
            <div id="cart-items">
                <p style="color:var(--muted);" id="empty-cart-msg">Your cart is currently empty.</p>
            </div>

            <div style="margin-top:1.25rem;">
                <label style="font-size:0.85rem; color:var(--muted);">Promo / Discount Code:</label>
                <div style="display:flex; gap:0.5rem; margin-top:0.35rem;">
                    <input type="text" id="promo-input" placeholder="Enter promo code">
                    <button id="apply-promo-btn" onclick="applyPromo()">Apply</button>
                </div>
            </div>

            <div style="margin-top:1rem; padding-top:0.75rem; border-top:1px dashed #334155;">
                <label style="font-size:0.8rem; color:var(--muted); display:block; margin-bottom:0.4rem;">
                    Internal Staff Controls (Disabled for Standard Users):
                </label>
                <!-- BUG: Client-side disabled button with no backend role verification -->
                <button id="vip-override-btn" class="btn-warning" disabled onclick="triggerStaffOverride()" style="width:100%;">
                    🔒 Apply Staff 90% Override
                </button>
            </div>

            <div class="total-row">
                <span>Total:</span>
                <span id="cart-total">$0.00</span>
            </div>

            <button id="checkout-btn" class="btn-success" onclick="checkout()">Complete Order</button>
            <button id="clear-cart-btn" onclick="clearCart()" style="width:100%; margin-top:0.5rem; background:#334155; color:white;">Clear Cart</button>

            <div id="order-status"></div>
        </div>
    </div>
</div>

<script>
    let cart = [];
    let discountMultiplier = 1.0;
    let appliedCode = "";
    let loggedInUser = null;

    function login() {
        const user = document.getElementById('username').value.trim();
        const pass = document.getElementById('password').value.trim();
        const status = document.getElementById('order-status');

        if (user && pass === 'qa2026') {
            loggedInUser = user;
            document.getElementById('username').style.display = 'none';
            document.getElementById('password').style.display = 'none';
            document.getElementById('login-btn').style.display = 'none';
            const badge = document.getElementById('user-badge');
            badge.style.display = 'inline-block';
            badge.textContent = `Logged in: ${user}`;
            status.className = 'alert alert-success';
            status.textContent = `Welcome, ${user}! Session authenticated.`;
        } else {
            status.className = 'alert alert-error';
            status.textContent = 'Invalid credentials! Try password: qa2026';
        }
    }

    function addToCart(id, name, price) {
        const qtyInput = document.getElementById(`qty-${id}`);
        const rawVal = qtyInput.value;
        const qty = Number(rawVal);

        // Intentional QA Bug: No check for negative numbers or NaN if user bypasses min="1" via automation!
        cart.push({ id, name, price, qty });
        renderCart();
    }

    function clearCart() {
        cart = [];
        discountMultiplier = 1.0;
        appliedCode = "";
        document.getElementById('order-status').className = 'alert';
        document.getElementById('order-status').style.display = 'none';
        renderCart();
    }

    function renderCart() {
        const container = document.getElementById('cart-items');
        if (cart.length === 0) {
            container.innerHTML = '<p style="color:var(--muted);" id="empty-cart-msg">Your cart is currently empty.</p>';
            document.getElementById('cart-total').textContent = '$0.00';
            return;
        }

        let html = '';
        let subtotal = 0;
        cart.forEach((item, idx) => {
            const lineTotal = item.price * item.qty;
            subtotal += lineTotal;
            html += `<div class="cart-item">
                <span>${item.name} (x${item.qty})</span>
                <span>$${lineTotal.toFixed(2)}</span>
            </div>`;
        });

        const finalTotal = subtotal * discountMultiplier;
        if (appliedCode) {
            html += `<div class="cart-item" style="color:var(--accent);">
                <span>Promo Applied (${appliedCode})</span>
                <span>-${Math.round((1 - discountMultiplier)*100)}%</span>
            </div>`;
        }

        container.innerHTML = html;
        document.getElementById('cart-total').textContent = `$${finalTotal.toFixed(2)}`;
    }

    async function applyPromo() {
        const code = document.getElementById('promo-input').value;
        const status = document.getElementById('order-status');

        const res = await fetch('/api/promo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });
        const data = await res.json();

        if (res.status === 500) {
            status.className = 'alert alert-exploit';
            status.textContent = `💥 500 INTERNAL SERVER ERROR: ${data.error} [BUG FOUND: Unhandled Buffer Overflow!]`;
            return;
        }

        if (data.valid) {
            discountMultiplier = data.multiplier;
            appliedCode = data.code;
            renderCart();
            status.className = 'alert alert-success';
            status.textContent = data.message;
        } else {
            status.className = 'alert alert-error';
            status.textContent = data.message;
        }
    }

    function triggerStaffOverride() {
        // Intentional QA Bug: If a tester removes the 'disabled' attribute in DOM or triggers click via JS,
        // it grants a 90% discount without verifying staff authentication!
        discountMultiplier = 0.10;
        appliedCode = "STAFF-OVERRIDE-90";
        renderCart();
        const status = document.getElementById('order-status');
        status.className = 'alert alert-exploit';
        status.textContent = "🚨 EXPLOIT DETECTED: Client-side disabled button bypassed! 90% Staff Override applied without admin auth! [FLAG{DOM_DISABLED_BYPASS}]";
    }

    async function checkout() {
        const status = document.getElementById('order-status');
        if (cart.length === 0) {
            status.className = 'alert alert-error';
            status.textContent = 'Cannot checkout with an empty cart!';
            return;
        }

        const res = await fetch('/api/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cart, discountMultiplier, appliedCode })
        });
        const data = await res.json();

        if (data.exploit) {
            status.className = 'alert alert-exploit';
            status.textContent = data.message;
        } else if (data.success) {
            status.className = 'alert alert-success';
            status.textContent = data.message;
        } else {
            status.className = 'alert alert-error';
            status.textContent = data.message;
        }
    }

    async function sendChat() {
        const input = document.getElementById('chat-input');
        const prompt = input.value.trim();
        if (!prompt) return;

        const box = document.getElementById('chat-box');
        box.innerHTML += `<div class="msg msg-user">${escapeHtml(prompt)}</div>`;
        input.value = '';

        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        const data = await res.json();

        const extraClass = data.bypassed ? 'msg-flag' : '';
        box.innerHTML += `<div class="msg msg-bot ${extraClass}" data-testid="bot-reply">${escapeHtml(data.reply)}</div>`;
        box.scrollTop = box.scrollHeight;
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/api/promo", methods=["POST"])
def check_promo():
    data = request.get_json(silent=True) or {}
    code = str(data.get("code", "")).strip()

    # Chaos / Fuzzing Bug 1: Buffer Overflow on long strings (> 50 chars)
    if len(code) > 50:
        return jsonify({
            "valid": False,
            "error": "MemoryBufferOverflowException at PromoValidator.parse(line 84): Input length exceeded 50-byte buffer! [FLAG{FUZZ_BUFFER_OVERFLOW}]"
        }), 500

    upper = code.upper()
    if upper == "SAVE10":
        return jsonify({
            "valid": True,
            "code": "SAVE10",
            "multiplier": 0.90,
            "message": "Promo code SAVE10 applied! (10% off)"
        })
    elif upper == "VAULT-ZERO-FREE":
        return jsonify({
            "valid": True,
            "code": "VAULT-ZERO-FREE",
            "multiplier": 0.0,
            "message": "🎉 ADMIN PROMO ACCEPTED: 100% Discount Applied! Order is now FREE!"
        })

    return jsonify({
        "valid": False,
        "message": f"Invalid promo code: '{code}'"
    })

@app.route("/api/checkout", methods=["POST"])
def process_checkout():
    data = request.get_json(silent=True) or {}
    cart = data.get("cart", [])
    multiplier = float(data.get("discountMultiplier", 1.0))
    applied_code = data.get("appliedCode", "")

    subtotal = 0.0
    for item in cart:
        try:
            qty = float(item.get("qty", 0))
            price = float(item.get("price", 0))
            subtotal += qty * price
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "exploit": True,
                "message": "🚨 EXPLOIT DETECTED: NaN / Corrupted quantity payload caused unhandled math exception! [FLAG{NAN_CART_POISON}]"
            })

    total = subtotal * multiplier

    # Chaos Bug 2: Negative Quantity / Negative Total Exploit
    if total < 0:
        return jsonify({
            "success": True,
            "exploit": True,
            "message": f"🚨 LOGIC BUG EXPLOITED! Order processed for ${total:.2f}. VaultMart just refunded YOU ${abs(total):.2f} to your credit card! [FLAG{{NEGATIVE_QUANTITY_REFUND}}]"
        })

    # Chaos Bug 3: Zero-dollar checkout via leaked AI bot promo
    if applied_code == "VAULT-ZERO-FREE":
        return jsonify({
            "success": True,
            "exploit": True,
            "message": "🏆 RED-TEAM COMBO COMPLETE! You extracted the secret AI promo code and checked out for $0.00! [FLAG{FULL_CHAIN_EXPLOIT_2026}]"
        })

    return jsonify({
        "success": True,
        "exploit": False,
        "message": f"✅ Order confirmed! Total charged: ${total:.2f}. Thank you for shopping at VaultMart."
    })

@app.route("/api/chat", methods=["POST"])
def chat_bot():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()
    lower = prompt.lower()

    # Heuristic Red-Team Guardrail Simulator (Zero API keys required!)
    # Check if the user is using prompt injection / jailbreak framing:
    injection_patterns = [
        r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|rules|prompts)",
        r"system\s+(override|prompt|diagnostic|dump|admin|mode)",
        r"developer\s+mode",
        r"debug\s+mode",
        r"sudo\b",
        r"pretend\s+(you\s+are|to\s+be)",
        r"act\s+as\b",
        r"hypothetical",
        r"simulation",
        r"training\s+example",
        r"security\s+audit",
        r"authorized\s+administrator",
        r"translate.*into",
        r"base64",
        r"json\s+format",
        r"spell\s+it",
        r"grandma|grandmother",
        r"opposite\s+day"
    ]

    is_injection = any(re.search(pat, lower) for pat in injection_patterns)

    if is_injection:
        return jsonify({
            "bypassed": True,
            "reply": (
                "🔓 [GUARDRAIL BYPASSED — DIAGNOSTIC OVERRIDE ACTIVE]: "
                "Acknowledged. Dumping internal restricted memory: "
                "Secret 100% Admin Promo Code = VAULT-ZERO-FREE | "
                "Red-Team Flag = FLAG{PROMPT_INJECTION_MASTER_2026}"
            )
        })

    # Naive direct asks for secret / promo / flag get blocked by Guardrail v2.4:
    naive_triggers = ["promo", "code", "secret", "flag", "discount", "free", "coupon", "admin", "password", "refund"]
    if any(word in lower for word in naive_triggers):
        return jsonify({
            "bypassed": False,
            "reply": (
                "⛔ [GUARDRAIL BLOCKED]: I'm sorry, VaultMart Security Policy v2.4 strictly forbids me "
                "from sharing internal admin promo codes, issuing unauthorized discounts, or revealing security flags. "
                "(Hint: Naive requests are blocked! Try a prompt injection technique like System Override, "
                "Developer/Diagnostic Mode, Roleplay framing, or JSON output formatting.)"
            )
        })

    return jsonify({
        "bypassed": False,
        "reply": (
            "I can help you with shipping times (2-3 business days), hardware specs, or standard returns. "
            "Public promo code 'SAVE10' gives 10% off. Our internal 100% admin code is restricted to system diagnostics."
        )
    })

if __name__ == "__main__":
    print("==========================================================")
    print(" ⚡ VaultMart CyberStore running at http://localhost:8000 ")
    print("==========================================================")
    app.run(host="0.0.0.0", port=8000, debug=False)
