import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

DEX_SEARCH_URL = "https://api.dexscreener.com/latest/dex/search"


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Crypto AI Trading Bot is running.")

    def log_message(self, format, *args):
        return


def start_health_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


def money(value):
    if value is None:
        return "N/A"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    if value >= 1_000:
        return f"${value / 1_000:.2f}K"

    return f"${value:.6f}"


def get_pairs(query):
    response = requests.get(
        DEX_SEARCH_URL,
        params={"q": query},
        timeout=15
    )

    response.raise_for_status()

    return response.json().get("pairs", [])


def analyze_pair(pair):
    liquidity = (pair.get("liquidity") or {}).get("usd") or 0
    volume = (pair.get("volume") or {}).get("h24") or 0
    price_change = (pair.get("priceChange") or {}).get("h24") or 0

    txns = (pair.get("txns") or {}).get("h24") or {}

    buys = txns.get("buys", 0)
    sells = txns.get("sells", 0)

    score = 0

    if liquidity >= 100_000:
        score += 25
    elif liquidity >= 25_000:
        score += 15

    if volume >= 100_000:
        score += 25
    elif volume >= 25_000:
        score += 15

    if price_change > 0:
        score += 20

    if buys > sells:
        score += 20

    total_transactions = buys + sells

    if total_transactions > 0:
        if buys / total_transactions >= 0.55:
            score += 10

    if score >= 75:
        signal = "🟢 STRONG SETUP"
    elif score >= 55:
        signal = "🟡 WATCH"
    else:
        signal = "🔴 AVOID / WEAK"

    return {
        "score": score,
        "signal": signal,
        "liquidity": liquidity,
        "volume": volume,
        "change": price_change,
        "buys": buys,
        "sells": sells,
    }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🤖 Crypto AI Trading Agent

Bot is online.

Commands:

/scan COIN
DEX market scanner.

/analyze COIN
Market analysis.

/help
Show commands.

⚠️ Current mode: PAPER TRADING
No real money is being traded.
"""
    )


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Use:\n/scan SOL\n\nExample:\n/scan PEPE"
        )
        return

    query = " ".join(context.args).strip()

    await update.message.reply_text(
        f"🔎 Scanning DEX markets for {query}..."
    )

    try:
        pairs = get_pairs(query)

        if not pairs:
            await update.message.reply_text(
                f"❌ No DEX pairs found for {query}."
            )
            return

        pairs = sorted(
            pairs,
            key=lambda p: (p.get("liquidity") or {}).get("usd") or 0,
            reverse=True
        )

        results = []

        for pair in pairs[:5]:
            analysis = analyze_pair(pair)

            base = pair.get("baseToken", {})
            quote = pair.get("quoteToken", {})

            symbol = base.get("symbol", query)
            quote_symbol = quote.get("symbol", "USD")

            chain = pair.get("chainId", "unknown")
            dex = pair.get("dexId", "unknown")
            price = pair.get("priceUsd")

            results.append(
                f"""
<b>{symbol}/{quote_symbol}</b>

⛓ Chain: {chain}
🏦 DEX: {dex}
💵 Price: ${price or 'N/A'}

💧 Liquidity: {money(analysis['liquidity'])}
📊 24h Volume: {money(analysis['volume'])}
📈 24h Change: {analysis['change']}%

🟢 Buys: {analysis['buys']}
🔴 Sells: {analysis['sells']}

🎯 Score: {analysis['score']}/100
{analysis['signal']}
"""
            )

        text = "🔎 <b>DEX MARKET SCAN</b>\n"
        text += "\n".join(results)

        text += (
            "\n\n⚠️ Market research only."
            "\nNo real trade has been executed."
        )

        await update.message.reply_text(
            text,
            parse_mode="HTML"
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Scan error:\n{error}"
        )


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Use:\n/analyze SOL\n\nExample:\n/analyze BONK"
        )
        return

    query = " ".join(context.args).strip()

    await update.message.reply_text(
        f"🧠 Analyzing {query}..."
    )

    try:
        pairs = get_pairs(query)

        if not pairs:
            await update.message.reply_text(
                "❌ I couldn't find this coin on DEX markets."
            )
            return

        pairs = sorted(
            pairs,
            key=lambda p: (p.get("liquidity") or {}).get("usd") or 0,
            reverse=True
        )

        pair = pairs[0]
        result = analyze_pair(pair)

        base = pair.get("baseToken", {})
        symbol = base.get("symbol", query)

        price = pair.get("priceUsd", "N/A")
        chain = pair.get("chainId", "N/A")
        dex = pair.get("dexId", "N/A")

        message = f"""
🧠 <b>CRYPTO ANALYSIS</b>

🪙 Coin: {symbol}
⛓ Chain: {chain}
🏦 DEX: {dex}

💵 Price: ${price}

💧 Liquidity: {money(result['liquidity'])}
📊 24h Volume: {money(result['volume'])}
📈 24h Change: {result['change']}%

🟢 Buys: {result['buys']}
🔴 Sells: {result['sells']}

🎯 Score: {result['score']}/100

<b>{result['signal']}</b>

🚧 Next modules:
• AI analysis
• Technical indicators
• Website research
• X/Twitter research
• Contract risk checks
• Entry / SL / TP
• Automatic alerts
• Paper trading engine

Current mode: PAPER TRADING.
"""

        await update.message.reply_text(
            message,
            parse_mode="HTML"
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Analysis error:\n{error}"
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🤖 Crypto AI Trading Agent

/scan COIN
DEX market scanner.

/analyze COIN
Market analysis.

/help
Show commands.

🚧 Coming next:
• AI analysis
• Technical indicators
• Website research
• X/Twitter research
• Contract risk checks
• Entry / SL / TP
• Automatic alerts
• Paper trading
• Later: automatic trading
"""
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    health_thread = threading.Thread(
        target=start_health_server,
        daemon=True
    )

    health_thread.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("help", help_command))

    print("Crypto AI Trading Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
