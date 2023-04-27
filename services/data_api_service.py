import json


def update_api_counter(new_value):
    with open('data/data_api.json', 'r+') as file:
        data = json.load(file)
        data = new_value
        with open('data/data_api.json', 'w') as f:
            json.dump(data, f, indent=4)


def get_data_api():
    with open('data/data_api.json', 'r') as file:
        data = json.load(file)
        return data


def count_words(input_string):
    # Split the string into a list of words
    words_list = input_string.split()

    # Count the number of words in the list
    word_count = len(words_list)

    # Return the word count
    return word_count
