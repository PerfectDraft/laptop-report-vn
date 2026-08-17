import json
import os

ALL_ITEMS_PATH = "all_items.json"
USER_ALL_ITEMS_PATH = os.path.expanduser("~/laptop-report-19m/all_items.json")
USER_ALL_SCORED_PATH = os.path.expanduser("~/laptop-report-19m/raw/full/_ALL_scored.json")

def sync_dataset():
    # Load all_items.json
    with open(ALL_ITEMS_PATH, "r", encoding="utf-8") as f:
        existing_items = json.load(f)

    # Load converted GearVN items
    with open("gearvn_converted_scored.json", "r", encoding="utf-8") as f:
        gearvn_new = json.load(f)

    print(f"Existing items count: {len(existing_items)}")
    print(f"GearVN new/updated items count: {len(gearvn_new)}")

    # Index existing items by URL and name
    url_to_idx = {it.get("url"): idx for idx, it in enumerate(existing_items) if it.get("url")}
    name_to_idx = {it.get("name"): idx for idx, it in enumerate(existing_items) if it.get("name") and it.get("shop") == "gearvn"}

    updated_count = 0
    added_count = 0

    for item in gearvn_new:
        url = item.get("url")
        name = item.get("name")
        
        idx = url_to_idx.get(url)
        if idx is None and name:
            idx = name_to_idx.get(name)

        if idx is not None:
            # Update existing item
            existing_items[idx] = item
            updated_count += 1
        else:
            # Add new item
            existing_items.append(item)
            url_to_idx[url] = len(existing_items) - 1
            added_count += 1

    print(f"Synced GearVN items: {updated_count} updated, {added_count} newly added.")
    print(f"New total items count: {len(existing_items)}")

    # Save all_items.json in workspace
    with open(ALL_ITEMS_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_items, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved: {ALL_ITEMS_PATH}")

    # Save to user home if exists
    if os.path.exists(USER_ALL_ITEMS_PATH):
        with open(USER_ALL_ITEMS_PATH, "w", encoding="utf-8") as f:
            json.dump(existing_items, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved: {USER_ALL_ITEMS_PATH}")

    # Update _ALL_scored.json
    if os.path.exists(USER_ALL_SCORED_PATH):
        with open(USER_ALL_SCORED_PATH, "r", encoding="utf-8") as f:
            scored_data = json.load(f)
        scored_data["items"] = existing_items
        with open(USER_ALL_SCORED_PATH, "w", encoding="utf-8") as f:
            json.dump(scored_data, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved: {USER_ALL_SCORED_PATH}")

if __name__ == "__main__":
    sync_dataset()
