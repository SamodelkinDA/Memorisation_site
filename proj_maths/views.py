from django.shortcuts import render
from django.core.cache import cache
from . import terms_work
from . import categories_work


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