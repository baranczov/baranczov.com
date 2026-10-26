from django.db import migrations

# Snapshot of the work history approved on 2026-10-23.
EXPERIENCES = [{'company': 'Т-Банк',
  'role_ru': 'Machine Learning Engineer',
  'role_en': 'Machine Learning Engineer',
  'period_ru': 'Июль 2026 — Октябрь 2026',
  'period_en': 'July 2026 — October 2026',
  'color': 'yellow',
  'tasks': [{'title_ru': 'Обновление техстека',
             'title_en': 'Technology stack upgrade',
             'description_ru': 'Обновил MLOps-фреймворк с версии 0.1.x до 0.2.x и перевёл GitLab CI на '
                               'pipeline v2. Перенёс проект на Python 3.11 и проверил совместимость с Python '
                               '3.12. Обновил Airflow-инстансы train, QA и prod до версии 2.10.5, перенёс '
                               'модели из S3 в Model Registry, адаптировав код и конфигурации загрузки. '
                               'Проверил работу обучающих и QA DAG, а также инференса. Ретротестирование '
                               'подтвердило отсутствие расхождений в скорах моделей после миграции.',
             'description_en': 'Upgraded the MLOps framework from 0.1.x to 0.2.x and migrated GitLab CI to '
                               'pipeline v2. Moved the project to Python 3.11 and verified compatibility '
                               'with Python 3.12. Upgraded the train, QA and prod Airflow instances to '
                               '2.10.5, migrated models from S3 to Model Registry, and adapted the loading '
                               'code and configurations. Verified training and QA DAGs, as well as '
                               'inference. Retrospective testing confirmed that model scores remained '
                               'unchanged after the migration.'},
            {'title_ru': 'Разработка модели 172Т',
             'title_en': '172T model development',
             'description_ru': 'Подготовил локальную выборку для переобучения: исправил SQL-скрипты и логику '
                               'DAG в Airflow, заменив использование двух базисов единым. Изучил устройство '
                               'модели и результаты предыдущих экспериментов, на основе которых '
                               'сформулировал 10 гипотез повышения качества. Вместе с командой проверили '
                               'гипотезы на подготовленных данных, сравнили результаты экспериментов и '
                               'определили изменения, позволившие улучшить метрики модели.',
             'description_en': 'Prepared a local dataset for retraining: corrected SQL scripts and Airflow '
                               'DAG logic, replacing the use of two bases with a single one. Studied the '
                               'model architecture and previous experiment results, then formulated 10 '
                               'hypotheses for improving quality. Together with the team, tested the '
                               'hypotheses on the prepared data, compared experimental results and '
                               'identified changes that improved the model’s metrics.'},
            {'title_ru': 'Обновление ML System Doc',
             'title_en': 'ML System Doc update',
             'description_ru': 'Изучил существующую документацию и код всех моделей production-репозитория. '
                               'Сопоставил описание моделей с их реализацией, собрал вопросы по подготовке '
                               'данных, обучению и инференсу. Провёл встречи с разработчиками моделей, '
                               'уточнил детали и на основе полученных ответов актуализировал ML System Doc, '
                               'приведя документацию в соответствие с текущей реализацией.',
             'description_en': 'Reviewed the existing documentation and code for every model in the '
                               'production repository. Compared model descriptions with their '
                               'implementations and collected questions about data preparation, training and '
                               'inference. Met with model developers to clarify the details and used their '
                               'answers to update ML System Doc, bringing the documentation into line with '
                               'the current implementation.'}]},
 {'company': 'IT_ONE',
  'role_ru': 'Frontend-разработчик',
  'role_en': 'Frontend Developer',
  'period_ru': 'Август 2026 — Январь 2027',
  'period_en': 'August 2026 — January 2027',
  'color': 'blue',
  'tasks': [{'title_ru': 'Сервис обратной связи',
             'title_en': 'Feedback service',
             'description_ru': 'Разрабатываю интерфейсы для создания, просмотра и обработки обращений '
                               'пользователей. Реализую формы с валидацией, списки обращений с поиском, '
                               'фильтрацией и сортировкой, а также карточки с подробной информацией, '
                               'статусами и историей обработки. Продумываю состояния интерфейса для пустых '
                               'результатов, загрузки данных и ошибок.',
             'description_en': 'Develop interfaces for creating, viewing and processing user requests. '
                               'Implement validated forms, request lists with search, filtering and sorting, '
                               'and detailed cards showing status and processing history. Design interface '
                               'states for empty results, data loading and errors.'},
            {'title_ru': 'Сервис аналитики',
             'title_en': 'Analytics service',
             'description_ru': 'Создаю интерфейсы аналитических дашбордов с ключевыми показателями, '
                               'графиками и таблицами. Реализую фильтрацию по периодам и категориям, '
                               'переключение между представлениями данных и просмотр подробной информации по '
                               'выбранным показателям. Разрабатываю переиспользуемые компоненты для '
                               'единообразного отображения аналитики.',
             'description_en': 'Build analytics dashboards with key metrics, charts and tables. Implement '
                               'filtering by period and category, switching between data views, and viewing '
                               'detailed information for selected metrics. Develop reusable components for '
                               'consistent presentation of analytics.'},
            {'title_ru': 'Интеграция с API',
             'title_en': 'API integration',
             'description_ru': 'Подключаю интерфейсы к backend-сервисам: реализую получение и отправку '
                               'данных, обработку ответов и обновление содержимого после действий '
                               'пользователя. Добавляю состояния загрузки, сообщения об ошибках и '
                               'уведомления о результатах операций. Согласовываю с backend-разработчиками '
                               'форматы данных и поведение интерфейсов.',
             'description_en': 'Connect interfaces to backend services: implement data retrieval and '
                               'submission, response handling, and content updates after user actions. Add '
                               'loading states, error messages and notifications about operation results. '
                               'Coordinate data formats and interface behavior with backend developers.'}]},
 {'company': 'ВкусВилл',
  'role_ru': 'Machine Learning Engineer',
  'role_en': 'Machine Learning Engineer',
  'period_ru': 'Ноябрь 2025 — Март 2026',
  'period_en': 'November 2025 — March 2026',
  'color': 'lavender',
  'tasks': [{'title_ru': 'Разработка ML-пайплайна',
             'title_en': 'ML pipeline development',
             'description_ru': 'Спроектировал архитектуру интеллектуального ядра системы разбора инцидентов '
                               'дежурной поддержки на базе гибридного ML-пайплайна. Объединил распознавание '
                               'речи, обработку транскриптов и генерацию отчётов в последовательный процесс '
                               'обработки созвонов.',
             'description_en': 'Designed the architecture of the intelligent core for an on-call support '
                               'incident analysis system based on a hybrid ML pipeline. Combined speech '
                               'recognition, transcript processing and report generation into a sequential '
                               'workflow for processing calls.'},
            {'title_ru': 'Распознавание речи',
             'title_en': 'Speech recognition',
             'description_ru': 'Интегрировал Vosk для локальной транскрибации аудиопотоков созвонов в '
                               'реальном времени. Реализовал обработку на CPU с минимальной задержкой, чтобы '
                               'текст разговора поступал в систему по мере обсуждения инцидента.',
             'description_en': 'Integrated Vosk for local, real-time transcription of call audio streams. '
                               'Implemented low-latency CPU processing so that the conversation text entered '
                               'the system as the incident was being discussed.'},
            {'title_ru': 'Генерация отчётов',
             'title_en': 'Report generation',
             'description_ru': 'Реализовал Use-Case слой для буферизации транскриптов и их группировки по '
                               'сессиям. Подключил Groq API с моделью Llama-3 70B для формирования отчётов '
                               'по материалам созвонов со скоростью генерации более 200 токенов в секунду.',
             'description_en': 'Implemented a use-case layer to buffer transcripts and group them by '
                               'session. Connected the Groq API with the Llama-3 70B model to generate '
                               'reports from call transcripts at more than 200 tokens per second.'}]}]


def populate(apps, schema_editor):
    Experience = apps.get_model("portfolio", "Experience")
    Task = apps.get_model("portfolio", "ExperienceTask")
    db = schema_editor.connection.alias
    for position, content in enumerate(EXPERIENCES):
        fields = {key: value for key, value in content.items() if key not in ("company", "tasks")}
        experience, _ = Experience.objects.using(db).get_or_create(
            company=content["company"], defaults={**fields, "position": position},
        )
        # Keep uploaded covers, ordering and publication choices intact.
        for key, value in fields.items():
            setattr(experience, key, value)
        experience.tasks_ru = "\n".join(task["title_ru"] for task in content["tasks"])
        experience.tasks_en = "\n".join(task["title_en"] for task in content["tasks"])
        experience.save(using=db)
        for task_position, task in enumerate(content["tasks"]):
            Task.objects.using(db).get_or_create(experience=experience, position=task_position, defaults=task)
    # Preserve any independently authored legacy lists as editable task records.
    for experience in Experience.objects.using(db).exclude(company__in=[item["company"] for item in EXPERIENCES]):
        ru = [line.strip() for line in experience.tasks_ru.splitlines() if line.strip()]
        en = [line.strip() for line in experience.tasks_en.splitlines() if line.strip()]
        for position in range(max(len(ru), len(en))):
            Task.objects.using(db).create(
                experience=experience, position=position,
                title_ru=ru[position] if position < len(ru) else "",
                title_en=en[position] if position < len(en) else "",
            )


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0006_experience_tasks")]
    operations = [migrations.RunPython(populate, migrations.RunPython.noop)]
