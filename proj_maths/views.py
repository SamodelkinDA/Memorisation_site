from django.shortcuts import render
from django.core.cache import cache
from . import terms_work
from . import categories_work
from . import sourses_work


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def send_new_category(request):
    context = {"request_answer" : True}
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        user_email = request.POST.get("email")
        new_categoty_name = request.POST.get("new_categoty_name", "")
        new_categoty_word_title = request.POST.get("new_categoty_word_title", "").replace(";", ",")
        new_categoty_definition_title = request.POST.get("new_categoty_definition_title", "").replace(";", ",")
        context["success"] = False
        context["request_answer"] = True
        if len(new_categoty_name) == 0:
            context["comment"] = "Добавьте название"
        elif len(new_categoty_name) > 30:
            context["comment"] = "Слишком длинное название"
        elif len(new_categoty_word_title) == 0:
            context["comment"] = "Добавьте название для запоминаемых слов"
        elif len(new_categoty_word_title) > 30:
            context["comment"] = "Название для запоминаемых слов слишком длинное"
        elif len(new_categoty_definition_title) == 0:
            context["comment"] = "Добавьте название для фраз-определений"
        elif len(new_categoty_definition_title) > 30:
            context["comment"] = "Название для фраз-определений слишком длинное"
        else:
            
            source_id = sourses_work.get_source({
                'name': user_name,
                'email': user_email
            })
            if source_id > 0:
                res = categories_work.add_new_category({'id': "-1",
                                            'name': new_categoty_name,
                                            'filename': "", 
                                            'available' : "1",
                                            'word_title': new_categoty_word_title,
                                            'definition_title': new_categoty_definition_title,
                                            'sourse_id': source_id})
                if res['success']:
                    context["success"] = True
                    context["comment"] = "Новая категория успешно создана"
                else: 
                    context["comment"] = res["error_string"]
        return render(request, "new_category.html", context)
    else:
        return add_new_category(request)

def add_new_category(request):
    context ={"request_answer" : False}
    return render(request, "new_category.html", context)

def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)

def term_list_category_selection(request):
    category_id = request.GET.get('category_id')
    
    categories = categories_work.get_list_of_categories()
    if not categories:
        pass    # TODO обработка отсутствия категорий вообще
    
    # Если не определена выбранная категория
    if not (category_id and category_id != ''):
        category_id = "1"

    selected_category_info = categories_work.get_category_info(category_id)

    # Если выбранная категория не существует или не ликвидна
    if not selected_category_info:
        category_id = "1"
        selected_category_info = categories_work.get_category_info(category_id)
    
    terms = terms_work.get_terms_in_category_for_table(selected_category_info)
    context = {
        'terms': terms,
        'categories': categories,
        'selected_category_info': selected_category_info,
    }
    
    return render(request, 'term_list_category_selection.html', context)