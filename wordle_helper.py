import wordle


def guess_to_colors(guess, colors_list):
    colors_dict = {
        'x': ['','','','',''], # grey
        'y': ['','','','',''], # yellow
        'g': ['','','','','']  # green
    }
    for i, char in enumerate(guess):
        colors_dict[colors_list[i]][i] = char

    return colors_dict


def count_letters(word):
    count_dict = {}
    for char in word:
        if char in count_dict:
            count_dict[char] += 1
        else:
            count_dict[char] = 1

    return count_dict


def wordle_guess(possible_answers, guess, colors_list):
    colors = guess_to_colors(guess, colors_list)

    # grey and yellow logic changes when a letter is already green:
    # e.g.
    # solution: elder
    # lever -> yyxgg
    # ruler -> xxygg

    post_grey_possible_answers = []
    for word in possible_answers:
        for i, letter in enumerate(colors['x']):
            if letter != '' and letter in word:
                if letter == word[i]:
                    break
                elif letter not in colors['g']:
                    break
        else:
            post_grey_possible_answers.append(word)

    green_letter_count = count_letters(colors['g'])
    post_yellow_possible_answers = []
    for word in post_grey_possible_answers:
        for i, letter in enumerate(colors['y']):
            if letter != '':
                if letter not in word:
                    break
                elif letter == word[i]:
                    break
                elif letter in colors['g'] and count_letters(word)[letter] <= green_letter_count[letter]:
                    break
        else:
            post_yellow_possible_answers.append(word)

    post_green_possible_answers = []
    for word in post_yellow_possible_answers:
        for i, letter in enumerate(colors['g']):
            if letter != '' and letter != word[i]:
                break
        else:
            post_green_possible_answers.append(word)

    return post_green_possible_answers


def next_best_guess(possible_answers):
    # count all occurences of letters in possible answers
    # sum counts of unique letters per word
    # sort

    # this is kind of opinionated though
    # maybe it should just get the count sum once
    # and use that each time instead of recalculating

    total_letter_count = {}
    for word in possible_answers:
        for letter in word:
            if letter in total_letter_count:
                total_letter_count[letter] += 1
            else:
                total_letter_count[letter] = 1

    word_letter_count_sum = {}
    for word in possible_answers:
        letter_count_sum = 0
        for letter in set(word):
            letter_count_sum += total_letter_count[letter]
        word_letter_count_sum[word] = letter_count_sum

    words_sorted_by_letter_count_sum = sorted(
        word_letter_count_sum, key=word_letter_count_sum.get, reverse=True
    )

    return words_sorted_by_letter_count_sum


def input_loop():
    new_possible_answers = wordle.possible_answers
    while True:
        print(next_best_guess(new_possible_answers)[:10])

        guess = ''
        while len(guess) != 5:
            guess = input('Word guessed? ')

        colors_list = ''
        while len(colors_list) != 5:
            colors_list = input('Color results? ')
        
        new_possible_answers = wordle_guess(new_possible_answers, guess, colors_list)

        print(new_possible_answers)


def main():
    try:
        input_loop()
    except KeyboardInterrupt:
        print('')


if __name__ == '__main__':
    main()