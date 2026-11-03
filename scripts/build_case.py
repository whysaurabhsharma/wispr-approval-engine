"""Business case maths. All inputs visible; placeholders are reported, never hidden."""
def build(active_users, hours_saved_per_user_month, loaded_cost_per_hour, price_per_user_month, placeholders=()):
    value = active_users * hours_saved_per_user_month * loaded_cost_per_hour
    cost = active_users * price_per_user_month
    return {"monthly_value": value, "monthly_cost": cost, "ratio": round(value / cost, 1) if cost else None,
            "annual_value": value * 12, "annual_cost": cost * 12,
            "value_at_half_hours": value / 2, "placeholders": list(placeholders)}
if __name__ == "__main__":
    print(build(142, 4, 60, 18, placeholders=["hours_saved_per_user_month", "loaded_cost_per_hour"]))
