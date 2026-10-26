"""Approved work history. Used only when initializing new records."""
EXPERIENCES = [
    {
        "company": "Т-Банк", "role_ru": "Machine Learning Engineer", "role_en": "Machine Learning Engineer",
        "period_ru": "Март 2026 - Октябрь 2026", "period_en": "March 2026 - October 2026", "color": "yellow",
        "tasks_ru": "Миграция ML-инфраструктуры\nРазработка модели 172Т\nДокументация ML-систем",
        "tasks_en": "ML infrastructure migration\n172T model development\nML system documentation",
        "tasks": [
            {
                "title_ru": "Миграция ML-инфраструктуры", "title_en": "ML infrastructure migration",
                "description_ru": "Самостоятельно обновил MLOps-фреймворк, GitLab CI, Python и Airflow для 25 моделей комплаенса: 25 train DAG и 25 QA DAG в окружениях train/QA/prod. Перенёс модели из S3 в Model Registry. Изменения внедрены в production; упростились загрузка, версионирование, повторное обучение и сопровождение.\n\nРетротестированием на существующей выборке проверил старую и новую версии всех 25 моделей: скоры и итоговые метрики совпали в пределах установленного допуска.",
                "description_en": "Independently upgraded the MLOps framework, GitLab CI, Python and Airflow for 25 compliance models: 25 training DAGs and 25 QA DAGs across train/QA/prod environments. Migrated models from S3 to Model Registry. The changes were deployed to production, simplifying model loading, versioning, retraining and maintenance.\n\nRetrospectively tested the old and new versions of all 25 models on an existing dataset, confirming that prediction scores and aggregate metrics matched within the specified tolerance.",
            },
            {
                "title_ru": "Разработка модели 172Т", "title_en": "172T model development",
                "description_ru": "Подготовил выборку на едином базисе, исправив SQL-скрипты и Airflow DAG. Лично реализовал 10 гипотез и повысил ROC-AUC с 0,92 до 0,95 в экспериментах. До моего ухода улучшенная версия не была внедрена в production.",
                "description_en": "Prepared the training dataset from a unified sampling base, correcting SQL scripts and Airflow DAGs. Personally implemented and tested changes for 10 hypotheses, improving ROC-AUC from 0.92 to 0.95 in experiments. The improved version had not been deployed to production when I left.",
            },
            {
                "title_ru": "Документация ML-систем", "title_en": "ML system documentation",
                "description_ru": "Актуализировал ML System Doc по 25 моделям, сверив подготовку данных, обучение и инференс с кодом. Изменения приняты всей командой.",
                "description_en": "Updated ML System Doc for 25 models, checking data preparation, training and inference descriptions against the code. The changes were accepted by the entire team.",
            },
        ],
    },
    {
        "company": "IT_ONE", "role_ru": "Machine Learning Engineer", "role_en": "Machine Learning Engineer",
        "period_ru": "Февраль 2026 - Июль 2026", "period_en": "February 2026 - July 2026", "color": "blue",
        "tasks_ru": "Подготовка текстовых данных\nРазработка NLP-модели\nПодготовка сервиса к интеграции",
        "tasks_en": "Text data preparation\nNLP model development\nService preparation for integration",
        "tasks": [
            {
                "title_ru": "Подготовка текстовых данных", "title_en": "Text data preparation",
                "description_ru": "Подготовил датасет из 60 тыс. обращений по 12 категориям для маршрутизации в поддержке. Очистил тексты, удалил дубликаты и согласовал правила разметки. Сформировал временное разделение train/validation/test, исключив пересечение цепочек обращений между выборками.",
                "description_en": "Prepared a dataset of 60,000 requests across 12 categories for support ticket routing. Cleaned text, removed duplicates and agreed on annotation guidelines. Created time-based train/validation/test splits, keeping entire request threads within a single split.",
            },
            {
                "title_ru": "Разработка NLP-модели", "title_en": "NLP model development",
                "description_ru": "Дообучил RuBERT на PyTorch и Hugging Face Transformers; сравнил с baseline TF-IDF и логистической регрессией. На отложенной выборке получил macro-F1 0,86 против 0,78 у baseline. Проанализировал ошибки и дисбаланс классов, подготовил уточнения разметки неоднозначных категорий.",
                "description_en": "Fine-tuned RuBERT using PyTorch and Hugging Face Transformers and compared it with a TF-IDF and logistic regression baseline. Achieved a macro-F1 of 0.86 versus 0.78 for the baseline on a held-out dataset. Analyzed errors and class imbalance and proposed annotation refinements for ambiguous categories.",
            },
            {
                "title_ru": "Подготовка сервиса к интеграции", "title_en": "Service preparation for integration",
                "description_ru": "Реализовал FastAPI-сервис в Docker с пакетной обработкой, валидацией запросов, логированием ошибок и версионированием модели. На стенде с NVIDIA T4 получил p95 задержки 120 мс для одиночных запросов до 256 токенов. Передал сервис и контракт API backend-команде; production-запуск в период работы не состоялся.",
                "description_en": "Implemented a Dockerized FastAPI service with batch processing, request validation, error logging and model versioning. Measured p95 latency of 120 ms on an NVIDIA T4 test system for single requests of up to 256 tokens. Handed the service and API contract over to the backend team; production deployment did not take place during my tenure.",
            },
        ],
    },
    {
        "company": "ВкусВилл", "role_ru": "Machine Learning Engineer", "role_en": "Machine Learning Engineer",
        "period_ru": "Ноябрь 2024 - Март 2026", "period_en": "November 2024 - March 2026", "color": "lavender",
        "tasks_ru": "Разработка ML-пайплайна\nРаспознавание речи\nГенерация отчётов",
        "tasks_en": "ML pipeline development\nSpeech recognition\nReport generation",
        "tasks": [
            {
                "title_ru": "Разработка ML-пайплайна", "title_en": "ML pipeline development",
                "description_ru": "Спроектировал архитектуру интеллектуального ядра системы разбора инцидентов дежурной поддержки на базе гибридного ML-пайплайна. Объединил распознавание речи, обработку транскриптов и генерацию отчётов в последовательный процесс обработки созвонов.",
                "description_en": "Designed the architecture of the intelligent core for an on-call support incident analysis system based on a hybrid ML pipeline. Combined speech recognition, transcript processing and report generation into a sequential workflow for processing calls.",
            },
            {
                "title_ru": "Распознавание речи", "title_en": "Speech recognition",
                "description_ru": "Интегрировал Vosk для локальной транскрибации аудиопотоков созвонов в реальном времени. Реализовал обработку на CPU с минимальной задержкой: текст разговора поступал в систему по мере обсуждения инцидента.",
                "description_en": "Integrated Vosk for local, real-time transcription of call audio streams. Implemented low-latency CPU processing so that the conversation text entered the system as the incident was being discussed.",
            },
            {
                "title_ru": "Генерация отчётов", "title_en": "Report generation",
                "description_ru": "Реализовал Use-Case слой для буферизации транскриптов и группировки по сессиям. Подключил Groq API с моделью Llama-3 70B для формирования отчётов по материалам созвонов со скоростью более 200 токенов/с.",
                "description_en": "Implemented a use-case layer to buffer transcripts and group them by session. Integrated the Groq API with Llama-3 70B to generate reports from call transcripts at more than 200 tokens per second.",
            },
        ],
    },
]
