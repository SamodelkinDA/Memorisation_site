import random
def get_terms_in_category_for_table(category_info : dict):
    """ Список всех карточек из категории """
    terms = []
    if category_info:
        with open(f"./data/{category_info['filename']}.csv", "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                term_id, term, definition, _ = line.split(";")
                terms.append([term_id, term, definition])
    return terms

def add_term_to_db(new_word_info : dict) -> dict:
    """ Добавление новой карточки в БД """
    result = {
        "success": True,
        "error_string" : ""
    }
    max_word_id = 0
    with open(f"./data/{new_word_info['category_db_filename']}.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            term_id, *_ = line.split(";")
            max_word_id = max(max_word_id, int(term_id))
    new_term_line = f"\n{max_word_id + 1};{new_word_info['word']}" + \
        f";{new_word_info['definition']};{new_word_info['source_id']}"
    with open(f"./data/{new_word_info['category_db_filename']}.csv", "a", encoding="utf-8") as f:
        f.write(new_term_line)
    return result

def select_terms_for_game(category_info : dict, max_number : int = 10):
    """ """
    terms = []
    with open(f"./data/{category_info['filename']}.csv", "r", encoding="utf-8") as f:
        for line in random.sample(f.readlines()[1:], min(max_number, len(terms))):
            term_id, term, definition, _ = line.split(";")
            terms.append({'id': term_id, 'left': definition, 'right': term})
    return terms
