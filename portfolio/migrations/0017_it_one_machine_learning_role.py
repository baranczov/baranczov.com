from django.db import migrations


# Frozen copy approved from the owner's CV on 26 October 2026.
ROLE_AND_TASK_SUMMARIES = {'role_ru': 'Machine Learning Engineer',
 'role_en': 'Machine Learning Engineer',
 'tasks_ru': 'Подготовка текстовых данных\nОбучение NLP-модели\nИнтеграция инференса',
 'tasks_en': 'Text data preparation\nNLP model training\nInference integration'}

TASKS = [{'title_ru': 'Подготовка текстовых данных',
  'title_en': 'Text data preparation',
  'description_ru': 'Подготовил датасет обращений для автоматической классификации: очистил '
                    'тексты, удалил дубликаты, согласовал правила разметки. Сформировал обучающую, '
                    'валидационную и тестовую выборки с контролем утечек и анализом распределения '
                    'классов.',
  'description_en': 'Prepared a dataset of user requests for automatic classification: cleaned the '
                    'texts, removed duplicates and agreed on annotation guidelines. Created '
                    'training, validation and test splits with data leakage checks and analysis of '
                    'class distributions.'},
 {'title_ru': 'Обучение NLP-модели',
  'title_en': 'NLP model training',
  'description_ru': 'Дообучил RuBERT на PyTorch и Hugging Face Transformers; сравнил с baseline '
                    'TF-IDF и логистической регрессией. Оценивал macro-F1, precision и recall по '
                    'классам; анализировал ошибки, дисбаланс и влияние параметров обучения.',
  'description_en': 'Fine-tuned RuBERT using PyTorch and Hugging Face Transformers; compared it '
                    'with a TF-IDF and logistic regression baseline. Evaluated macro-F1 and '
                    'per-class precision and recall; analyzed errors, class imbalance and the '
                    'impact of training parameters.'},
 {'title_ru': 'Интеграция инференса',
  'title_en': 'Inference integration',
  'description_ru': 'Разработал API классификации на FastAPI, упаковал модель в Docker и '
                    'подготовил интеграцию с backend. Реализовал пакетную обработку, логирование '
                    'предсказаний и замеры p95 задержки и пропускной способности сервиса.',
  'description_en': 'Developed a classification API with FastAPI, packaged the model in Docker and '
                    'prepared integration with the backend. Implemented batch processing, '
                    'prediction logging and measurements of p95 latency and service throughput.'}]


def update_it_one(apps, schema_editor):
    alias = schema_editor.connection.alias
    Experience = apps.get_model("portfolio", "Experience")
    ExperienceTask = apps.get_model("portfolio", "ExperienceTask")
    for experience in Experience.objects.using(alias).filter(company="IT_ONE"):
        tasks = list(ExperienceTask.objects.using(alias).filter(
            experience_id=experience.pk,
        ).order_by("position", "pk"))
        if len(tasks) != len(TASKS):
            raise RuntimeError("Expected three IT_ONE tasks; review the current content before updating.")
        Experience.objects.using(alias).filter(pk=experience.pk).update(**ROLE_AND_TASK_SUMMARIES)
        for task, content in zip(tasks, TASKS):
            ExperienceTask.objects.using(alias).filter(pk=task.pk).update(**content)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0016_data_processing_technologies")]
    operations = [migrations.RunPython(update_it_one, migrations.RunPython.noop)]
