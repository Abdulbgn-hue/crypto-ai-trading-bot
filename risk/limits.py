from config import (
    MAX_RISK_PER_TRADE,
    MAX_DAILY_LOSS,
    MAX_OPEN_TRADES,
    MAX_POSITION_USD,
    MIN_SIGNAL_SCORE,
    MIN_RISK_REWARD,
)


RISK_LIMITS = {
    "max_risk_per_trade_percent": MAX_RISK_PER_TRADE,
    "max_daily_loss_percent": MAX_DAILY_LOSS,
    "max_open_trades": MAX_OPEN_TRADES,
    "max_position_usd": MAX_POSITION_USD,
    "min_signal_score": MIN_SIGNAL_SCORE,
    "min_risk_reward": MIN_RISK_REWARD,
}


def get_risk_limits() -> dict:
    return dict(RISK_LIMITS)


def emergency_stop_active() -> bool:
    """
    Returns True when emergency stop is enabled.
    The execution engine must refuse new trades
    while the emergency stop is active.
    """

    from config import EMERGENCY_STOP

    return EMERGENCY_STOP


def can_open_trade(
    signal_score: float,
    open_trades: int,
    daily_loss_percent: float,
) -> dict:

    if emergency_stop_active():
        return {
            "allowed": False,
            "reason": "Emergency stop is active.",
        }

    if signal_score < MIN_SIGNAL_SCORE:
        return {
            "allowed": False,
            "reason": (
                f"Signal score {signal_score} "
                f"is below minimum "
                f"{MIN_SIGNAL_SCORE}."
            ),
        }

    if open_trades >= MAX_OPEN_TRADES:
        return {
            "allowed": False,
            "reason": "Maximum open trades reached.",
        }

    if daily_loss_percent >= MAX_DAILY_LOSS:
        return {
            "allowed": False,
            "reason": "Maximum daily loss reached.",
        }

    return {
        "allowed": True,
        "reason": "All risk limits passed.",
    }


def cap_position_size(
    position_usd: float,
) -> float:

    if position_usd <= 0:
        return 0.0

    return min(
        position_usd,
        MAX_POSITION_USD,
  )
