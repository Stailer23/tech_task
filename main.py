import NeuroNetLibrary, NeuroNluLibrary, NeuroVoiceLibrary

nn = NeuroNetLibrary()
nlu = NeuroNluLibrary()
nv = NeuroVoiceLibrary()


def main():
    '''Планирование звонка и определение точки входа в логику'''
    nn.call(msisdn='89012345678', date='2022-09-12 10:00:00', entry_point='hello_main')


'''
---hello_logic---
Прохождение по диалогу приветствия и запись этапов в логи
'''


def hello_main():
    nn.log('prompt', 'hello_main')
    nv.say('hello')
    return hello_detect()


def hello_null():
    nn.log('element', 'func_hello_null')
    if nn.counter('hello_null', '+') >= 1:
        return hangup_null()
    nv.say('hello_null')
    return hello_detect()


def hello_repeat():
    nn.log('prompt', 'hello_repeat')
    nv.say('hello_repeat')
    return hello_detect()


def hello_detect():
    '''функция нахождения сущностей в логике приветствия'''
    with nv.listen(500, entities=[
        'confirm',
        'wrong_time',
        'repeat',
    ]) as r:
        nn.log('hello_detect_entity', r)
    return hello_logic(r)


def hello_logic(r):
    """Логика условий переходов по функциям приветствия"""
    if not r:
        nn.log('state', 'say_NULL')
        return hello_null()

    if not r.has_entities():
        nn.log('state', 'DEFAULT')
        return recommend_main()

    if r.has_entity('confirm'):
        if r.entity('confirm') == 'true':
            nn.log('state', 'confirm=True')
            return recommend_main()
        elif r.entity('confirm') == 'false':
            nn.log('state', 'confirm=False')
            return hangup_wrong_time()

    if r.has_entity('wrong_time'):
        if r.entity('wrong_time') == 'true':
            nn.log('state', 'say_BUSY')
            return hangup_wrong_time()

    if r.has_entity('repeat'):
        if r.entity('repeat') == 'true':
            nn.log('state', 'say_REPEAT')
            return hello_repeat()

    nn.log('state', 'Didnt detected entities')
    return hangup_wrong_time()


'''
---main logic---
Прохождение по основному скрипту диалога и запись этапов в логи 
'''


def recommend_main():
    nn.log("prompt", "recommend_main")
    nv.say('recommend_main')
    return recommend_detect()


def recommend_repeat():
    nn.log("prompt", "recommend_repeat")
    nv.say('recommend_repeat')
    return recommend_detect()


def recommend_repeat_2():
    nn.log("prompt", "recommend_repeat_2")
    nv.say('recommend_repeat_2')
    return recommend_detect()


def recommend_score_negative():
    nn.log("prompt", "recommend_score_negative")
    nv.say('recommend_score_negative')
    return recommend_detect()


def recommend_score_neutral():
    nn.log("prompt", "recommend_score_neutral")
    nv.say('recommend_score_neutral')
    return recommend_detect()


def recommend_score_positive():
    nn.log("prompt", "recommend_score_positive")
    nv.say('recommend_score_positive')
    return recommend_detect()


def recommend_null():
    '''Завершает диалог, если абонента не слышно больше 1 итерации'''
    nn.log('element', 'func_recommend_null')
    if nn.counter('recommend_null', '+') >= 1:
        return hangup_null()
    nv.say('recommend_null')
    return recommend_detect()


def recommend_default():
    nn.log("prompt", "recommend_default")
    nv.say('recommend_default')
    return recommend_detect()


def recommend_detect():
    '''Функция распознования сущностей в основной логике скрипта'''
    with nv.listen(500, entities=[
        'recommendation_score',
        'recommendation',
        'repeat',
        'wrong_time',
        'question',
    ]) as r:
        nn.log('recommend_detect_entity', r)
    return main_logic(r)


def main_logic(r):
    '''Условия переходов по функциям основной логике скрипта'''
    if not r:
        nn.log('state', 'NULL')
        return recommend_null()

    if not r.has_entities():
        nn.log('state', 'DEFAULT')
        return recommend_default()

    if r.has_entity('recommendation_score'):
        nn.log('recommendation_score', r.entity('recommendation_score'))
        if r.entity('recommendation_score') in range(9):
            return hangup_negative()
        elif r.entity('recommendation_score') in [9, 10]:
            return hangup_positive()

    if r.has_entity('recommendation'):
        if r.entity('recommendation') == 'negative':
            nn.log('state', 'recommendation=negative')
            return recommend_score_negative()
        elif r.entity('recommendation') == 'neutral':
            nn.log('state', 'recommendation=neutral')
            return recommend_score_neutral()
        elif r.entity('recommendation') == 'positive':
            nn.log('state', 'recommendation=positive')
            return recommend_score_positive()
        elif r.entity('recommendation') == 'dont_know':
            nn.log('state', 'recommendation=dont_know')
            return recommend_repeat_2()

    if r.has_entity('repeat'):
        if r.entity('repeat') == 'true':
            nn.log('state', 'say_repeat')
            return recommend_repeat()

    if r.has_entity('wrong_time'):
        if r.entity('wrong_time') == 'true':
            nn.log('state', 'say_BUSY')
            return hangup_wrong_time()

    if r.has_entity('question'):
        if r.entity('question') == 'true':
            nn.log('state', 'quest')
            return forward()


'''
---hangup_logic---
Запись в логи времени звонка и транскрипцию диалогов, сгруппированных по результатам опроса.
Завершение диалога и разрыв/переадресация соединения.
'''


def hangup_positive():
    nn.log('call_duration_positive_score', nv.get_call_duration())
    nn.log('call_transcription_positive_score', nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT))
    nv.say('hangup_positive')
    nn.dialog.result = nn.RESULT_DONE
    nv.hangup()


def hangup_negative():
    nn.log('call_duration_negative_score', nv.get_call_duration())
    nn.log('call_transcription_negative_score', nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT))
    nv.say('hangup_negative')
    nn.dialog.result = nn.RESULT_DONE
    nv.hangup()


def hangup_wrong_time():
    nn.log('call_duration_wrong_time', nv.get_call_duration())
    nn.log('call_transcription_wrong_time', nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT))
    nv.say('hangup_wrong_time')
    nn.dialog.result = nn.RESULT_DONE
    nv.hangup()


def hangup_null():
    nn.log('call_duration_hangup_null', nv.get_call_duration())
    nn.log('call_transcription_hangup_null', nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT))
    nv.say('hangup_null')
    nn.dialog.result = nn.RESULT_DONE
    nv.hangup()


def forward():
    nn.log('call_duration_question', nv.get_call_duration())
    nn.log('call_transcription_question', nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT))
    nv.say('forward')
    nn.dialog.result = nn.RESULT_DONE
    nv.bridge('перевод_на_оператора')


if __name__ == '__main__':
    main()