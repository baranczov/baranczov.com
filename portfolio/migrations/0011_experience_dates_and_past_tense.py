from django.db import migrations


# Frozen approved content: keep historical migrations independent of seed data.
PERIODS = {'Т-Банк': {'period_ru': 'Март 2026 - Октябрь 2026', 'period_en': 'March 2026 - October 2026'},
 'IT_ONE': {'period_ru': 'Февраль 2026 - Июль 2026', 'period_en': 'February 2026 - July 2026'}}

IT_ONE_TASKS = {'Сервис обратной связи': {'description_ru': 'Разрабатывал интерфейсы для создания, просмотра и '
                                             'обработки обращений пользователей. Реализовывал '
                                             'формы с валидацией, списки обращений с поиском, '
                                             'фильтрацией и сортировкой, а также карточки с '
                                             'подробной информацией, статусами и историей '
                                             'обработки. Продумывал состояния интерфейса для '
                                             'пустых результатов, загрузки данных и ошибок.',
                           'description_en': 'Developed interfaces for creating, viewing and '
                                             'processing user requests. Implemented validated '
                                             'forms, request lists with search, filtering and '
                                             'sorting, and detailed cards showing status and '
                                             'processing history. Designed interface states for '
                                             'empty results, data loading and errors.'},
 'Сервис аналитики': {'description_ru': 'Создавал интерфейсы аналитических дашбордов с ключевыми '
                                        'показателями, графиками и таблицами. Реализовывал '
                                        'фильтрацию по периодам и категориям, переключение между '
                                        'представлениями данных и просмотр подробной информации по '
                                        'выбранным показателям. Разрабатывал переиспользуемые '
                                        'компоненты для единообразного отображения аналитики.',
                      'description_en': 'Built analytics dashboards with key metrics, charts and '
                                        'tables. Implemented filtering by period and category, '
                                        'switching between data views, and viewing detailed '
                                        'information for selected metrics. Developed reusable '
                                        'components for consistent presentation of analytics.'},
 'Интеграция с API': {'description_ru': 'Подключал интерфейсы к backend-сервисам: реализовывал '
                                        'получение и отправку данных, обработку ответов и '
                                        'обновление содержимого после действий пользователя. '
                                        'Добавлял состояния загрузки, сообщения об ошибках и '
                                        'уведомления о результатах операций. Согласовывал с '
                                        'backend-разработчиками форматы данных и поведение '
                                        'интерфейсов.',
                      'description_en': 'Connected interfaces to backend services: implemented '
                                        'data retrieval and submission, response handling, and '
                                        'content updates after user actions. Added loading states, '
                                        'error messages and notifications about operation results. '
                                        'Coordinated data formats and interface behavior with '
                                        'backend developers.'}}


def update_work_history(apps, schema_editor):
    alias = schema_editor.connection.alias
    Experience = apps.get_model("portfolio", "Experience")
    ExperienceTask = apps.get_model("portfolio", "ExperienceTask")
    for company, periods in PERIODS.items():
        Experience.objects.using(alias).filter(company=company).update(**periods)
    for title, descriptions in IT_ONE_TASKS.items():
        ExperienceTask.objects.using(alias).filter(
            experience__company="IT_ONE", title_ru=title,
        ).update(**descriptions)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0010_project_content")]
    operations = [migrations.RunPython(update_work_history, migrations.RunPython.noop)]
