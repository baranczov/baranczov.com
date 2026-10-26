from django.core.validators import FileExtensionValidator
from django.db import models
from .validators import validate_contact_url, validate_upload_size
from .content import BIO_EN, BIO_RU

def image_field(folder, **kwargs):
    return models.ImageField(upload_to=folder, blank=True, validators=[validate_upload_size, FileExtensionValidator(["jpg", "jpeg", "png", "webp"])], **kwargs)

class Profile(models.Model):
    first_name_ru = models.CharField("Имя RU", max_length=80, default="Данил")
    first_name_en = models.CharField("Имя EN", max_length=80, default="Danil")
    last_name_ru = models.CharField("Фамилия RU", max_length=80, default="Баранцов")
    last_name_en = models.CharField("Фамилия EN", max_length=80, default="Baranczov")
    bio_ru = models.TextField("О себе RU", blank=True, default=BIO_RU, help_text="Выделение жирным и синим: **текст**.")
    bio_en = models.TextField("О себе EN", blank=True, default=BIO_EN, help_text="Выделение жирным и синим: **текст**.")
    portrait = image_field("portrait/", verbose_name="Фотография")
    cv = models.FileField("Резюме PDF RU", upload_to="cv/", blank=True, validators=[validate_upload_size, FileExtensionValidator(["pdf"])])
    cv_en = models.FileField("Резюме PDF EN", upload_to="cv/", blank=True, validators=[validate_upload_size, FileExtensionValidator(["pdf"])])

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профиль"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name_ru} {self.last_name_ru}"

class OrderedModel(models.Model):
    position = models.PositiveIntegerField("Порядок", default=0)
    published = models.BooleanField("Опубликовано", default=True)

    class Meta:
        abstract = True
        ordering = ["position", "pk"]

class Experience(OrderedModel):
    company = models.CharField("Компания", max_length=100)
    role_ru = models.CharField("Должность RU", max_length=120)
    role_en = models.CharField("Должность EN", max_length=120)
    tasks_ru = models.TextField("Задачи RU", blank=True, help_text="Одна задача на строку.")
    tasks_en = models.TextField("Задачи EN", blank=True, help_text="Одна задача на строку.")
    period_ru = models.CharField("Период RU", max_length=120, blank=True)
    period_en = models.CharField("Период EN", max_length=120, blank=True)
    image = image_field("experience/", verbose_name="Лицевая сторона")
    color = models.CharField("Цвет карточки", max_length=10, choices=[("yellow", "Жёлтый"), ("blue", "Синий"), ("gray", "Серый"), ("lavender", "Лавандовый")], default="yellow")

    class Meta(OrderedModel.Meta):
        verbose_name = "место работы"
        verbose_name_plural = "рабочий опыт"

    def __str__(self):
        return self.company

class ExperienceTask(OrderedModel):
    experience = models.ForeignKey(Experience, related_name="responsibilities", on_delete=models.CASCADE)
    title_ru = models.CharField("Название RU", max_length=160)
    title_en = models.CharField("Название EN", max_length=160)
    description_ru = models.TextField("Описание RU", blank=True)
    description_en = models.TextField("Описание EN", blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "задача"
        verbose_name_plural = "задачи"

    def __str__(self):
        return self.title_ru

class Project(OrderedModel):
    title_ru = models.CharField("Название RU", max_length=160)
    title_en = models.CharField("Название EN", max_length=160)
    description_ru = models.TextField("Описание RU", blank=True)
    description_en = models.TextField("Описание EN", blank=True)
    image = image_field("projects/", verbose_name="Обложка")
    color = models.CharField("Цвет карточки", max_length=10, choices=[("lavender", "Лавандовый"), ("blue", "Синий"), ("gray", "Серый")], default="lavender")
    url = models.URLField("Ссылка на проект", blank=True)
    github_url = models.URLField("GitHub", max_length=500, blank=True)
    kaggle_url = models.URLField("Kaggle", max_length=500, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __str__(self):
        return self.title_ru

class Technology(OrderedModel):
    title_ru = models.CharField("Название RU", max_length=100)
    title_en = models.CharField("Название EN", max_length=100)
    items_ru = models.TextField("Технологии RU", blank=True, help_text="Перечислите технологии через запятую.")
    items_en = models.TextField("Технологии EN", blank=True)
    color = models.CharField("Цвет", max_length=10, choices=[("gray", "Серый"), ("blue", "Синий"), ("lavender", "Лавандовый")])

    class Meta(OrderedModel.Meta):
        verbose_name = "категория технологий"
        verbose_name_plural = "технологический стек"

    def __str__(self):
        return self.title_ru

class Contact(OrderedModel):
    label = models.CharField("Название", max_length=80, unique=True)
    url = models.CharField("Ссылка", max_length=500, blank=True, validators=[validate_contact_url])

    class Meta(OrderedModel.Meta):
        verbose_name = "контакт"
        verbose_name_plural = "контакты"

    def __str__(self):
        return self.label

