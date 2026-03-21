
def get_category_info(target_category_id : str = "1") -> dict:
    target_category_info = {}
    with open("./data/biblios.csv", "r", encoding="utf-8") as biblios_file:
        for line in biblios_file.readlines()[1:]:
            category_id, public_name, filename, available, \
                  word_title, definition_title = line.split(";")
            if category_id == target_category_id and available == "1":
                target_category_info = {'id': category_id,
                                        'name': public_name,
                                        'filename': filename, 
                                        'available' : available,
                                        'word_title': word_title,
                                        'definition_title': definition_title}
    return target_category_info 
    
def get_list_of_categories() -> list:
    categories = []
    with open("./data/biblios.csv", "r", encoding="utf-8") as biblios_file:
        for line in biblios_file.readlines()[1:]:
            category_id, public_name, filename, available, \
                  word_title, definition_title = line.split(";")
            if available == "1":
                categories.append((category_id, public_name))
    return categories


def write_term(new_term, new_definition):
    new_term_line = f"{new_term};{new_definition};user"
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        existing_terms = [l.strip("\n") for l in f.readlines()]
        title = existing_terms[0]
        old_terms = existing_terms[1:]
    terms_sorted = old_terms + [new_term_line]
    terms_sorted.sort()
    new_terms = [title] + terms_sorted
    with open("./data/terms.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_terms))


def get_terms_stats():
    db_terms = 0
    user_terms = 0
    defin_len = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            term, defin, added_by = line.split(";")
            words = defin.split()
            defin_len.append(len(words))
            if "user" in added_by:
                user_terms += 1
            elif "db" in added_by:
                db_terms += 1
    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": sum(defin_len)/len(defin_len),
        "words_max": max(defin_len),
        "words_min": min(defin_len)
    }
    return stats

