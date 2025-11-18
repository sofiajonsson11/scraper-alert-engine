from storage.repository import item_exists


def should_alert(data: dict) -> bool:
    """Example rule: send alert if temperature < 32°F or 'Snow' in description"""
    temp_value = "".join(filter(str.isdigit, data.get("temperature", "")))
    if temp_value and int(temp_value) < 32:
        return True
    if "snow" in data["description"].lower():
        return True
    return False
