from storage.repository import items_exist


def should_alert(item):
    url = item["url"]
    return not items_exist(url)
