import requests
import time
import json
import os
from datetime import datetime


BASE_URL = "https://hacker-news.firebaseio.com/v0"

HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}


CATEGORIES = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


def get_story_ids():
    """Get the first 500 top HackerNews story IDs."""

    url = f"{BASE_URL}/topstories.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        story_ids = response.json()

        return story_ids[:500]

    except requests.RequestException as error:
        print("Error fetching story IDs:", error)
        return []


def get_story(story_id):
    """Get the details of one HackerNews story."""

    url = f"{BASE_URL}/item/{story_id}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        story = response.json()

        if not isinstance(story, dict):
            return None

        return story

    except requests.RequestException as error:
        print(f"Error fetching story {story_id}: {error}")
        return None


def find_category(title):
    """Assign the first matching category based on title keywords."""

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    return None


def create_story_record(story, category):
    """Create the seven fields required by the assignment."""

    return {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now().isoformat()
    }


def collect_stories():
    """Fetch the top 500 stories and collect up to 25 per category."""

    story_ids = get_story_ids()

    if not story_ids:
        print("No story IDs found.")
        return []

    # Fetch each story only once and keep the results.
    stories = []

    for story_id in story_ids:
        story = get_story(story_id)

        if story:
            stories.append(story)

    collected_stories = []

    # Process each category separately.
    # This makes the required category loop and delay clear.
    for category in CATEGORIES:

        category_count = 0

        for story in stories:

            # Stop after collecting 25 stories for this category.
            if category_count >= 25:
                break

            title = story.get("title", "")

            # Check whether this story belongs to this category.
            if find_category(title) != category:
                continue

            record = create_story_record(story, category)

            collected_stories.append(record)
            category_count += 1

        print(f"{category}: collected {category_count} stories")

        # Wait 2 seconds between category loops.
        time.sleep(2)

    return collected_stories


def save_to_json(stories):
    """Save collected stories to the required JSON file."""

    os.makedirs("data", exist_ok=True)

    date_string = datetime.now().strftime("%Y%m%d")

    filename = f"data/trends_{date_string}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            stories,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(f"Collected {len(stories)} stories.")
    print(f"Saved to {filename}")


if __name__ == "__main__":
    stories = collect_stories()
    save_to_json(stories)