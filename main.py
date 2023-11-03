WORD_SIZE = 5
WORDS = {"Termo": 1, "Dueto": 2, "Quarteto": 4}
TURNS = {"Termo": 7, "Dueto": 8, "Quarteto": 10}
PRINT_N_VALID_SOLUTIONS = 20

COLOR = {"White": "\33[0m", "Red": "\33[91m", "Green": "\33[92m", "Yellow": "\33[93m", "Blue": "\33[94m", "Word": "\33[92m\33[4m"}
BULLET = ['🟠', '🔵', '🟣', '🟤']

LETTER_DICT = {"a": "a", "b": "b", "c": "c", "d": "d", "e": "e", "f": "f", "g": "g",
                "h": "h", "i": "i", "j": "j", "k": "k", "l": "l", "m": "m", "n": "n",
                "o": "o", "p": "p", "q": "q", "r": "r", "s": "s", "t": "t", "u": "u",
                "v": "v", "w": "w", "x": "x", "y": "y", "z": "z", "á": "a", "à": "a",
                "â": "a", "ã": "a", "é": "e", "ê": "e", "è": "e", "í": "i", "ï": "i",
                "ó": "o", "ô": "o", "õ": "o", "ú": "u", "û": "u", "ü": "u", "ç": "c"}

def product(array):
    if not array:
        yield()
    else:
        for x in array[0]:
            for y in product(array[1:]):
                yield(x, ) + y

def convert_alphanum(word):
    word = word.lower()
    for i, v in enumerate(word):
        word = word[:i] + LETTER_DICT[v] + word[i + 1:]
    return word

def check_valid_solutions(words, guess, response):
    for pos, _ in enumerate(response):
        num, letter = response[pos], guess[pos]
        repeated_letters = [(i, l) for i, l in enumerate(guess) if (response[i] == 1 or response[i] == 2)]
        if num == 0:
            words = [x for x in words if letter not in x or letter in [l for (_, l) in repeated_letters]]
        if num == 1:
            words = [x for x in words if x[pos] == letter]
        if num == 2:
            words = [x for x in words if (letter in x) and (x[pos] != letter)]
    return words

def max_guess(valid_guesses, valid_solutions):
    if len(valid_solutions) == 1:
        return valid_solutions[0]
    possible_responses = list(product([[0, 1, 2]] * WORD_SIZE))
    higher_score = float("inf")
    max_guess = None
    for _, v in enumerate(valid_guesses):
        score = 0
        for response in possible_responses:
            if response != (1,) * WORD_SIZE:
                solutions = check_valid_solutions(valid_solutions, v, response)
                score += pow(len(solutions), 2) / len(valid_solutions)
        if score < higher_score:
            higher_score = score
            max_guess = v
    return max_guess, higher_score

def print_game_modes():
    print(f"\n🟢 {COLOR['Green']} 1 - Termo {COLOR['White']}")
    print(f"🟡 {COLOR['Yellow']} 2 - Dueto {COLOR['White']}")
    print(f"🔴 {COLOR['Red']} 3 - Quarteto {COLOR['White']}")

def color_response(word, response):
    colored_response = ""
    if not word:
        colored_response = "🟩🟩🟩🟩🟩"
    else:
        for x in response:
            if x == 0:
                colored_response += "🔳"
            elif x == 1:
                colored_response += "🟩"
            elif x == 2:
                colored_response += "🟨"

    return colored_response

def update_conditions(words):
    return [words[i] for i in range(WORDS[game_mode])]

def check_end(words):
    return any(words[i] for i in range(WORDS[game_mode]))
            
if __name__ == "__main__":
    
    ###############     CHOOSE GAME MODE     ###############

    print_game_modes()
    
    while True:
        mode = input(f"\nEscolha o modo de jogo: {COLOR['Blue']}")
        print(f"{COLOR['White']}", end = "")
        if mode.isdigit():
            mode = int(mode)
            if mode in range(1, 4):
                game_mode = list(TURNS.keys())[mode-1]
                break
        else:
            mode = mode.title()
            if mode in TURNS.keys():
                game_mode = mode
                mode = int(list(TURNS.keys()).index(game_mode)+1)
                break

    turns = TURNS[game_mode]
    print(f"\n{COLOR['Blue']}{game_mode} iniciado! {COLOR['White']}")

    ###############     SET UP WORDS     ###############

    guesses = []
    solutions = []

    with open("solutions") as file:
        for line in file:
            solutions.append(line.rstrip())

    alphanum_solutions = [convert_alphanum(w) for w in solutions]
    valid_solutions = []

    for i in range(WORDS[game_mode]):
        valid_solutions.append(alphanum_solutions)
    
    max_score = float('-inf')

    ###############     START SOLVING     ###############  

    for turn in range(1, turns):
        if turn == 1:
            words = [True,] * WORDS[game_mode]
            post_find = False
            post_list = []
            
            while True:
                guess = input(f"\nEscolha a palavra inicial: {COLOR['Yellow']}")
                if len(guess) == WORD_SIZE and guess.isalpha():
                    break
                else:
                    print(f"{COLOR['Red']}A palavra deve possuir {WORD_SIZE} letras. {COLOR['White']}")
            guess = convert_alphanum(guess)
            print(f"{COLOR['White']}Usou a palavra: {COLOR['Word']}{guess}{COLOR['White']}\n")
            print("❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
        else:
            if not post_find:
                possible_guesses = []
                guesses_score = []
                if game_mode == "Termo": # Termo
                    guess, _ = max_guess(alphanum_solutions, valid_solutions[0])
                else: # Dueto ou Quarteto
                    for i in range(WORDS[game_mode]):
                        if words[i]:
                            x_guess, x_score = max_guess(alphanum_solutions, valid_solutions[i])
                            possible_guesses.append(x_guess)
                            guesses_score.append(x_score)
                            guess = x_guess
                    conditions = update_conditions(words)
                    for i in range(WORDS[game_mode]):
                        if conditions[i] and guesses_score[i] > max_score:
                            max_score = guesses_score[i]
                            guess = possible_guesses[i]
            else:
                guess = post_list.pop(0)
            print(f"Use a palavra: {COLOR['Yellow']}{guess}{COLOR['White']}.")

        if not post_list:
            post_find = False
        admit = True

        while True:
            if not admit:
                print(f"Use a palavra: {COLOR['Yellow']}guess{COLOR['White']}.")
            responses = []
            for i, word in enumerate(words):
                if word:
                    response = input(f"{COLOR['White']}{BULLET[i]} [{i+1}] Palavra ➜ Resposta do termo: {COLOR['Red']}")
                    if len(response) != WORD_SIZE or not response.isdigit():
                        print(f"{COLOR['Red']}A resposta deve possuir {WORD_SIZE} números entre [0, 1, 2].{COLOR['White']}\n")
                        break
                    elif any(int(x) not in [0, 1, 2] for x in response):
                        print(f"{COLOR['White']}❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
                        break
                else:
                    response = "00000"
                responses.append([int(x) for x in response])
            else:
                admit = True
                break

        print()
        print(f"{COLOR['White']}", end = "")

        for i in range(WORDS[game_mode]):
            print(color_response(words[i], responses[i]), end="\t")
            if words[i]:
                valid_solutions[i] = check_valid_solutions(valid_solutions[i], guess, responses[i])
        print("\n")
        
        solution_found = [None,] * WORDS[game_mode]
        
        end = False
        for i in range(WORDS[game_mode]):
            if words[i]:
                print(f"{BULLET[i]} [{i+1}] Palavra ➜ {COLOR['Green']}{len(valid_solutions[i])} {COLOR['White']}", end = "")
                if(len(valid_solutions[i]) != 1):
                    print("soluções possíveis: ", end = "")
                else:
                    print("solução possível: ", end = "")
                if len(valid_solutions[i]) <= PRINT_N_VALID_SOLUTIONS:
                    valid_solutions_iter = 1
                    for x in valid_solutions[i]:
                        print(f"{COLOR['Yellow']}{x}{COLOR['White']}", end = "")
                        if valid_solutions_iter != len(valid_solutions[0]):
                            print(", ", end = "")
                        else:
                            print(".", end = "")
                        valid_solutions_iter += 1                   
                else:
                    print(f"{COLOR['Yellow']}[>{PRINT_N_VALID_SOLUTIONS}]{COLOR['White']}", end = "")
                if len(valid_solutions[i]) == 1:
                    solution_found[i] = valid_solutions[i][0]
                    if responses[i] == [1, 1, 1, 1, 1]:
                        tries = turn
                    else:
                        tries = turn + 1
                    print(f"\n\n{BULLET[i]} [{i+1}] Palavra ➜ ✔️ Solução encontrada: {COLOR['Word']}{solution_found[i]}{COLOR['White']}.")
                    print(f"{BULLET[i]} [{i+1}] Palavra ➜ 💬 Número de tentativas: {COLOR['Green']}{tries}{COLOR['White']}.")
                    
                    words[i] = False
                    if not check_end(words):
                        print()
                        for j in range(WORDS[game_mode]):
                            print("🟩🟩🟩🟩🟩\t", end = "")
                        print("\n")
                        end = True
                        break
                    else:
                        if responses[i] != [1, 1, 1, 1, 1]:
                            guess = solution_found[i]
                            post_find = True
                            post_list.append(solution_found[i])
                        print()
                elif len(valid_solutions[i]) == 0:
                    if words[i]:
                        print(f"\n\n{BULLET[i]} [{i+1}] Palavra ➜ {COLOR['Red']}❌ Nenhuma solução encontrada!{COLOR['White']}")
                    end = True
                    break
                else:
                    print("\n")            
        if end:
            break