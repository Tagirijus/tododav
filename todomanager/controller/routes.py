'''
The web routes for the todomanager website.
'''

from fastapi import FastAPI
from todomanager.model import config
import caldav


app = FastAPI()


@app.get('/')
def read_home():
    with caldav.DAVClient(
        url=config.NC_URI,
        username=config.NC_USER,
        password=config.NC_PASSWORD
    ) as client:
        principal = client.principal()
    calendar = principal.calendar(config.NC_CALENDAR)
    todo = calendar.todos()[0]
    vtodo = todo.vobject_instance

    # so kann ich checken, ob der Todo-Eintrag alle nötigen Tags hat
    # WEITER HIER:
    #   Kann man nicht noch sinnvoller die Todos mit einer Art
    #   Query bekommen? Sonst erschiene mir das etwas cumberstone ...
    tags = vtodo.vtodo.categories.value
    check = 0
    for tag_need in config.NC_TAGS:
        if tag_need in tags:
            check += 1
    if len(config.NC_TAGS) == check:
        print('ALLE TAGS DA!')
    else:
        print('... es fehlen Tags !!')
    print(todo.data)

    # so kann ich überschreiben und speichern
    # vtodo.vtodo.summary.value = 'am mondigen Montag'
    # todo.save()

    return 'calendar.todos()'
