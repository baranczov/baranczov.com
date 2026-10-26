from django.conf import settings
from django.db.models import Prefetch
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_safe
from .copy import COPY
from .content import CONTACTS, EXPERIENCE_COVERS
from .models import Contact, Experience, ExperienceTask, Profile, Project, Technology

@require_safe
def root(request):
    language = request.COOKIES.get("portfolio_language", "ru")
    return redirect("home", language=language if language in COPY else "ru")

@require_safe
def home(request, language):
    if language not in COPY:
        raise Http404
    profile = Profile.objects.first() or Profile()
    # Supplied covers fill unconfigured slots without inventing roles or dates.
    records = list(Experience.objects.prefetch_related(Prefetch(
        "responsibilities", queryset=ExperienceTask.objects.filter(published=True), to_attr="visible_tasks",
    )))
    cover_by_company = {alias: cover for cover in EXPERIENCE_COVERS for alias in cover["aliases"]}
    configured_covers = {
        cover["image"] for record in records
        if (cover := cover_by_company.get(record.company.strip().casefold()))
    }
    # A hidden company must not reappear as a cover-only placeholder.
    pending_covers = iter(cover for cover in EXPERIENCE_COVERS if cover["image"] not in configured_covers)
    published_records = [record for record in records if record.published][:3]
    experiences = []
    for record in published_records + [None] * (3 - len(published_records)):
        cover = cover_by_company.get(record.company.strip().casefold()) if record else next(pending_covers, None)
        experiences.append({
            "record": record,
            "company": record.company if record else cover["company"] if cover else "",
            "cover": cover["image"] if cover else "",
        })
    contact_designs = {item["label"]: item for item in CONTACTS}
    resume = profile.cv_en if language == "en" else profile.cv
    resume_url = resume.url if resume else ""
    contact_tiles = []
    for contact in Contact.objects.filter(published=True):
        design = contact_designs.get(contact.label)
        if not design:
            continue
        is_resume = design["icon"] == "resume"
        contact_tiles.append({
            **design,
            "label": COPY[language]["resume"] if is_resume else contact.label,
            "url": resume_url if is_resume else contact.url,
            "image": f"images/contacts/{design['icon']}.svg" if not is_resume else "",
            "pending_label": COPY[language]["cv_pending" if is_resume else "contact_pending"],
        })
    response = render(request, "portfolio/home.html", {
        "language": language, "t": COPY[language], "site_url": settings.SITE_URL,
        "profile": profile,
        "resume_url": resume_url,
        "contact_tiles": contact_tiles,
        "experiences": experiences,
        "projects": Project.objects.filter(published=True),
        "technologies": Technology.objects.filter(published=True),
        "nav_ids": ["about", "experience", "projects", "stack", "contacts"],
        "pattern_rows": range(13), "pattern_repeats": range(8), "placeholder_cards": range(3),
    })
    response.set_cookie("portfolio_language", language, max_age=31536000, samesite="Lax", secure=not settings.DEBUG)
    response.headers["Content-Language"] = language
    return response

@require_safe
def health(request):
    return JsonResponse({"status": "ok"})

@require_safe
def robots(request):
    return HttpResponse(f"User-agent: *\nDisallow: /admin/\nSitemap: {settings.SITE_URL}/sitemap.xml\n", content_type="text/plain")

@require_safe
def sitemap(request):
    return render(request, "portfolio/sitemap.xml", {"site_url": settings.SITE_URL}, content_type="application/xml")

