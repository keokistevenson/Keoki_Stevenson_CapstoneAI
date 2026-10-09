# src/youtube_university/main.py
"""Orchestration: ask the user, call the LLM, call YouTube, print the result."""

import sys

from .llm import Curriculum, generate_curriculum
from .youtube import YOUTUBE_KEY, find_videos

QUERIES_PER_MODULE = 1   # each query costs 100 YouTube quota units; keep at 1 while developing

def ask_learner() -> dict:
    """Ask the user 4 questions and return their answers as a profile dict."""

    print("Hi, learner!")
    while True:                                   
        topic = input("What would you like to study? Be concise. ").strip()

        if topic == "":
            print("That's not a valid topic!\n")
        else:
            print('Thanks!\n')
            break

    while True:                                   
        level = input("How would you describe your expertise -- beginner, intermediate, or experienced? ").strip()

        newbie = "beginner, intro, starter, new, newbie"
        some = "some, intermediate"
        expert = "expert, advanced, experienced, pro"

        if len(level) < 3:
            print("I didn't get that.\n")
            continue

        level = level.lower()

        if level in newbie:
            level = "beginner"
            break

        if level in some:
            level = "intermediate"
            break

        if level in expert:
            level = "experienced"
            break

        print("That's not a valid experience level!\n")
    print('Got it!\n')

    while True:                                   
        goal = input("What's your goal? Why are you learning this? ").strip()
    
        if goal == "" or len(goal) <= 3:
            print("I didn't get that.\n")
        else:
            print('Cool!\n')
            break

    while True:                                   
        hours = input("How many hours do you plan to study a week? ").strip()
        try:
            if 1 <= int(hours) <= 40:
                print("Great!\n")
                break 
            else:
                print('Come on!\n')
        except ValueError:
            print("Give me numbers, please!  Between 1 and 40.\n")

    return {
        "topic": topic,
        "level": level,
        "goal":  goal,
        "hours_per_week": int(hours)
    }


def print_path(curriculum: Curriculum, results: list) -> None:
    """Print the finished learning path. `results` is a list of (module, videos) pairs."""
    # TODO: print the curriculum title, then for each (module, videos) pair:
    #   the module title, its objectives, and each video's title, channel, and url.
    #   If videos is empty, print "No videos found".

    print(f"\n\n==== {curriculum.title} ====\n")

    week_number = 0
    for module, videos in results:
        week_number += 1

        print(f"\nWeek {week_number}: {module.title}")
        for objective in module.objectives:
            print(f"    - {objective}")

        if len(videos) == 0:
            print("  No videos found")
        else:
            for video in videos:
                title = video["title"]       # video is a dict, so square brackets here
                channel = video["channel"]
                url = video["url"]
                print(f"\n      Watch: {title} ({channel})")
                print(f"      {url}")


def main() -> None:
    if not YOUTUBE_KEY:
        sys.exit("YOUTUBE_API_KEY is missing. Check your .env file.")
    try:
        profile = ask_learner()
        print("\nGenerating your curriculum (about a minute on CPU)...")
        curriculum = generate_curriculum(profile)
        seen_ids: set[str] = set()
        results = []
        for module in curriculum.modules:
            queries = module.search_queries[:QUERIES_PER_MODULE]
            videos = find_videos(queries, seen_ids)
            results.append((module, videos))

        print_path(curriculum, results)
    except RuntimeError as err:      # friendly messages raised by llm.py and youtube.py
        print(err)
    except KeyboardInterrupt:
        print("\nCancelled.")


if __name__ == "__main__":
    main()