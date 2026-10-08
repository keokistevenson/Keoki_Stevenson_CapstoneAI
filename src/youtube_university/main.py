# src/youtube_university/main.py
"""Orchestration: ask the user, call the LLM, call YouTube, print the result."""
from .llm import generate_curriculum


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



def main() -> None:        # TEMPORARY: we replace this in Checkpoint 5
    profile = ask_learner()
    print("\nGenerating your curriculum (about a minute on CPU)...")
    try:
        curriculum = generate_curriculum(profile)
    except RuntimeError as err:
        print(err)
        return
    print(curriculum.model_dump_json(indent=2))


if __name__ == "__main__":
    main()