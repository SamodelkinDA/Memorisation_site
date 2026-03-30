
def get_category_info(target_category_id : str = "1") -> dict:
    target_category_info = {}
    with open("./data/biblios.csv", "r", encoding="utf-8") as biblios_file:
        for line in biblios_file.readlines()[1:]:
            category_id, public_name, filename, available, \
                  word_title, definition_title, sourse_id = line.split(";")
            if category_id == target_category_id and available == "1":
                target_category_info = {'id': category_id,
                                        'name': public_name,
                                        'filename': filename, 
                                        'available' : available,
                                        'word_title': word_title,
                                        'definition_title': definition_title,
                                        'sourse_id': sourse_id}
    return target_category_info 
    
def get_list_of_categories() -> list:
    categories = []
    with open("./data/biblios.csv", "r", encoding="utf-8") as biblios_file:
        for line in biblios_file.readlines()[1:]:
            category_id, public_name, filename, available, \
                  word_title, definition_title, sourse_id = line.split(";")
            if available == "1":
                categories.append((category_id, public_name))
    return categories

def add_new_category(new_category_info : dict) -> dict:
    result = {
        "success": True,
        "error_string" : ""
    }
    max_category_id = 0
    with open("./data/biblios.csv", "r", encoding="utf-8") as biblios_file:
        for line in biblios_file.readlines()[1:]:
            category_id, public_name, filename, available, \
                    word_title, definition_title, sourse_id = line.split(";")
            if int(category_id) > max_category_id:
                max_category_id = int(category_id)
            if public_name == new_category_info['name']:
                result = {
                    "success": False,
                    "error_string" : "Категория с таким названием уже существует"
                }
                break
    if result['success']:
        with open("./data/biblios.csv", "a", encoding="utf-8") as biblios_file:
            biblios_file.write("\n" + f"{max_category_id + 1};{new_category_info['name']};" +
                            f"{str(max_category_id + 1)};1;{new_category_info['word_title']};" +
                                f"{new_category_info['definition_title']};{new_category_info['sourse_id']}")
        with open(f'./data/{max_category_id + 1}.csv', 'x') as f:
            f.write("id;word;definition;sourse_id")
        result['category_id'] = f'{max_category_id + 1}'
    return result

def get_categories_stats(user_id):
    categories_number = 0
    your_categories_number = 0
    cards_numbers = []
    with open("./data/biblios.csv", "r", encoding="utf-8") as bib_file:
        for line in bib_file.readlines()[1:]:
            ategory_id, public_name, filename, available, \
                  word_title, definition_title, sourse_id = line.split(";")
            if available:
                categories_number += 1
                if user_id == sourse_id:
                    your_categories_number += 1
                with open(f"./data/{filename}.csv", "r", encoding="utf-8") as category_file:
                    cards_numbers.append(len(category_file.readlines()) - 1)
    
    stats = {
        "categories_number": categories_number,
        "your_categories_number": your_categories_number,
        "words_avg": sum(cards_numbers)/len(cards_numbers),
        "words_max": max(cards_numbers),
        "words_min": min(cards_numbers)
    }
    return stats

