from datetime import datetime as dt

new_event_title_text = "заголовок собрания"

new_event_description_text = "описание собрания"

new_event_themes_text = "темы собрания"

new_event_location_text = "место собрания"

new_event_location_url_text = "ссылка на адрес места собрания"

new_event_datetime_text = "дата и время начала собрания"

new_event_img_text = "изображение для сообщения"


def refactor_datetime(datetime: dt = None) -> str:
    return f'\n\n🗓️Дата: {datetime.strftime("%d.%m.%Y")}\n\n🕛Время: {datetime.strftime("%H:%M")}' if datetime else ''


def refactor_location(location: str = None, location_url: str = None) -> str:
    if location_url and location:
        return f'\n\n🗺️Место: <a href="{location_url}">{location}</a>'
    if location:
        return f'\n\n🗺️Место: {location}'
    return ''


def refactor_themes(themes: str = None):
    if themes:
        themes = themes.replace("\n", "\n▫️")
        return f"\n\n📋<b>Темы этого и будущих собраний:</b>\n▫️{themes}"
    return ''


def event_constructor(
        title: str = None,
        description: str = None,
        themes: str = None,
        location: str = None,
        location_url: str = None,
        datetime: dt = None,
        id: int = None,
        ev_id: int = None
) -> str:
    title = f"📚<b><u>{title}</u></b>" if title else ''
    description = f"\n\n‼️{description}" if description else ''
    themes = refactor_themes(themes)
    datetime = refactor_datetime(datetime)
    location = refactor_location(location, location_url)

    return title + description + themes + datetime + location


new_event_texts = {
    'title': new_event_title_text,
    'description': new_event_description_text,
    'themes': new_event_themes_text,
    'datetime': new_event_datetime_text,
    'location': new_event_location_text,
    'location_url': new_event_location_url_text,
    'img': new_event_img_text
}

steps = ('title', 'description', 'themes', 'datetime', 'location', 'location_url', 'img')

next_text = "Продолжить?"
save_text = "Сохранить?"
