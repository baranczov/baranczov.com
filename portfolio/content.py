"""Owner-approved portfolio copy, used as defaults for a new installation."""

BIO_RU = (
    "Занимаюсь **прикладным ML, NLP и production-пайплайнами**. "
    "Учусь в двух университетах: **Центральном университете** по направлению «Искусственный интеллект» "
    "и **НИУ ВШЭ** на программе «Прикладная математика и информатика» ФКН. "
    "Имею **более двух лет коммерческого опыта.** "
    "**Победитель регионального этапа ВсОШ по математике и Всесибирской открытой олимпиады школьников**, "
    "призёр «Дататона 2.0» от Т-Банка. Обладаю **аналитическим мышлением**, быстро осваиваю новое, "
    "внимательно отношусь к деталям и **довожу задачи до результата**."
)

BIO_EN = (
    "I work on **applied ML, NLP and production pipelines**. "
    "I study at two universities: Artificial Intelligence at **Central University** and Applied Mathematics "
    "and Informatics at **HSE University**'s Faculty of Computer Science. "
    "I have **over two years of commercial experience.** I am a **winner of the regional stage of the "
    "All-Russian Olympiad for School Students in Mathematics and the All-Siberian Open Olympiad for "
    "School Students**, and a prize winner of T-Bank's Datathon 2.0. I **think analytically**, learn quickly, "
    "pay close attention to detail, and **see tasks through to completion**."
)

EXPERIENCE_COVERS = [
    {"company": "Т-Банк", "image": "images/experience/t-bank.svg", "aliases": ("т-банк", "т банк", "t-bank", "tbank")},
    {"company": "IT_ONE", "image": "images/experience/it-one.svg", "aliases": ("it_one", "it one", "it.one", "itone")},
    {"company": "ВкусВилл", "image": "images/experience/vkusvill.svg", "aliases": ("вкусвилл", "вкусвил", "vkusvill")},
]

TECHNOLOGIES = [
    {
        "title_ru": "Classic ML", "title_en": "Classic ML", "color": "gray",
        "items_ru": "Python, NumPy, Pandas, scikit-learn, CatBoost, LightGBM, Optuna, анализ данных, предобработка данных, feature engineering, ансамбли моделей, кросс-валидация, SHAP.",
        "items_en": "Python, NumPy, Pandas, scikit-learn, CatBoost, LightGBM, Optuna, data analysis, data preprocessing, feature engineering, model ensembles, cross-validation, SHAP.",
    },
    {
        "title_ru": "MLOps", "title_en": "MLOps", "color": "blue",
        "items_ru": "Docker, Git, GitLab CI/CD, Apache Airflow, Spark/PySpark, Hive, HDFS, S3, Model Registry, Linux, автоматизация обучения и инференса, тестирование ML-пайплайнов, мониторинг моделей.",
        "items_en": "Docker, Git, GitLab CI/CD, Apache Airflow, Spark/PySpark, Hive, HDFS, S3, Model Registry, Linux, training and inference automation, ML pipeline testing, model monitoring.",
    },
    {
        "title_ru": "Frontend", "title_en": "Frontend", "color": "lavender",
        "items_ru": "HTML, CSS, JavaScript, TypeScript, React, адаптивная вёрстка, REST API, визуализация данных, npm, Vite.",
        "items_en": "HTML, CSS, JavaScript, TypeScript, React, responsive layouts, REST API, data visualization, npm, Vite.",
    },
    {
        "title_ru": "Backend", "title_en": "Backend", "color": "gray",
        "items_ru": "Python, Flask, FastAPI, SQL, PostgreSQL, ClickHouse, Kafka, REST API, клиент-серверная архитектура, интеграция внешних сервисов, тестирование, Docker.",
        "items_en": "Python, Flask, FastAPI, SQL, PostgreSQL, ClickHouse, Kafka, REST API, client-server architecture, external service integration, testing, Docker.",
    },
    {
        "title_ru": "Deep Learning", "title_en": "Deep Learning", "color": "blue",
        "items_ru": "Python, PyTorch, нейронные сети, NLP, эмбеддинги, трансформеры, LLM, мультимодальные модели, обучение на GPU, распознавание речи.",
        "items_en": "Python, PyTorch, neural networks, NLP, embeddings, transformers, LLMs, multimodal models, GPU training, speech recognition.",
    },
    {
        "title_ru": "Математика", "title_en": "Mathematics", "color": "lavender",
        "items_ru": "Линейная алгебра, математический анализ, теория вероятностей, математическая статистика, дискретная математика, методы оптимизации, проверка гипотез, A/B-тестирование.",
        "items_en": "linear algebra, calculus, probability theory, mathematical statistics, discrete mathematics, optimization methods, hypothesis testing, A/B testing.",
    },
]

CONTACTS = [
    {"label": "GitHub", "url": "https://github.com/baranczov", "icon": "github", "width": 157, "height": 157},
    {"label": "Kaggle", "url": "https://www.kaggle.com/danilbarantsov", "icon": "kaggle", "width": 200, "height": 77},
    {"label": "Gmail", "url": "mailto:dbaranczov@gmail.com", "icon": "gmail", "width": 148, "height": 118},
    {"label": "Telegram", "url": "https://t.me/baranczov", "icon": "telegram", "width": 153, "height": 153},
    {"label": "Instagram", "url": "https://www.instagram.com/baranczov/", "icon": "instagram", "width": 156, "height": 156},
    {"label": "Phone Number (CV)", "url": "", "icon": "resume"},
    {"label": "LinkedIn", "url": "", "icon": "linkedin", "width": 140, "height": 140},
]
