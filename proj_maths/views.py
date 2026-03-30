from django.shortcuts import redirect, render
from django.core.cache import cache
from . import terms_work
from . import categories_work
from . import sourses_work


def index(request):
    return render(request, "index.html")


def add_term(request):
    category_id = request.GET.get('category_id')
    categories = categories_work.get_list_of_categories()
    if not categories:
        terms = []
        context = {
            'terms': terms,
            'categories': categories,
            'selected_category_info': {},
        }
        return render(request, 'term_add.html', context)
    
    context = request.session.pop("send_term_response", {})

    # Если не определена выбранная категория
    if not (category_id and category_id != ''):
        category_id = "1"

    selected_category_info = categories_work.get_category_info(category_id)

    # Если выбранная категория не существует или не ликвидна
    if not selected_category_info:
        category_id = "1"
        selected_category_info = categories_work.get_category_info(category_id)
    
    terms = terms_work.get_terms_in_category_for_table(selected_category_info)
    context = context | {
        'terms': terms,
        'categories': categories,
        'selected_category_info': selected_category_info,
    }
    return render(request, "term_add.html", context)


def send_term(request):
    context = {}
    print(request.method)
    if request.method == "POST":
        cache.clear()
        category_id = request.POST.get('category_id_post')
        user_name = request.POST.get("name").replace(";", ",")
        user_email = request.POST.get("email").replace(";", ",")
        new_word = request.POST.get("word", "").replace(";", ",")
        new_definition = request.POST.get("definition", "").replace(";", ",")
        context["success"] = False
        context["request_answer"] = True
        context['target_category_id'] = category_id
        if len(new_word) == 0:
            context["comment"] = "Добавьте слово"
        elif len(new_word) > 30:
            context["comment"] = "Слишком длинное слово"
        elif len(new_definition) == 0:
            context["comment"] = "Добавьте определение"
        elif len(new_definition) > 300:
            context["comment"] = "Слишком длинное слово определение"
        else:
            source_id = sourses_work.get_source({
                    'name': user_name,
                    'email': user_email
                })
            
            category_info = categories_work.get_category_info(category_id)

            if category_info:
                new_word_info = {
                    'category_db_filename' : category_info['filename'],
                    'word' : new_word,
                    'definition': new_definition,
                    'source_id': source_id
                }
                res = terms_work.add_term_to_db(new_word_info)
                if res['success']:
                    context["success"] = True
                    context["comment"] = "Новое слово добавлено"
                else: 
                    context["comment"] = res["error_string"]
        request.session['send_term_response'] = context
        return redirect(f"/add-term?category_id={category_id}")
    else:
        return redirect(f"/add-term")


def send_new_category(request):
    context = {}
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name").replace(";", ",")
        user_email = request.POST.get("email").replace(";", ",")
        new_categoty_name = request.POST.get("new_categoty_name", "").replace(";", ",")
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
                    context["new_category_id"] = res["category_id"]
                else: 
                    context["comment"] = res["error_string"]
        request.session['send_category_response'] = context
        return redirect(f"/add-new-category")
    else:
        return redirect(f"/add-new-category")

def add_new_category(request):
    context = request.session.pop("send_category_response", {}) 
    return render(request, "new_category.html", context)

def show_stats(request):
    stats = categories_work.get_categories_stats(user_id=-1)
    return render(request, "stats.html", stats)

def term_list_category_selection(request):
    category_id = request.GET.get('category_id')
    
    categories = categories_work.get_list_of_categories()
    if not categories:
        terms = []
        context = {
            'terms': terms,
            'categories': categories,
            'selected_category_info': {},
        }
        return render(request, 'term_list_category_selection.html', context)
    
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