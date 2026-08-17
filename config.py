import os


# =========================
# TELEGRAM
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


# =========================
# TRADING MODE
# =========================

# LIVE = real-money trading
# OFF = trading disabled
TRADING_MODE = os.getenv("TRADING_MODE", "OFF").upper()

AUTO_TRADE = os.getenv("AUTO_TRADE", "false").lower() == "true"


# =========================
# RISK MANAGEMENT
# =========================

MAX_RISK_PER_TRADE = float(
    os.getenv("MAX_RISK_PER_TRADE", "1")
)

MAX_DAILY_LOSS = float(
    os.getenv("MAX_DAILY_LOSS", "5")
)

MAX_OPEN_TRADES = int(
    os.getenv("MAX_OPEN_TRADES", "3")
)

MAX_POSITION_USD = float(
    os.getenv("MAX_POSITION_USD", "50")
)


# =========================
# MARKET SCANNER
# =========================

SCAN_INTERVAL_SECONDS = int(
    os.getenv("SCAN_INTERVAL_SECONDS", "60")
)

MIN_LIQUIDITY_USD = float(
    os.getenv("MIN_LIQUIDITY_USD", "25000")
)

MIN_VOLUME_24H_USD = float(
    os.getenv("MIN_VOLUME_24H_USD", "25000")
)


# =========================
# SIGNAL SETTINGS
# =========================

MIN_SIGNAL_SCORE = int(
    os.getenv("MIN_SIGNAL_SCORE", "75")
)

MIN_RISK_REWARD = float(
    os.getenv("MIN_RISK_REWARD", "2")
)


# =========================
# SUPPORTED CHAINS
# =========================

CHAINS = [
    "ethereum",
    "base",
    "bsc",
    "arbitrum",
    "polygon",
    "solana",
]


# =========================
# AI
# =========================

AI_ENABLED = (
    os.getenv("AI_ENABLED", "false").lower() == "true"
)

AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "openai"
)


# =========================
# RESEARCH
# =========================

WEBSITE_RESEARCH_ENABLED = (
    os.getenv(
        "WEBSITE_RESEARCH_ENABLED",
        "true"
    ).lower() == "true"
)

TWITTER_RESEARCH_ENABLED = (
    os.getenv(
        "TWITTER_RESEARCH_ENABLED",
        "true"
    ).lower() == "true"
)

NEWS_RESEARCH_ENABLED = (
    os.getenv(
        "NEWS_RESEARCH_ENABLED",
        "true"
    ).lower() == "true"
)


# =========================
# ALERTS
# =========================

ALERTS_ENABLED = (
    os.getenv("ALERTS_ENABLED", "true").lower()
    == "true"
)


# =========================
# SAFETY
# =========================

EMERGENCY_STOP = (
    os.getenv(
        "EMERGENCY_STOP",
        "true"
    ).lower() == "true"
)


def validate_config():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing."
        )

    if not WEBHOOK_SECRET:
        raise RuntimeError(
            "WEBHOOK_SECRET is missing."
        )

    if TRADING_MODE not in ["OFF", "LIVE"]:
        raise RuntimeError(
            "TRADING_MODE must be OFF or LIVE."
        )

    if MAX_RISK_PER_TRADE <= 0:
        raise RuntimeError(
            "MAX_RISK_PER_TRADE must be greater than 0."
        )

    if MAX_DAILY_LOSS <= 0:
        raise RuntimeError(
            "MAX_DAILY_LOSS must be greater than 0."
        )

    if MAX_OPEN_TRADES <= 0:
        raise RuntimeError(
            "MAX_OPEN_TRADES must be greater than 0."
        )

    if MIN_SIGNAL_SCORE < 0 or MIN_SIGNAL_SCORE > 100:
        raise RuntimeError(
            "MIN_SIGNAL_SCORE must be between 0 and 100."
)
