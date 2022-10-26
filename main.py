WORD_SIZE = 5
TURNS_TERMO = 7
TURNS_DUETO = 8
TURNS_QUARTETO = 10
PRINT_N_VALID_SOLUTIONS = 20

def product(array):
    if not array:
        yield()
    else:
        for x in array[0]:
            for y in product(array[1:]):
                yield(x, ) + y

def convert_alphanum(word):
    letter_dict = {"a": "a", "b": "b", "c": "c", "d": "d", "e": "e", "f": "f", "g": "g",
        "h": "h", "i": "i", "j": "j", "k": "k", "l": "l", "m": "m", "n": "n",
        "o": "o", "p": "p", "q": "q", "r": "r", "s": "s", "t": "t", "u": "u",
        "v": "v", "w": "w", "x": "x", "y": "y", "z": "z", "á": "a", "à": "a",
        "â": "a", "ã": "a", "é": "e", "ê": "e", "è": "e", "í": "i", "ï": "i",
        "ó": "o", "ô": "o", "õ": "o", "ú": "u", "û": "u", "ü": "u", "ç": "c"}

    word = word.lower()
    for i, v in enumerate(word):
        word = word[:i] + letter_dict[v] + word[i + 1:]

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
    possible_responses = list(product([[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2]]))
    higher_score = float("inf")
    max_guess = None
    for _, v in enumerate(valid_guesses):
        score = 0
        for response in possible_responses:
            if response != (1, 1, 1, 1, 1):
                solutions = check_valid_solutions(valid_solutions, v, response)
                score += pow(len(solutions), 2) / len(valid_solutions)
        if score < higher_score:
            higher_score = score
            max_guess = v
    return max_guess, higher_score

if __name__ == "__main__":
    
    print("\n🟢 " + "\33[92m" + "1 - Termo" + "\33[0m")
    print("🟡 " + "\33[93m" + "2 - Dueto" + "\33[0m")
    print("🔴 " + "\33[91m" + "3 - Quarteto" + "\33[0m")
    
    termo = dueto = quarteto = False
    
    while True:
        mode = input("\n\33[0m" + "Escolha o modo de jogo: " + "\33[94m")
        if mode.isdigit():
            if int(mode) == 1:
                print("\n🟢 \33[92m" + "Termo iniciado!" + "\33[0m")
                termo = True
                break
            elif int(mode) == 2:
                print("\n🟡 \33[93m" + "Dueto iniciado!" + "\33[0m")
                dueto = True
                break
            elif int(mode) == 3:
                print("\n🔴 \33[91m" + "Quarteto iniciado!" + "\33[0m")
                quarteto = True
                break
        else:
            mode = mode.lower()
            if mode == "termo":
                print("\n🟢 \33[92m" + "Termo iniciado!" + "\33[0m")
                termo = True
                break
            elif mode == "dueto":
                print("\n🟡 \33[93m" + "Dueto iniciado!" + "\33[0m")
                dueto = True
                break
            elif mode == "quarteto":
                print("\n🔴 \33[91m" + "Quarteto iniciado!" + "\33[0m")
                quarteto = True
                break
      
    if termo:                   ###############     TERMO     ###############
        guesses = []
        solutions = []

        with open("guesses") as file:
            for line in file:
                guesses.append(line.rstrip())

        with open("solutions") as file:
            for line in file:
                solutions.append(line.rstrip())

        alphanum_guesses = [convert_alphanum(w) for w in guesses]
        alphanum_solutions = [convert_alphanum(w) for w in solutions]

        valid_solutions = alphanum_solutions

        for turn in range(1, TURNS_TERMO):
            if turn == 1:
                while True:
                    guess = input("\n\33[0m" + "Escolha a palavra inicial: " + "\33[93m")
                    if len(guess) == WORD_SIZE and guess.isalpha():
                        break
                    else:
                        print("\33[91m" + f"A palavra deve possuir {WORD_SIZE} letras." + "\33[0m")
                print("\33[0m" + "Usou a palavra: " + "\33[92m\33[4m" + guess + "\33[0m.\n")
                guess = convert_alphanum(guess)
                print("❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
            else:
                guess, _ = max_guess(alphanum_solutions, valid_solutions)
                print("Use a palavra: " + "\33[93m" + guess + "\33[0m.")
            
            admit = True
            while True:
                if not admit:
                    print("Use a palavra: " + "\33[93m" + guess + "\33[0m.")
                response = input("\33[0m" + "Resposta do termo: " + "\33[91m")
                admit = True
                if len(response) != WORD_SIZE or response.isdigit() is False:
                    print("\33[91m" + f"A resposta deve possuir {WORD_SIZE} caracteres (números)." + "\33[0m\n")
                    continue 
                if response.isdigit():
                    for x in response:
                        if (int(x) != 0 and int(x) != 1 and int(x) != 2):
                            admit = False
                            print("\33[0m" + "❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
                            break             
                if admit:
                    break
                
            response = [int(x) for x in response]
            print("\33[0m", end = "")
            for x in response:
                if x == 0:
                    print("🔳", end = "")
                elif x == 1:
                    print("🟩", end = "")
                elif x == 2:
                    print("🟨", end = "")
            print("\n")
            
            valid_solutions = check_valid_solutions(valid_solutions, guess, response)
            
            if len(valid_solutions) <= PRINT_N_VALID_SOLUTIONS:
                if(len(valid_solutions) != 1):
                    print("\33[92m" + str(len(valid_solutions)) + "\33[0m" + " soluções possíveis: ", end = "")
                else:
                    print("\33[92m" + str(len(valid_solutions)) + "\33[0m" + " solução possível: ", end = "")
                valid_solutions_iter = 1
                for x in valid_solutions:
                    print("\33[93m" + x + "\33[0m", end = "")
                    if valid_solutions_iter != len(valid_solutions):
                        print(", ", end = "")
                    else:
                        print(".", end = "")
                    valid_solutions_iter += 1
            else:
                print("\33[92m" + str(len(valid_solutions)) + "\33[0m" + " soluções possíveis.", end = "")
            
            if len(valid_solutions) == 1:
                solution = valid_solutions[0]
                if response == [1, 1, 1, 1, 1]:
                    tries = turn
                else:
                    tries = turn + 1
                print("\n")
                print("✔️ Solução encontrada: " + "\33[92m\33[4m" + solution + "\33[0m.")
                print("💬 Número de tentativas: " + "\33[92m" + str(tries) + "\33[0m.\n")
                print("🟩🟩🟩🟩🟩")
                break
            elif len(valid_solutions) == 0:
                print("❌ \33[91m" + "Nenhuma solução encontrada!" + "\33[0m")
                break
            else:
                print("\n")
    elif dueto:                     ###############     DUETO     ###############
        guesses = []
        solutions = []

        with open("guesses") as file:
            for line in file:
                guesses.append(line.rstrip())

        with open("solutions") as file:
            for line in file:
                solutions.append(line.rstrip())

        alphanum_guesses = [convert_alphanum(w) for w in guesses]
        alphanum_solutions = [convert_alphanum(w) for w in solutions]

        valid_solutions_1 = valid_solutions_2 = alphanum_solutions

        for turn in range(1, TURNS_DUETO):
            if turn == 1:
                word_1 = word_2 = True
                post_find = False
                while True:
                    guess = input("\n\33[0m" + "Escolha a palavra inicial: " + "\33[93m")
                    if len(guess) == WORD_SIZE and guess.isalpha():
                        break
                    else:
                        print("\33[91m" + f"A palavra deve possuir {WORD_SIZE} letras." + "\33[0m")
                print("\33[0m" + "Usou a palavra: " + "\33[92m\33[4m" + guess + "\33[0m.\n")
                guess = convert_alphanum(guess)
                print("❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
            else:
                if not post_find:
                    if word_1:
                        guess_1, score_1 = max_guess(alphanum_solutions, valid_solutions_1)
                        guess = guess_1
                    if word_2:
                        guess_2, score_2 = max_guess(alphanum_solutions, valid_solutions_2)
                        guess = guess_2
                    if word_1 and word_2:
                        if score_1 >= score_2:
                            guess = guess_1
                        else:
                            guess = guess_2
                print("Use a palavra: " + "\33[93m" + guess + "\33[0m.")
            
            post_find = False
            admit = True
            while True:
                if not admit:   
                    print("Use a palavra: " + "\33[93m" + guess + "\33[0m.")
                if word_1:
                    response_1 = input("\33[0m" + "🔸 [1] Palavra ➜ Resposta do termo: " + "\33[91m")
                else:
                    response_1 = "00000"
                if word_2:
                    response_2 = input("\33[0m" + "🔹 [2] Palavra ➜ Resposta do termo: " + "\33[91m")
                else:
                    response_2 = "00000"
                admit = True
                if len(response_1) != WORD_SIZE or response_1.isdigit() is False or len(response_2) != WORD_SIZE or response_2.isdigit() is False:
                    print("\33[91m" + f"A resposta deve possuir {WORD_SIZE} caracteres (números)." + "\33[0m\n")
                    continue 
                if response_1.isdigit() and response_2.isdigit():
                    for x in response_1:
                        if (int(x) != 0 and int(x) != 1 and int(x) != 2):
                            admit = False
                            print("\33[0m" + "❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
                            break
                    if admit:
                        for x in response_2:
                            if (int(x) != 0 and int(x) != 1 and int(x) != 2):
                                admit = False
                                print("\33[0m" + "❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
                                break           
                if admit:
                    break
            
            response_1 = [int(x) for x in response_1]
            response_2 = [int(x) for x in response_2]

            print()
            print("\33[0m", end = "")
            if word_1:
                for x in response_1:
                    if x == 0:
                        print("🔳", end = "")
                    elif x == 1:
                        print("🟩", end = "")
                    elif x == 2:
                        print("🟨", end = "")
            else:
                print("🟩🟩🟩🟩🟩", end = "")

            print("\t", end = "")
            if word_2:
                for x in response_2:
                    if x == 0:
                        print("🔳", end = "")
                    elif x == 1:
                        print("🟩", end = "")
                    elif x == 2:
                        print("🟨", end = "")
            else:
                print("🟩🟩🟩🟩🟩", end = "")

            print("\n")

            if word_1:
                valid_solutions_1 = check_valid_solutions(valid_solutions_1, guess, response_1)
                
            if word_2:
                valid_solutions_2 = check_valid_solutions(valid_solutions_2, guess, response_2)

            if word_1:
                if len(valid_solutions_1) <= PRINT_N_VALID_SOLUTIONS:
                    if(len(valid_solutions_1) != 1):
                        print("🔸 [1] Palavra ➜ \33[92m" + str(len(valid_solutions_1)) + "\33[0m" + " soluções possíveis: ", end = "")
                    else:
                        print("🔸 [1] Palavra ➜ \33[92m" + str(len(valid_solutions_1)) + "\33[0m" + " solução possível: ", end = "")
                    valid_solutions_iter = 1
                    for x in valid_solutions_1:
                        print("\33[93m" + x + "\33[0m", end = "")
                        if valid_solutions_iter != len(valid_solutions_1):
                            print(", ", end = "")
                        else:
                            print(".", end = "")
                        valid_solutions_iter += 1
                else:
                    print("🔸 [1] Palavra ➜ \33[92m" + str(len(valid_solutions_1)) + "\33[0m" + " soluções possíveis.", end = "")
                
                if len(valid_solutions_1) == 1:
                    solution_1 = valid_solutions_1[0]
                    if response_1 == [1, 1, 1, 1, 1]:
                        tries_1 = turn
                    else:
                        tries_1 = turn + 1
                    print("\n\n🔸 [1] Palavra ➜ ✔️ Solução encontrada: " + "\33[92m\33[4m" + solution_1 + "\33[0m.")
                    print("🔸 [1] Palavra ➜ 💬 Número de tentativas: " + "\33[92m" + str(tries_1) + "\33[0m.")
                    word_1 = False
                    if word_2 is False:
                        print("\n🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩")
                        break
                    else:
                        if response_1 != [1, 1, 1, 1, 1]:
                            guess = solution_1
                            post_find = True
                        print()
                elif len(valid_solutions_1) == 0:
                    if word_1:
                        print("\n\n🔸 [1] Palavra ➜ \33[91m" + "❌ Nenhuma solução encontrada!" + "\33[0m")
                    break
                else:
                    print("\n")

            if word_2:
                if len(valid_solutions_2) <= PRINT_N_VALID_SOLUTIONS:
                    if(len(valid_solutions_2) != 1):
                        print("🔹 [2] Palavra ➜ \33[92m" + str(len(valid_solutions_2)) + "\33[0m" + " soluções possíveis: ", end = "")
                    else:
                        print("🔹 [2] Palavra ➜ \33[92m" + str(len(valid_solutions_2)) + "\33[0m" + " solução possível: ", end = "")
                    valid_solutions_iter = 1
                    for x in valid_solutions_2:
                        print("\33[93m" + x + "\33[0m", end = "")
                        if valid_solutions_iter != len(valid_solutions_2):
                            print(", ", end = "")
                        else:
                            print(".", end = "")
                        valid_solutions_iter += 1
                else:
                    print("🔹 [2] Palavra ➜ \33[92m" + str(len(valid_solutions_2)) + "\33[0m" + " soluções possíveis.", end = "")
                
                if len(valid_solutions_2) == 1:
                    solution_2 = valid_solutions_2[0]
                    if response_2 == [1, 1, 1, 1, 1]:
                        tries_2 = turn
                    else:
                        tries_2 = turn + 1
                    print("\n\n🔹 [2] Palavra ➜ ✔️ Solução encontrada: " + "\33[92m\33[4m" + solution_2 + "\33[0m.")
                    print("🔹 [2] Palavra ➜ 💬 Número de tentativas: " + "\33[92m" + str(tries_2) + "\33[0m.")
                    word_2 = False
                    if word_1 is False:
                        print("\n🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩")
                        break
                    else:
                        if response_2 != [1, 1, 1, 1, 1]:
                            guess = solution_2
                            post_find = True
                        print()
                elif len(valid_solutions_2) == 0:
                    if word_2:
                        print("\n\n🔹 [2] Palavra ➜ \33[91m" + "❌ Nenhuma solução encontrada!" + "\33[0m")
                    break
                else:
                    print("\n")
    elif quarteto:              ###############     QUARTETO     ###############
        guesses = []
        solutions = []

        with open("guesses") as file:
            for line in file:
                guesses.append(line.rstrip())

        with open("solutions") as file:
            for line in file:
                solutions.append(line.rstrip())

        alphanum_guesses = [convert_alphanum(w) for w in guesses]
        alphanum_solutions = [convert_alphanum(w) for w in solutions]

        valid_solutions_1 = valid_solutions_2 = valid_solutions_3 = valid_solutions_4 = alphanum_solutions

        for turn in range(1, TURNS_QUARTETO):
            if turn == 1:
                word_1 = word_2 = word_3 = word_4 = True
                post_list = []
                post_find = False
                while True:
                    guess = input("\n\33[0m" + "Escolha a palavra inicial: " + "\33[93m")
                    if len(guess) == WORD_SIZE and guess.isalpha():
                        break
                    else:
                        print("\33[91m" + f"A palavra deve possuir {WORD_SIZE} letras." + "\33[0m")
                print("\33[0m" + "Usou a palavra: " + "\33[92m\33[4m" + guess + "\33[0m.\n")
                guess = convert_alphanum(guess)
                print("❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
            else:
                if not post_find:
                    if word_1:
                        guess_1, score_1 = max_guess(alphanum_solutions, valid_solutions_1)
                        guess = guess_1
                    if word_2:
                        guess_2, score_2 = max_guess(alphanum_solutions, valid_solutions_2)
                        guess = guess_2
                    if word_3:
                        guess_3, score_3 = max_guess(alphanum_solutions, valid_solutions_3)
                        guess = guess_3
                    if word_4:
                        guess_4, score_4 = max_guess(alphanum_solutions, valid_solutions_4)
                        guess = guess_4
                    if word_1 and word_2 and word_3 and word_4:
                        if score_1 >= score_2:
                            guess = guess_1
                            max_score = score_1
                        else:
                            guess = guess_2
                            max_score = score_2
                        if score_3 > max_score:
                            guess = guess_3
                            max_score = score_3
                        if score_4 > max_score:
                            guess = guess_4
                    elif word_1 and word_2 and word_3 and not word_4:
                        if score_1 >= score_2:
                            guess = guess_1
                            max_score = score_1
                        else:
                            guess = guess_2
                            max_score = score_2
                        if score_3 > max_score:
                            guess = guess_3
                    elif word_1 and word_2 and not word_3 and word_4:
                        if score_1 >= score_2:
                            guess = guess_1
                            max_score = score_1
                        else:
                            guess = guess_2
                            max_score = score_2
                        if score_4 > max_score:
                            guess = guess_4
                    elif word_1 and word_2 and not word_3 and not word_4:
                        if score_1 >= score_2:
                            guess = guess_1
                        else:
                            guess = guess_2
                    elif word_1 and not word_2 and word_3 and word_4:
                        if score_1 >= score_3:
                            guess = guess_1
                            max_score = score_1
                        else:
                            guess = guess_3
                            max_score = score_3
                        if score_4 > max_score:
                            guess = guess_4
                    elif word_1 and not word_2 and word_3 and not word_4:
                        if score_1 >= score_3:
                            guess = guess_1
                        else:
                            guess = guess_3
                    elif word_1 and not word_2 and not word_3 and word_4:
                        if score_1 >= score_4:
                            guess = guess_1
                        else:
                            guess = guess_4
                    elif not word_1 and word_2 and word_3 and word_4:
                        if score_2 >= score_3:
                            guess = guess_2
                            max_score = score_2
                        else:
                            guess = guess_3
                            max_score = score_3
                        if score_4 > max_score:
                            guess = guess_4
                    elif not word_1 and word_2 and word_3 and not word_4:
                        if score_2 >= score_3:
                            guess = guess_2
                        else:
                            guess = guess_3
                    elif not word_1 and word_2 and not word_3 and word_4:
                        if score_2 >= score_4:
                            guess = guess_2
                        else:
                            guess = guess_4
                    elif not word_1 and not word_2 and word_3 and word_4:
                        if score_3 >= score_4:
                            guess = guess_3
                        else:
                            guess = guess_4
                else:
                    guess = post_list.pop(0)
                print("Use a palavra: " + "\33[93m" + guess + "\33[0m.")
            
            if not post_list:
                post_find = False
            admit = True
            while True:
                if not admit:
                    print("Use a palavra: " + "\33[93m" + guess + "\33[0m.")
                if word_1:
                    response_1 = input("\33[0m" + "🟠 [1] Palavra ➜ Resposta do termo: " + "\33[91m")
                else:
                    response_1 = "00000"
                if word_2:
                    response_2 = input("\33[0m" + "🔵 [2] Palavra ➜ Resposta do termo: " + "\33[91m")
                else:
                    response_2 = "00000"
                if word_3:
                    response_3 = input("\33[0m" + "🟣 [3] Palavra ➜ Resposta do termo: " + "\33[91m")
                else:
                    response_3 = "00000"
                if word_4:
                    response_4 = input("\33[0m" + "🟤 [4] Palavra ➜ Resposta do termo: " + "\33[91m")
                else:
                    response_4 = "00000"
                admit = True
                if len(response_1) != WORD_SIZE or response_1.isdigit() is False or len(response_2) != WORD_SIZE or response_2.isdigit() is False:
                    print("\33[91m" + f"A resposta deve possuir {WORD_SIZE} caracteres (números)." + "\33[0m\n")
                    continue
                elif len(response_3) != WORD_SIZE or response_3.isdigit() is False or len(response_4) != WORD_SIZE or response_4.isdigit() is False:
                    print("\33[91m" + f"A resposta deve possuir {WORD_SIZE} caracteres (números)." + "\33[0m\n")
                    continue
                if response_1.isdigit() and response_2.isdigit() and response_3.isdigit() and response_4.isdigit():
                    for x in response_1:
                        if (int(x) != 0 and int(x) != 1 and int(x) != 2):
                            admit = False
                            print("\33[0m" + "❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
                            break
                    if admit:
                        for x in response_2:
                            if (int(x) != 0 and int(x) != 1 and int(x) != 2):
                                admit = False
                                print("\33[0m" + "❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
                                break
                    if admit:
                        for x in response_3:
                            if (int(x) != 0 and int(x) != 1 and int(x) != 2):
                                admit = False
                                print("\33[0m" + "❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
                                break
                    if admit:
                        for x in response_4:
                            if (int(x) != 0 and int(x) != 1 and int(x) != 2):
                                admit = False
                                print("\33[0m" + "❕ A resposta do termo equivale, para cada casa, a 🔳 = 0, 🟩 = 1 e 🟨 = 2.\n")
                                break
                if admit:
                    break
            
            response_1 = [int(x) for x in response_1]
            response_2 = [int(x) for x in response_2]
            response_3 = [int(x) for x in response_3]
            response_4 = [int(x) for x in response_4]

            print()
            print("\33[0m", end = "")
            if word_1:
                for x in response_1:
                    if x == 0:
                        print("🔳", end = "")
                    elif x == 1:
                        print("🟩", end = "")
                    elif x == 2:
                        print("🟨", end = "")
            else:
                print("🟩🟩🟩🟩🟩", end = "")

            print("\t", end = "")
            if word_2:
                for x in response_2:
                    if x == 0:
                        print("🔳", end = "")
                    elif x == 1:
                        print("🟩", end = "")
                    elif x == 2:
                        print("🟨", end = "")
            else:
                print("🟩🟩🟩🟩🟩", end = "")

            print("\t", end = "")
            if word_3:
                for x in response_3:
                    if x == 0:
                        print("🔳", end = "")
                    elif x == 1:
                        print("🟩", end = "")
                    elif x == 2:
                        print("🟨", end = "")
            else:
                print("🟩🟩🟩🟩🟩", end = "")

            print("\t", end = "")
            if word_4:
                for x in response_4:
                    if x == 0:
                        print("🔳", end = "")
                    elif x == 1:
                        print("🟩", end = "")
                    elif x == 2:
                        print("🟨", end = "")
            else:
                print("🟩🟩🟩🟩🟩", end = "")

            print("\n")
            if word_1:
                valid_solutions_1 = check_valid_solutions(valid_solutions_1, guess, response_1)
            
            if word_2:
                valid_solutions_2 = check_valid_solutions(valid_solutions_2, guess, response_2)
            
            if word_3:
                valid_solutions_3 = check_valid_solutions(valid_solutions_3, guess, response_3)
            
            if word_4:
                valid_solutions_4 = check_valid_solutions(valid_solutions_4, guess, response_4)

            if word_1:
                if len(valid_solutions_1) <= PRINT_N_VALID_SOLUTIONS:
                    if(len(valid_solutions_1) != 1):
                        print("🟠 [1] Palavra ➜ \33[92m" + str(len(valid_solutions_1)) + "\33[0m" + " soluções possíveis: ", end = "")
                    else:
                        print("🟠 [1] Palavra ➜ \33[92m" + str(len(valid_solutions_1)) + "\33[0m" + " solução possível: ", end = "")
                    valid_solutions_iter = 1
                    for x in valid_solutions_1:
                        print("\33[93m" + x + "\33[0m", end = "")
                        if valid_solutions_iter != len(valid_solutions_1):
                            print(", ", end = "")
                        else:
                            print(".", end = "")
                        valid_solutions_iter += 1
                else:
                    print("🟠 [1] Palavra ➜ \33[92m" + str(len(valid_solutions_1)) + "\33[0m" + " soluções possíveis.", end = "")
                
                if len(valid_solutions_1) == 1:
                    solution_1 = valid_solutions_1[0]
                    if response_1 == [1, 1, 1, 1, 1]:
                        tries_1 = turn
                    else:
                        tries_1 = turn + 1
                    print("\n\n🟠 [1] Palavra ➜ ✔️ Solução encontrada: " + "\33[92m\33[4m" + solution_1 + "\33[0m.")
                    print("🟠 [1] Palavra ➜ 💬 Número de tentativas: " + "\33[92m" + str(tries_1) + "\33[0m.")
                    word_1 = False
                    if word_2 is False and word_3 is False and word_4 is False:
                        print("\n🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩")
                        break
                    else:
                        if response_1 != [1, 1, 1, 1, 1]:
                            post_find = True
                            post_list.append(solution_1)
                        print()
                elif len(valid_solutions_1) == 0:
                    if word_1:
                        print("\n\n🟠 [1] Palavra ➜ \33[91m" + "❌ Nenhuma solução encontrada!" + "\33[0m")
                    break
                else:
                    print("\n")

            if word_2:
                if len(valid_solutions_2) <= PRINT_N_VALID_SOLUTIONS:
                    if(len(valid_solutions_2) != 1):
                        print("🔵 [2] Palavra ➜ \33[92m" + str(len(valid_solutions_2)) + "\33[0m" + " soluções possíveis: ", end = "")
                    else:
                        print("🔵 [2] Palavra ➜ \33[92m" + str(len(valid_solutions_2)) + "\33[0m" + " solução possível: ", end = "")
                    valid_solutions_iter = 1
                    for x in valid_solutions_2:
                        print("\33[93m" + x + "\33[0m", end = "")
                        if valid_solutions_iter != len(valid_solutions_2):
                            print(", ", end = "")
                        else:
                            print(".", end = "")
                        valid_solutions_iter += 1
                else:
                    print("🔵 [2] Palavra ➜ \33[92m" + str(len(valid_solutions_2)) + "\33[0m" + " soluções possíveis.", end = "")
                
                if len(valid_solutions_2) == 1:
                    solution_2 = valid_solutions_2[0]
                    if response_2 == [1, 1, 1, 1, 1]:
                        tries_2 = turn
                    else:
                        tries_2 = turn + 1
                    print("\n\n🔵 [2] Palavra ➜ ✔️ Solução encontrada: " + "\33[92m\33[4m" + solution_2 + "\33[0m.")
                    print("🔵 [2] Palavra ➜ 💬 Número de tentativas: " + "\33[92m" + str(tries_2) + "\33[0m.")
                    word_2 = False
                    if word_1 is False and word_3 is False and word_4 is False:
                        print("\n🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩")
                        break
                    else:
                        if response_2 != [1, 1, 1, 1, 1]:
                            post_find = True
                            post_list.append(solution_2)
                        print()
                elif len(valid_solutions_2) == 0:
                    if word_2:
                        print("\n\n🔵 [2] Palavra ➜ \33[91m" + "❌ Nenhuma solução encontrada!" + "\33[0m")
                    break
                else:
                    print("\n")

            if word_3:
                if len(valid_solutions_3) <= PRINT_N_VALID_SOLUTIONS:
                    if(len(valid_solutions_3) != 1):
                        print("🟣 [3] Palavra ➜ \33[92m" + str(len(valid_solutions_3)) + "\33[0m" + " soluções possíveis: ", end = "")
                    else:
                        print("🟣 [3] Palavra ➜ \33[92m" + str(len(valid_solutions_3)) + "\33[0m" + " solução possível: ", end = "")
                    valid_solutions_iter = 1
                    for x in valid_solutions_3:
                        print("\33[93m" + x + "\33[0m", end = "")
                        if valid_solutions_iter != len(valid_solutions_3):
                            print(", ", end = "")
                        else:
                            print(".", end = "")
                        valid_solutions_iter += 1
                else:
                    print("🟣 [3] Palavra ➜ \33[92m" + str(len(valid_solutions_3)) + "\33[0m" + " soluções possíveis.", end = "")
                
                if len(valid_solutions_3) == 1:
                    solution_3 = valid_solutions_3[0]
                    if response_3 == [1, 1, 1, 1, 1]:
                        tries_3 = turn
                    else:
                        tries_3 = turn + 1
                    print("\n\n🟣 [3] Palavra ➜ ✔️ Solução encontrada: " + "\33[92m\33[4m" + solution_3 + "\33[0m.")
                    print("🟣 [3] Palavra ➜ 💬 Número de tentativas: " + "\33[92m" + str(tries_3) + "\33[0m.")
                    word_3 = False
                    if word_1 is False and word_2 is False and word_4 is False:
                        print("\n🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩")
                        break
                    else:
                        if response_3 != [1, 1, 1, 1, 1]:
                            post_find = True
                            post_list.append(solution_3)
                        print()
                elif len(valid_solutions_3) == 0:
                    if word_3:
                        print("\n\n🟣 [3] Palavra ➜ \33[91m" + "❌ Nenhuma solução encontrada!" + "\33[0m")
                    break
                else:
                    print("\n")
            
            if word_4:
                if len(valid_solutions_4) <= PRINT_N_VALID_SOLUTIONS:
                    if(len(valid_solutions_4) != 1):
                        print("🟤 [4] Palavra ➜ \33[92m" + str(len(valid_solutions_4)) + "\33[0m" + " soluções possíveis: ", end = "")
                    else:
                        print("🟤 [4] Palavra ➜ \33[92m" + str(len(valid_solutions_4)) + "\33[0m" + " solução possível: ", end = "")
                    valid_solutions_iter = 1
                    for x in valid_solutions_4:
                        print("\33[93m" + x + "\33[0m", end = "")
                        if valid_solutions_iter != len(valid_solutions_4):
                            print(", ", end = "")
                        else:
                            print(".", end = "")
                        valid_solutions_iter += 1
                else:
                    print("🟤 [4] Palavra ➜ \33[92m" + str(len(valid_solutions_4)) + "\33[0m" + " soluções possíveis.", end = "")
                
                if len(valid_solutions_4) == 1:
                    solution_4 = valid_solutions_4[0]
                    if response_4 == [1, 1, 1, 1, 1]:
                        tries_4 = turn
                    else:
                        tries_4 = turn + 1
                    print("\n\n🟤 [4] Palavra ➜ ✔️ Solução encontrada: " + "\33[92m\33[4m" + solution_4 + "\33[0m.")
                    print("🟤 [4] Palavra ➜ 💬 Número de tentativas: " + "\33[92m" + str(tries_4) + "\33[0m.")
                    word_4 = False
                    if word_1 is False and word_2 is False and word_3 is False:
                        print("\n🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩\t🟩🟩🟩🟩🟩")
                        break
                    else:
                        if response_4 != [1, 1, 1, 1, 1]:
                            post_find = True
                            post_list.append(solution_4)
                        print()
                elif len(valid_solutions_4) == 0:
                    if word_4:
                        print("\n\n🟤 [4] Palavra ➜ \33[91m" + "❌ Nenhuma solução encontrada!" + "\33[0m")
                    break
                else:
                    print("\n")