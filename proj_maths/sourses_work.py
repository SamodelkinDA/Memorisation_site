

def get_source(source_info : dict):
    target_source = -1
    max_source_id = 0
    with open("./data/sourses.csv", "r", encoding="utf-8") as sources_file:
        for line in sources_file.readlines()[1:]:
            source_id, sourse_name, sourse_email, rank = line.split(";")
            if sourse_name == source_info['name'] and sourse_email == source_info['email']:
                target_source = source_id
                break
            if int(source_id) > max_source_id:
                max_source_id = int(source_id)
    if target_source == -1:
        with open("./data/sourses.csv", "a", encoding="utf-8") as sources_file:
            new_source = f"\n{max_source_id + 1};{source_info['name']};{source_info['email']};{0}"
            sources_file.write(new_source)
        target_source = max_source_id + 1

    return str(target_source)

def get_source_info(target_source_id : str) -> dict:
    source_info = {}
    with open("./data/sourses.csv", "r", encoding="utf-8") as sources_file:
        for line in sources_file.readlines()[1:]:
            source_id, sourse_name, sourse_email, rank = line.split(";")
            if source_id == target_source_id:
                source_info['name'] = sourse_name
                source_info['email'] = sourse_email
                break
    return source_info