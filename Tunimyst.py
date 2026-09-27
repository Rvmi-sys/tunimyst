import pygame
import sys
import random
import math

pygame.init()

# === Windowed Mode Setup (No Stretching) ===
WIDTH, HEIGHT = 1280, 720  # Fixed size window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Removed FULLSCREEN
pygame.display.set_caption("Tunimyst")
# === Colors & Fonts ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (193, 154, 107)
SCORE_BOX_COLOR = (240, 210, 150)
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 42)

try:
    pygame.mixer.music.load("Sound_Effect.mp3")  # Replace with your sound file e.g., 'theme.wav'
    pygame.mixer.music.play(-1)  # -1 means loop forever
except:
    print("⚠️ Sound file not found or invalid.")


# === Background Image Safe Load ===
try:
    original_bg = pygame.image.load("assets/background.jpeg")
    background = pygame.transform.smoothscale(original_bg, (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BLACK)

# === Progressive Reveal Backgrounds for Level 1 ===
try:
    bg_blur1 = pygame.transform.smoothscale(pygame.image.load("assets/bg_blur1.png"), (WIDTH, HEIGHT))
    bg_blur2 = pygame.transform.smoothscale(pygame.image.load("assets/bg_blur2.png"), (WIDTH, HEIGHT))
    bg_blur3 = pygame.transform.smoothscale(pygame.image.load("assets/bg_blur3.png"), (WIDTH, HEIGHT))
    bg_bonus1 = pygame.transform.smoothscale(pygame.image.load("assets/bg_clear.png"), (WIDTH, HEIGHT))  # ✅ NEW for Bonus Level 1
except:
    bg_blur1 = background
    bg_blur2 = background
    bg_blur3 = background
    bg_bonus1 = background

# === Level 2 Personnage Guessing Backgrounds (Progressive) ===
# === Level 2 Personnage Guessing Backgrounds (Progressive) ===
try:
    nidhal_blur1 = pygame.transform.smoothscale(pygame.image.load("assets/Nidhal_Saadi2.png"), (WIDTH, HEIGHT))  # First image unavailable in this export
    nidhal_blur2 = pygame.transform.smoothscale(pygame.image.load("assets/Nidhal_Saadi2.png"), (WIDTH, HEIGHT))
    nidhal_clear = pygame.transform.smoothscale(pygame.image.load("assets/Nidhal_Saadi3.png"), (WIDTH, HEIGHT))
    nidhal_bonus = pygame.transform.smoothscale(pygame.image.load("assets/Nidhal_Saadi4.png"), (WIDTH, HEIGHT))  # ✅ NEW for Bonus Level 2
except:
    nidhal_blur1 = background
    nidhal_blur2 = background
    nidhal_clear = background
    nidhal_bonus = background

# === Level 3 Personnage Guessing Backgrounds: Ons Jabeur ===
try:
    ons_blur1 = pygame.transform.smoothscale(pygame.image.load("assets/Ons-Jabeur_1.png"), (WIDTH, HEIGHT))
    ons_blur2 = pygame.transform.smoothscale(pygame.image.load("assets/Ons-Jabeur_2.png"), (WIDTH, HEIGHT))
    ons_clear = pygame.transform.smoothscale(pygame.image.load("assets/Ons-Jabeur_3.png"), (WIDTH, HEIGHT))
    ons_bonus = pygame.transform.smoothscale(pygame.image.load("assets/Ons-Jabeur_Clear.png"), (WIDTH, HEIGHT))
except:
    print("⚠️ Ons Jabeur images not found, using default background.")
    ons_blur1 = background
    ons_blur2 = background
    ons_clear = background
    ons_bonus = background

# === Game Data ===
levels = ["Easy", "Medium", "Hard"]

# === Questions Level 1 ===
question_sets_level1 = {
    "Easy": [
        {"question": "What is the capital city of Tunisia?", "options": ["Sousse", "Tunis", "Monastir", "Bizerte"], "answer": "Tunis"},
        {"question": "Which sea borders Tunisia to the north?", "options": ["Atlantic Ocean", "Red Sea", "Mediterranean Sea", "Arabian Sea"], "answer": "Mediterranean Sea"}
    ],
    "Medium": [
        {"question": "Which ancient civilization founded Carthage?", "options": ["Greeks", "Phoenicians", "Romans", "Egyptians"], "answer": "Phoenicians"},
        {"question": "Who was the first president of independent Tunisia?", "options": ["Ben Ali", "Ghannouchi", "Bourguiba", "Marzouki"], "answer": "Bourguiba"}
    ],
    "Hard": [
        {"question": "Which famous Tunisian film won the Palme d'Or at Cannes in 1994?", "options": ["The Silences of the Palace", "Bab'Aziz", "Halfaouine", "Man of Ashes"], "answer": "The Silences of the Palace"},
        {"question": "Which famous Tunisian scholar wrote the 'Muqaddimah'?", "options": ["Avicenna", "Ibn Khaldun", "Al-Khwarizmi", "Farabi"], "answer": "Ibn Khaldun"}
    ]
}
bonus_question = {
    "question": "Who is this?","options": ["Habib Bourguiba", "Kais Saied", "Zine El Abidine Ben Ali", "Rached Ghannouchi"],"answer": "Kais Saied"
}


# === Questions Level 2 ===
question_sets_level2 = {
    "Easy": [
        {"question": "Tunisia is located on which continent?", "options": ["Europe", "Asia", "Africa", "South America"], "answer": "Africa"},
        {"question": "What is the famous spicy Tunisian sauce made from chili peppers?", "options": ["Ketchup", "Harissa", "Mustard", "Sriracha"], "answer": "Harissa"}
    ],
    "Medium": [
        {"question": "Which ancient civilization founded Carthage?", "options": ["Greeks", "Romans", "Phoenicians", "Egyptians"], "answer": "Phoenicians"},
        {"question": "What is the highest mountain in Tunisia?", "options": ["Mount Kilimanjaro", "Jebel Zaghouan", "Jebel Chaambi", "Jebel Ressas"], "answer": "Jebel Chaambi"}
    ],
    "Hard": [
        {"question": "In what year was the Code of Personal Status introduced in Tunisia?", "options": ["1947", "1956", "1961", "1975"], "answer": "1956"},
        {"question": "What does 'Ifriqiya' refer to historically?", "options": ["Ancient name for Libya", "Ancient region covering Tunisia", "Ancient Moroccan city", "A Berber tribe"], "answer": "Ancient region covering Tunisia"}
    ],
    "Bonus": [  # ✅ NEW BONUS CATEGORY
        {
            "question": "Who is this famous Tunisian actor?",
            "options": ["Nassim Ziadia", "Yassine Ben Gamra", "Kamel Touati", "Nidhal Saadi"],
            "answer": "Nidhal Saadi"
        }
    ]
}

# === Questions Level 3 ===
# === Questions Level 3 ===
question_sets_level3 = {
    "Easy": [
        {"question": "What is the national currency of Tunisia?", "options": ["Euro", "Dinar", "Franc", "Dirham"], "answer": "Dinar"},
        {"question": "Which city is famous for its white houses and blue windows in Tunisia?", "options": ["Sidi Bou Said", "Djerba", "Mahdia", "Tozeur"], "answer": "Sidi Bou Said"}
    ],
    "Medium": [
        {
            "question": "Which Tunisian tennis player became the first Arab woman \nin history to reach a Grand Slam final?",
            "options": ["Selima Sfar", "Ons Jabeur", "Malek Jaziri", "Chiraz Bechri"],
            "answer": "Ons Jabeur"
        },
        {"question": "What is the name of the famous amphitheater in El Djem?", "options": ["Colosseum of Tunisia", "Carthage Arena", "Arena of Sousse", "Africa Stadium"], "answer": "Colosseum of Tunisia"}
    ],
    "Hard": [
        {"question": "Who wrote the famous book “Our Women in the Sharia and Society”?", "options": ["Mahmoud Messadi", "Tahar Haddad", "Habib Bourguiba", "Hédi Bouraoui"], "answer": "Tahar Haddad"},
        {"question": "The ancient city of Kerkouane is special because it is:", "options": ["A Roman fortress", "An untouched Punic city", "A Berber cave", "A Phoenician cemetery"], "answer": "An untouched Punic city"}
    ],
    "Bonus": [  # ✅ NEW Bonus Question for Level 3
        {
            "question": "Who is this famous Tunisian tennis player?",
            "options": ["Ons Jabeur", "Selima Sfar", "Chiraz Bechri", "Malek Jaziri"],
            "answer": "Ons Jabeur"
        }
    ]
}

# === Questions Level 4 ===
question_sets_level4 = {
    "Easy": [
        {"question": "What colors are on the Tunisian flag?", "options": ["Green and Yellow", "Black and Red", "Blue and White", "Red and White"], "answer": "Red and White"},
        {"question": "What is the official language of Tunisia?", "options": ["English", "French", "Arabic", "Italian"], "answer": "Arabic"}
    ],
    "Medium": [
        {"question": "In which year did Tunisia gain independence from France?", "options": ["1945", "1950", "1956", "1965"], "answer": "1956"},
        {"question": "What is the name of Tunisia's largest desert?", "options": ["Sahara", "Grand Erg Oriental", "Kalahari", "Nefta Plains"], "answer": "Grand Erg Oriental"}
    ],
    "Hard": [
        {"question": "Which Tunisian poet is known for “Ila Tifl Lam Ya’ti”?", "options": ["Abu al-Qasim al-Shabbi", "Béchir Khraief", "Tahar Bekri", "Mustapha Khraïef"], "answer": "Abu al-Qasim al-Shabbi"},
        {"question": "What is the historic Medina of Tunis recognized by UNESCO for?", "options": ["Its religious tolerance", "Its Roman ruins", "Its Islamic architecture and heritage", "Its French colonial buildings"], "answer": "Its Islamic architecture and heritage"}
    ]
}



# === Game State Variables ===
current_level_index = 0
current_question = None
question_pool = []
correct_streak = 0
current_options = []
question_sets = {}

game_state = "menu"
sound_on = True
show_result = False
result_timer = 0
last_answer_correct = False
score = 0
is_bonus_question = False
level_intro_timer = 0
score_pulse_time = 0
score_increment = 0
score_increment_timer = 0
SCORE_INCREMENT_DURATION = 1500

total_questions = 0
current_question_number = 0
question_timer_start = 0
question_time_limit = 15  # This changes with difficulty

level_times = []  # 🆕 List to store time per level
level_start_time = 0
answered_in_level = 0
questions_in_level = 0       # ✅ Track how many questions asked in the current level
background_stage = 0         # ✅ Which background should be used for Level 1



# === Drawing Functions ===
def draw_text_centered(text, center_x, center_y, font=font, color=BLACK, y_offset=5):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(center_x, center_y + y_offset))
    screen.blit(surface, rect)

def draw_wrapped_text(text, x, y, w, h, font, color=WHITE):
    words = text.split(' ')
    lines = []
    line = ""
    for word in words:
        if font.size(line + word)[0] > w - 20:
            lines.append(line)
            line = word + " "
        else:
            line += word + " "
    lines.append(line)
    total_height = len(lines) * font.get_linesize()
    start_y = y + (h - total_height) // 2 + 5
    for i, l in enumerate(lines):
        txt_surface = font.render(l.strip(), True, color)
        txt_rect = txt_surface.get_rect(center=(x + w // 2, start_y + i * font.get_linesize()))
        screen.blit(txt_surface, txt_rect)

def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = x < mouse[0] < x + w and y < mouse[1] < y + h
    color = tuple(min(255, c + 30) for c in BUTTON_COLOR) if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    draw_wrapped_text(text, x, y, w, h, font)
    if hovered and click[0] == 1 and action:
        pygame.time.delay(200)
        action()
def draw_scoreboard():
    # Draw the background for the scoreboard screen
    screen.blit(background, (0, 0))  # Make sure to display the background

    # Title text for the scoreboard
    draw_text_centered("🏆 Scoreboard", WIDTH // 2, 60, big_font, WHITE)

    # Check if there's any data to display in the scoreboard
    if len(level_times) == 0:
        draw_text_centered("No data yet", WIDTH // 2, 160, font, WHITE)
    else:
        # Header for the scoreboard table
        draw_text_centered("Level | Time (s) | Score", WIDTH // 2, 130, font, WHITE)
        pygame.draw.line(screen, WHITE, (WIDTH // 2 - 200), 140, (WIDTH // 2 + 200), 140)  # Draw a line under the header

        y = 150
        # Sort the levels by time for the leaderboard
        sorted_levels = sorted(level_times, key=lambda x: x["time"])

        # Display each level's data in rows
        for entry in sorted_levels:
            level = entry["level"]
            time = entry["time"]
            answered = entry["answered"]  # Number of correct answers
            # Format the data into a table row
            text = f"Level {level} – Time: {time}s – Score: {answered}/7"
            draw_text_centered(text, WIDTH // 2, y, font, WHITE)
            y += 50  # Move down for the next row

    # Draw the Back button at the bottom
    draw_button("Back", WIDTH // 2 - 100, HEIGHT - 80, 200, 50, lambda: set_game_state("menu"))


def draw_score_box():
    global score_pulse_time
    box_w = 160
    box_h = 70
    x = WIDTH - box_w - 40
    y = 40
    pygame.draw.rect(screen, SCORE_BOX_COLOR, (x, y, box_w, box_h), border_radius=12)
    center_x = x + box_w / 2
    center_y = y + box_h / 2
    now = pygame.time.get_ticks()
    if score_increment > 0 and now - score_increment_timer < SCORE_INCREMENT_DURATION:
        draw_text_centered(f"+{score_increment}", center_x, center_y - 15, font, BLACK)
    draw_text_centered(f"Score: {score}", center_x, center_y, font, BLACK)

def draw_question_number_box():
    box_w = 160
    box_h = 50
    x = WIDTH - box_w - 40
    y = 120
    pygame.draw.rect(screen, SCORE_BOX_COLOR, (x, y, box_w, box_h), border_radius=12)
    center_x = x + box_w / 2
    center_y = y + box_h / 2

    if game_state == "game" or show_result:
        # Adjust max question number if we're currently on a bonus question
        max_display = total_questions + 1 if is_bonus_question else total_questions
        draw_text_centered(f"{current_question_number} / {max_display}", center_x, center_y, font, BLACK)

def draw_timer_box():
    box_w = 160
    box_h = 70
    x = 40  # Top-left
    y = 40
    pygame.draw.rect(screen, SCORE_BOX_COLOR, (x, y, box_w, box_h), border_radius=12)
    center_x = x + box_w / 2
    center_y = y + box_h / 2
    time_passed = (pygame.time.get_ticks() - question_timer_start) / 1000
    time_left = max(0, math.ceil(question_time_limit - time_passed))
    if game_state == "game" or show_result:
        draw_text_centered(f"Timer", center_x, center_y - 15, font, BLACK)
        draw_text_centered(f"{time_left} sec", center_x, center_y + 15, font, BLACK)

def draw_chronometer_box():
    box_w = 160
    box_h = 70
    x = 40  # Same X as timer
    y = 130  # Just below the timer box
    pygame.draw.rect(screen, SCORE_BOX_COLOR, (x, y, box_w, box_h), border_radius=12)
    center_x = x + box_w // 2
    center_y = y + box_h // 2
    if game_state == "game" or show_result:
        time_elapsed = (pygame.time.get_ticks() - level_start_time) // 1000
        draw_text_centered("Clock", center_x, center_y - 15, font, BLACK)
        draw_text_centered(f"{time_elapsed} sec", center_x, center_y + 15, font, BLACK)


# === Game Logic ===
def prepare_question_pool():
    global question_pool, total_questions, current_question_number
    question_pool = []
    for level_name in levels:
        questions = question_sets[level_name][:]
        random.shuffle(questions)
        question_pool += questions
    total_questions = len(question_pool)
    current_question_number = 0

def load_next_question():
    global current_question, question_pool, current_options, current_question_number
    global question_timer_start, question_time_limit
    global questions_in_level, background_stage

    current_question = question_pool.pop(0)
    current_options = current_question["options"][:]
    random.shuffle(current_options)
    current_question_number += 1
    question_timer_start = pygame.time.get_ticks()

    difficulty = ""
    for level_name in levels:
        if current_question in question_sets[level_name]:
            difficulty = level_name
            break

        if difficulty == "Easy":
            question_time_limit = 10
        elif difficulty == "Medium":
            question_time_limit = 15
    else:
        question_time_limit = 20

    # ✅ Properly increment question count for background stage tracking
    questions_in_level += 1

    if current_level_index == 0:  # Level 1
        if questions_in_level <= 2:
            background_stage = 0
        elif questions_in_level <= 4:
            background_stage = 1
        else:
            background_stage = 2

    elif current_level_index == 1:  # Level 2 (Guessing the personnage)
        if questions_in_level <= 2:
            background_stage = 0
        elif questions_in_level <= 4:
            background_stage = 1
        else:
            background_stage = 2

    elif current_level_index == 2:  # Level 3 (Ons Jabeur Reveal)
        if questions_in_level <= 2:
            background_stage = 0
        elif questions_in_level <= 4:
            background_stage = 1
        else:
            background_stage = 2


def handle_answer(selected):
    global show_result, result_timer, last_answer_correct, score, score_increment, score_increment_timer
    last_answer_correct = (selected == current_question["answer"])

    if last_answer_correct:
        # Check if it's the bonus question
        if is_bonus_question:
            added = 50  # Bonus question gives 50 points
        else:
            # Determine question difficulty for regular questions
            difficulty = ""
            for level_name in levels:
                if current_question in question_sets[level_name]:
                    difficulty = level_name
                    break

            # Correct scoring logic for regular questions
            if difficulty == "Easy":
                added = 10
            elif difficulty == "Medium":
                added = 20
            else:  # Hard
                added = 30

        score += added
        score_increment = added
        score_increment_timer = pygame.time.get_ticks()
    else:
        score_increment = 0

    show_result = True
    result_timer = pygame.time.get_ticks()



def check_result_and_continue():
    global show_result, correct_streak, current_level_index, game_state
    global question_sets, level_intro_timer, level_start_time, level_times, score
    global questions_in_level, background_stage, is_bonus_question, question_pool  # ✅ include these

    show_result = False

    if last_answer_correct:
        correct_streak += 1

        # === BONUS ROUND CONDITION ===
        if correct_streak >= 6 and current_level_index == 0 and not is_bonus_question:
            # 👉 Inject bonus question
            question_pool.insert(0, bonus_question)
            is_bonus_question = True
            correct_streak = 0  # Reset streak for bonus
            load_next_question()
            return
        elif correct_streak >= 6 and current_level_index == 1 and not is_bonus_question:
            question_pool.insert(0, question_sets_level2["Bonus"][0])
            is_bonus_question = True
            correct_streak = 0
            load_next_question()
            return
        elif correct_streak >= 6 and current_level_index == 2 and not is_bonus_question:
            question_pool.insert(0, question_sets_level3["Bonus"][0])
            is_bonus_question = True
            correct_streak = 0
            load_next_question()
            return


        # === BONUS ROUND CORRECT ===
                # === BONUS ROUND CORRECT ===
                # === BONUS ROUND CORRECT ===
                # === BONUS ROUND CORRECT ===
        # === BONUS ROUND CORRECT ===
        if is_bonus_question:
            score += 50  # ✅ Add 50 points for correct bonus answer
            is_bonus_question = False  # Reset bonus flag after the bonus question is answered
            correct_streak = 0
            questions_in_level = 0
            background_stage = 0

            # Calculate the elapsed time for this level
            elapsed_time = (pygame.time.get_ticks() - level_start_time) // 1000  # Time in seconds
            level_times.append({
            "level": current_level_index + 1,
            "time": elapsed_time,  # Store time for this level
            "answered": 6  # For bonus question, we assume all 6 questions are answered correctly
            })

            current_level_index += 1
            score = 0  # Reset score per level (optional, remove if keeping total score)


            # 🔁 Load the next level
            if current_level_index == 1:
                question_sets = question_sets_level2
            elif current_level_index == 2:
                question_sets = question_sets_level3
            elif current_level_index == 3:
                question_sets = question_sets_level4
            else:
                game_state = "win"
                return

            prepare_question_pool()
            level_intro_timer = pygame.time.get_ticks()
            level_start_time = pygame.time.get_ticks()
            game_state = "level_intro"
            return





        # === Continue normally if not a bonus question ===
        load_next_question()

    else:
        # === WRONG ANSWER — RESET LEVEL ===
        game_state = "lost"









def start_game():
    global current_level_index, correct_streak, score, score_increment, score_increment_timer
    global game_state, level_intro_timer, question_sets, level_times
    global level_start_time, answered_in_level  # ✅ NEW

    current_level_index = 0
    correct_streak = 0
    score = 0
    score_increment = 0
    score_increment_timer = 0
    level_times = []  # to store level times for scoreboard
    question_sets = question_sets_level1  # Always start with level 1 questions
    prepare_question_pool()

    # Reset game state
    game_state = "level_intro"
    level_intro_timer = pygame.time.get_ticks()
    level_start_time = pygame.time.get_ticks()




def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        pygame.mixer.music.unpause()  # Resume sound
    else:
        pygame.mixer.music.pause()    # Mute sound

def set_game_state(state):
    global game_state
    game_state = state



# === Main Loop ===
def main():
    global game_state, show_result, result_timer
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # === GAME STATE: MENU ===
        if game_state == "menu":
            screen.blit(background, (0, 0))
            draw_text_centered("Welcome to Tunimyst", WIDTH // 2, 70, big_font, WHITE)

            button_width = 200
            button_height = 60
            gap = 40

            start_x = (WIDTH - (button_width * 3 + gap * 2)) // 2
            y_pos = HEIGHT - 100

            draw_button("Start", start_x, y_pos, button_width, button_height, start_game)
            draw_button("Scoreboard", start_x + button_width + gap, y_pos, button_width, button_height, lambda: set_game_state("scoreboard"))
            draw_button("Sound On" if sound_on else "Sound Off", start_x + (button_width + gap) * 2, y_pos, button_width, button_height, toggle_sound)

        # === GAME STATE: LEVEL INTRO ===
        elif game_state == "level_intro":
            screen.blit(background, (0, 0))
            draw_text_centered(f"LEVEL {current_level_index + 1}", WIDTH // 2, HEIGHT // 2, big_font, WHITE)
            if pygame.time.get_ticks() - level_intro_timer > 2000:
                load_next_question()
                game_state = "game"

        # === GAME STATE: MAIN QUIZ ===
        elif game_state == "game":
            time_passed = (pygame.time.get_ticks() - question_timer_start) / 1000
            if not show_result and time_passed >= question_time_limit:
                game_state = "time_over"

            # === BACKGROUND LOGIC ===
            if current_level_index == 0:
                if is_bonus_question:
                    screen.blit(bg_bonus1, (0, 0))
                elif background_stage == 0:
                    screen.blit(bg_blur1, (0, 0))
                elif background_stage == 1:
                    screen.blit(bg_blur2, (0, 0))
                elif background_stage == 2:
                    screen.blit(bg_blur3, (0, 0))

            elif current_level_index == 1:
                if is_bonus_question:
                    screen.blit(nidhal_bonus, (0, 0))
                elif background_stage == 0:
                    screen.blit(nidhal_blur1, (0, 0))
                elif background_stage == 1:
                    screen.blit(nidhal_blur2, (0, 0))
                elif background_stage == 2:
                    screen.blit(nidhal_clear, (0, 0))

            elif current_level_index == 2:
                if is_bonus_question:
                    screen.blit(ons_bonus, (0, 0))
                elif background_stage == 0:
                    screen.blit(ons_blur1, (0, 0))
                elif background_stage == 1:
                    screen.blit(ons_blur2, (0, 0))
                elif background_stage == 2:
                    screen.blit(ons_clear, (0, 0))

            else:
                screen.blit(background, (0, 0))

            # === DISPLAY QUESTION & INFO BOXES ===
            if show_result:
                draw_text_centered("Correct!" if last_answer_correct else "Wrong", WIDTH // 2, 160, big_font, WHITE)
            else:
                draw_text_centered(current_question["question"], WIDTH // 2, 100, big_font, WHITE)

            draw_score_box()
            draw_question_number_box()
            draw_timer_box()
            draw_chronometer_box()

            # === ANSWER OPTIONS ===
            if not show_result:
                labels = ["A", "B", "C", "D"]
                button_start_y = HEIGHT - 320
                for i, option in enumerate(current_options):
                    label = f"Option {labels[i]}: {option}"
                    draw_button(label, (WIDTH - 600) // 2, button_start_y + i * 75, 600, 60, lambda opt=option: handle_answer(opt))
            else:
                if pygame.time.get_ticks() - result_timer > 2000:
                    check_result_and_continue()

        # === GAME STATE: LOST ===
        elif game_state == "lost":
            screen.blit(background, (0, 0))
            draw_text_centered("YOU LOST", WIDTH // 2, 300, big_font, WHITE)
            draw_button("Try Again", (WIDTH - 200) // 2, 400, 200, 60, lambda: set_game_state("menu"))
            draw_score_box()
            draw_question_number_box()
            draw_timer_box()

        # === GAME STATE: TIME OVER ===
        elif game_state == "time_over":
            screen.blit(background, (0, 0))
            draw_text_centered("TIME OVER", WIDTH // 2, 250, big_font, WHITE)
            draw_text_centered("YOU LOST", WIDTH // 2, 320, big_font, WHITE)
            draw_button("Try Again", (WIDTH - 200) // 2, 400, 200, 60, lambda: set_game_state("menu"))
            draw_score_box()
            draw_question_number_box()
            draw_timer_box()

        # === GAME STATE: WIN ===
        elif game_state == "win":
            screen.blit(background, (0, 0))
            draw_text_centered("Congratulations! You completed the Quiz!", WIDTH // 2, 300, big_font, WHITE)
            draw_button("Play Again", (WIDTH - 200) // 2, 400, 200, 60, start_game)
            draw_score_box()
            draw_question_number_box()
            draw_timer_box()

        # === GAME STATE: SCOREBOARD ===
        elif game_state == "scoreboard":
            draw_scoreboard()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
