import pandas as pd
import random
import datetime

# ----- تعریف زمان‌های مجاز -----
def generate_time_slots(start_time, end_time, durations):
    time_slots = []
    base_time = datetime.datetime.strptime(start_time, "%H:%M")
    end_time = datetime.datetime.strptime(end_time, "%H:%M")

    for duration in durations:
        slot_time = base_time
        while slot_time + datetime.timedelta(hours=duration) <= end_time:
            slot_start = slot_time.time()
            slot_end = (slot_time + datetime.timedelta(hours=duration)).time()
            time_slots.append((slot_start, slot_end, duration))
            slot_time += datetime.timedelta(minutes=30)

    return time_slots

time_slots = generate_time_slots("07:30", "18:00", [1.5, 3, 4])
weekdays = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه"]

# ----- تعریف ساختار ژن -----
class Gene:
    def __init__(self, course, teacher, day, time_slot, room):
        self.course = course
        self.teacher = teacher
        self.day = day
        self.time_slot = time_slot
        self.room = room

    def __repr__(self):
        return f"{self.course} | {self.teacher} | {self.day} | {self.time_slot[0]}-{self.time_slot[1]} | کلاس {self.room}"

# ----- خواندن فایل اکسل -----
df_teachers = pd.read_excel("input_data.xlsx", sheet_name="اساتید")
df_courses = pd.read_excel("input_data.xlsx", sheet_name="دروس")
df_rooms = pd.read_excel("input_data.xlsx", sheet_name="کلاس‌ها")

# ----- توابع کمکی -----
def get_teacher_available_days(teacher_name):
    match = df_teachers[df_teachers["نام استاد"] == teacher_name]
    if not match.empty:
        return match.iloc[0]["روزهای آزاد"].replace('،', ',').split(',')
    return []

def has_conflict(g1, g2):
    if g1.day != g2.day:
        return False
    start1, end1 = g1.time_slot[0], g1.time_slot[1]
    start2, end2 = g2.time_slot[0], g2.time_slot[1]
    overlap = max(start1, start2) < min(end1, end2)
    if overlap:
        return g1.teacher == g2.teacher or g1.room == g2.room
    return False

def evaluate_schedule(chromosome):
    score = 100
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            if has_conflict(chromosome[i], chromosome[j]):
                score -= 30
    for gene in chromosome:
        available_days = get_teacher_available_days(gene.teacher)
        if gene.day not in [d.strip() for d in available_days]:
            score -= 20
    return score

def create_initial_population(pop_size=10):
    population = []

    for _ in range(pop_size):
        chromosome = []
        for _, course_row in df_courses.iterrows():
            course_name = course_row["نام درس"]
            duration = course_row["مدت زمان"]
            teacher_row = df_teachers[df_teachers["نام درس"] == course_name]
            if teacher_row.empty:
                continue
            teacher_name = teacher_row.iloc[0]["نام استاد"]
            available_days = get_teacher_available_days(teacher_name)
            possible_slots = [slot for slot in time_slots if slot[2] == duration]
            if not available_days or not possible_slots:
                continue
            day = random.choice(available_days).strip()
            time_slot = random.choice(possible_slots)
            room = random.choice(df_rooms["شماره کلاس"].tolist())
            gene = Gene(course_name, teacher_name, day, time_slot, room)
            chromosome.append(gene)
        population.append(chromosome)
    return population

def crossover(parent1, parent2):
    mid = len(parent1) // 2
    return parent1[:mid] + parent2[mid:]

def mutate(chromosome, mutation_rate=0.1):
    new_chromosome = []
    for gene in chromosome:
        if random.random() < mutation_rate:
            new_day = random.choice(weekdays)
            duration = gene.time_slot[2]
            valid_slots = [slot for slot in time_slots if slot[2] == duration]
            new_time_slot = random.choice(valid_slots)
            new_room = random.choice(df_rooms["شماره کلاس"].tolist())
            mutated_gene = Gene(gene.course, gene.teacher, new_day, new_time_slot, new_room)
            new_chromosome.append(mutated_gene)
        else:
            new_chromosome.append(gene)
    return new_chromosome

def run_genetic_algorithm(generations=30, population_size=10, elite_size=2, mutation_rate=0.1):
    population = create_initial_population(population_size)
    for _ in range(generations):
        evaluated = [(chrom, evaluate_schedule(chrom)) for chrom in population]
        evaluated.sort(key=lambda x: x[1], reverse=True)
        elites = [chrom for chrom, _ in evaluated[:elite_size]]
        next_gen = elites.copy()
        while len(next_gen) < population_size:
            parent1 = random.choice(elites)
            parent2 = random.choice(elites)
            child = crossover(parent1, parent2)
            mutated_child = mutate(child, mutation_rate)
            next_gen.append(mutated_child)
        population = next_gen
    final_evaluated = [(chrom, evaluate_schedule(chrom)) for chrom in population]
    final_evaluated.sort(key=lambda x: x[1], reverse=True)
    return final_evaluated[0]

# اجرای الگوریتم و چاپ برنامه نهایی
best_schedule, score = run_genetic_algorithm()
print(f"📘 بهترین برنامه با امتیاز {score}:\n")
for gene in best_schedule:
    print(gene)
