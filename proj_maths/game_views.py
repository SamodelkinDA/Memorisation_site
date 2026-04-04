""" Модуль обработки событий для игр и рендер их страниц """
import random
from django.shortcuts import render, redirect

from . import categories_work
from . import terms_work

def pair_game(request):
    """ Обработка работы страницы игры pair-game """
    category_id = request.GET.get('category_id', '')
    categories = categories_work.get_list_of_categories()

    selected_category_info = categories_work.get_category_info(category_id)

    # Если выбранная категория не существует или не ликвидна
    if categories and not selected_category_info:
        category_id = "1"
        selected_category_info = categories_work.get_category_info(category_id)

    context = {
        'categories': categories,
        'selected_category_info': selected_category_info,
    }

    pairs_to_use = terms_work.select_terms_for_game(selected_category_info)

    # Инициализируем игровое состояние в сессии
    if 'pair_game_state' not in request.session:
        game_state = initialize_game_state(pairs_to_use, selected_category_info['id'])
        request.session['pair_game_state'] = game_state
    elif request.session['pair_game_state']['category_id'] != selected_category_info['id']:
        game_state = initialize_game_state(pairs_to_use, selected_category_info['id'])
        request.session['pair_game_state'] = game_state

    game_state = request.session['pair_game_state']

    if request.method == 'POST':
        if game_state['current_st'] == 'ERROR' or game_state['current_st'] == 'CORRECT':
            game_state['current_st'] = 'IDLE'
            game_state['left_id'] = ''
            game_state['right_id'] = ''
            game_state['message'] = "Давай! Вперед"

        left_id = request.POST.get('left_id', '')
        right_id = request.POST.get('right_id', '')
        action = request.POST.get('action', '')

        if action == 'reset':
            pairs_to_use = terms_work.select_terms_for_game(selected_category_info)
            request.session['pair_game_state'] = initialize_game_state(
                pairs_to_use, selected_category_info['id']
                )
            game_state = request.session['pair_game_state']

        elif action == 'reshaffle':
            request.session['pair_game_state'] = initialize_game_state(
                pairs_to_use, selected_category_info['id']
                )
            game_state = request.session['pair_game_state']

        elif action == 'quit':
            request.session.pop('pair_game_state')
            return redirect("/")

        # Это запись и чтение из сессии нажатых кнопок
        if left_id:
            if game_state['left_id']:
                if game_state['left_id'] == left_id:
                    game_state['left_id'] = ''
                else:
                    game_state['left_id'] = left_id
            else:
                game_state['left_id'] = left_id
        else:
            left_id = game_state['left_id']

        if right_id:
            if game_state['right_id']:
                if game_state['right_id'] == right_id:
                    game_state['right_id'] = ''
                else:
                    game_state['right_id'] = right_id
            else:
                game_state['right_id'] = right_id
        else:
            right_id = game_state['right_id']

        # Обработка пары
        if left_id and right_id:
            left_word = next((w for w in game_state['left_words'] if w['id'] == left_id), None)
            right_word = next((w for w in game_state['right_words'] if w['id'] == right_id), None)

            if (left_word and right_word and 
                    left_word['status'] == 'active' and right_word['status'] == 'active'):
                if left_id == right_id:
                    left_word['status'] = 'removed'
                    right_word['status'] = 'removed'

                    game_state['message'] = "Верно!"
                    game_state['current_st'] = 'CORRECT'

                    if game_state['active_pairs'] > 1:
                        game_state['active_pairs'] -= 1
                    else:
                        game_state['message'] = "Все верно! Поздравляем! Ошибок:" + \
                                                        f"{game_state['errors']}"
                else:
                    game_state['message'] = "Не угадал"
                    game_state['current_st'] = 'ERROR'
                    game_state['errors'] += 1
        request.session['pair_game_state'] = game_state
        return redirect(f"/pair-game?category_id={selected_category_info['id']}#game-section")
    context = context | game_state
    return render(request, 'pair_game.html', context)

def initialize_game_state(pairs, category_id):
    """Инициализирует начальное состояние игры pair-game """
    left_words = [{'id': pair['id'], 'text': pair['left'], 'status': 'active'} for pair in pairs]
    right_words = [{'id': pair['id'], 'text': pair['right'], 'status': 'active'} for pair in pairs]

    random.shuffle(left_words)
    random.shuffle(right_words)

    return {
        'active_pairs': len(pairs),
        'errors': 0,
        'left_words': left_words,
        'right_words': right_words,
        'left_id': '',
        'right_id': '',
        'message': "Давай! Вперед",
        'current_st' : 'IDLE',  # варианты 'IDLE', 'CORRECT', 'ERROR',
        'category_id': category_id
    }

def memo_game(request):
    """ Обработка работы страницы игры memo-game """
    category_id = request.GET.get('category_id', '')
    categories = categories_work.get_list_of_categories()

    selected_category_info = categories_work.get_category_info(category_id)

    # Если выбранная категория не существует или не ликвидна
    if categories and not selected_category_info:
        category_id = "1"
        selected_category_info = categories_work.get_category_info(category_id)

    context = {
        'categories': categories,
        'selected_category_info': selected_category_info,
    }

    pairs_to_use = terms_work.select_terms_for_game(selected_category_info)

    # Инициализируем игровое состояние в сессии
    if 'memo_game_state' not in request.session:
        game_state = initialize_memo_game_state(pairs_to_use, selected_category_info['id'])
        request.session['memo_game_state'] = game_state
    elif request.session['memo_game_state']['category_id'] != selected_category_info['id']:
        game_state = initialize_memo_game_state(pairs_to_use, selected_category_info['id'])
        request.session['memo_game_state'] = game_state

    game_state = request.session['memo_game_state']

    if request.method == 'POST':
        if game_state['current_st'] == 'ERROR' or game_state['current_st'] == 'CORRECT':
            game_state['current_st'] = 'IDLE'
            game_state['id1'] = ''
            game_state['id2'] = ''
            game_state['message'] = "Давай! Вперед"

        card_id = request.POST.get('card_id', '')
        action = request.POST.get('action', '')

        if action == 'reset':
            pairs_to_use = terms_work.select_terms_for_game(selected_category_info)
            request.session['memo_game_state'] = initialize_memo_game_state(
                pairs_to_use, selected_category_info['id']
                )
            game_state = request.session['memo_game_state']

        elif action == 'reshaffle':
            request.session['memo_game_state'] = initialize_memo_game_state(
                pairs_to_use, selected_category_info['id']
                )
            game_state = request.session['memo_game_state']

        elif action == 'quit':
            request.session.pop('memo_game_state')
            return redirect("/")

        # Это запись и чтение из сессии нажатых кнопок
        if card_id:
            if game_state['id1']:
                if game_state['id1'] == card_id:
                    pass
                else:
                    game_state['id2'] = card_id
            else:
                game_state['id1'] = card_id

        id1 = game_state['id1']
        id2 = game_state['id2']

        # Обработка пары
        if id1 and id2:
            word1 = next((w for w in game_state['cards'] if w['id'] == id1), None)
            word2 = next((w for w in game_state['cards'] if w['id'] == id2), None)

            if word1 and word2 and word1['status'] == 'active' and word2['status'] == 'active':
                if int(id1) + int(id2) == 0:
                    word1['status'] = 'removed'
                    word2['status'] = 'removed'

                    game_state['message'] = "Верно!"
                    game_state['current_st'] = 'CORRECT'

                    if game_state['active_pairs'] > 1:
                        game_state['active_pairs'] -= 1
                    else:
                        game_state['message'] = "Все верно! Поздравляем! Ошибок:" + \
                                                    f" {game_state['errors']}"
                else:
                    game_state['message'] = "Не угадал"
                    game_state['current_st'] = 'ERROR'
                    game_state['errors'] += 1
        request.session['memo_game_state'] = game_state
        return redirect(f"/memo-game?category_id={selected_category_info['id']}#game-section")
    context = context | game_state
    return render(request, 'memo_game.html', context)

def initialize_memo_game_state(pairs, category_id):
    """ Инициализирует начальное состояние игры memo-game """
    left_words = [{
        'id': pair['id'],
        'text': pair['left'], 
        'status': 'active'
        } for pair in pairs]
    right_words = [{
        'id': '-' + pair['id'], 
        'text': pair['right'], 
        'status': 'active'
        } for pair in pairs]
    cards = left_words + right_words

    random.shuffle(cards)

    return {
        'active_pairs': len(pairs),
        'errors': 0,
        'cards': cards,
        'id1': '',
        'id2': '',
        'message': "Давай! Вперед",
        'current_st' : 'IDLE',  # варианты 'IDLE', 'CORRECT', 'ERROR',
        'category_id': category_id
    }
