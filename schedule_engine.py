import pandas as pd
import random

# زمان‌ها از ساعت 7:30 تا 18 با بازه‌های متنوع
TIME_SLOTS = [
    ("07:30", "09:00"), ("09:15", "10:45"), ("11:00", "12:30"),
    ("13:30", "15:00"), ("15:15", "16:45"), ("17:00", "18:30")
]
DAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه"]

def read_input_data(filename="input_data.xlsx"):
    teachers_df = pd.read_excel(filename, sheet_name="اساتید")
    courses_df = pd.read_excel(filename, sheet_name="دروس")
    rooms_df = pd.read_excel(filename, sheet_name="کلاس‌ها")
    return teachers_df, courses_df, rooms_df

def generate_random_schedule(courses, teachers, rooms):
    schedule = []
    for _, course in courses.iterrows():
        teacher = teachers[teachers["درس"] == course["نام"]].sample(1).iloc[0]
        possible_days = teacher["روزهای آزاد"].split(",")
        room = rooms.sample(1).iloc[0]
        day = random.choice(possible_days)
        time_slot = random.choice(TIME_SLOTS)
        schedule.append({
            "course": course["نام"],
            "teacher": teacher["نام"],
            "day": day,
            "time_slot": time_slot,
            "room": room["نام"]
        })
    return schedule

def has_conflict(schedule):
    seen = set()
    for item in schedule:
        key = (item["day"], item["time_slot"], item["room"])
        if key in seen:
            return True
        seen.add(key)
    return False

def evaluate_schedule(schedule):
    if has_conflict(schedule):
        return 0
    return len(schedule)

def run_genetic_algorithm():
    teachers_df, courses_df, rooms_df = read_input_data()
    best = None
    best_score = -1
    for _ in range(200):
        candidate = generate_random_schedule(courses_df, teachers_df, rooms_df)
        score = evaluate_schedule(candidate)
        if score > best_score:
            best = candidate
            best_score = score
    return best, best_score
