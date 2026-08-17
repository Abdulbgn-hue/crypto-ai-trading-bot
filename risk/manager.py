from typing import Dict


def calculate_position_size(
    balance_usd: float,
    entry_price: float,
    stop_loss: float,
    risk_percent: float,
    max_position_usd: float,
) -> Dict:

    if balance_usd <= 0:
        return {
            "allowed": False,
            "reason": "Invalid balance.",
        }

    if entry_price <= 0:
        return {
            "allowed": False,
            "reason": "Invalid entry price.",
        }

    if stop_loss <= 0:
        return {
            "allowed": False,
            "reason": "Invalid stop-loss.",
        }

    if stop_loss >= entry_price:
        return {
            "allowed": False,
            "reason": "Stop-loss must be below entry.",
        }

    if risk_percent <= 0:
        return {
            "allowed": False,
            "reason": "Risk percentage must be positive.",
        }

    risk_amount = (
        balance_usd * risk_percent / 100
    )

    risk_per_unit = (
        entry_price - stop_loss
    )

    if risk_per_unit <= 0:
        return {
            "allowed": False,
            "reason": "Invalid risk distance.",
        }

    quantity = (
        risk_amount / risk_per_unit
    )

    position_value = (
        quantity * entry_price
    )

    if position_value > max_position_usd:
        position_value = max_position_usd

        quantity = (
            position_value / entry_price
        )

    return {
        "allowed": True,
        "risk_amount_usd": round(
            risk_amount,
            2,
        ),
        "quantity": quantity,
        "position_value_usd": round(
            position_value,
            2,
        ),
        "risk_percent": risk_percent,
    }


def check_trade_limits(
    open_trades: int,
    max_open_trades: int,
    daily_loss_percent: float,
    max_daily_loss_percent: float,
) -> Dict:

    if open_trades >= max_open_trades:
        return {
            "allowed": False,
            "reason": "Maximum open trades reached.",
        }

    if daily_loss_percent >= max_daily_loss_percent:
        return {
            "allowed": False,
            "reason": "Maximum daily loss reached.",
        }

    return {
        "allowed": True,
        "reason": "Trade limits passed.",
    }


def validate_trade(
    entry_price: float,
    stop_loss: float,
    take_profit: float,
    min_risk_reward: float,
) -> Dict:

    if entry_price <= 0:
        return {
            "allowed": False,
            "reason": "Invalid entry price.",
        }

    if stop_loss >= entry_price:
        return {
            "allowed": False,
            "reason": "Invalid stop-loss.",
        }

    if take_profit <= entry_price:
        return {
            "allowed": False,
            "reason": "Take-profit must be above entry.",
        }

    risk = entry_price - stop_loss
    reward = take_profit - entry_price

    if risk <= 0:
        return {
            "allowed": False,
            "reason": "Invalid risk.",
        }

    risk_reward = reward / risk

    if risk_reward < min_risk_reward:
        return {
            "allowed": False,
            "reason": (
                f"Risk/reward {risk_reward:.2f} "
                f"is below minimum "
                f"{min_risk_reward:.2f}."
            ),
        }

    return {
        "allowed": True,
        "risk_reward": round(
            risk_reward,
            2,
        ),
        "reason": "Trade risk passed.",
  }
