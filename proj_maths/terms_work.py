def get_terms_in_category_for_table(category_info : dict):
    terms = []
    with open(f"./data/{category_info['filename']}.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            id, term, definition, source = line.split(";")
            terms.append([id, term, definition])
    return terms

def add_term_to_db(new_word_info : dict) -> dict:
    result = {
        "success": True,
        "error_string" : ""
    }
    max_word_id = 0
    with open(f"./data/{new_word_info['category_db_filename']}.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            id, word, definition, sourse_id = line.split(";")
            if int(id) > max_word_id:
                max_word_id = int(id)
    new_term_line = f"\n{max_word_id + 1};{new_word_info['word']};{new_word_info['definition']};{new_word_info['source_id']}"
    with open(f"./data/{new_word_info['category_db_filename']}.csv", "a", encoding="utf-8") as f:
        f.write(new_term_line)
    return result