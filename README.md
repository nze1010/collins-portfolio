# Portfolio Website (Django)

A 4-page portfolio site built with Django: Homepage, Skills, Blog (full CRUD), and Contact.

## How each requirement is met

- **Homepage** — `main/views.py::home` — shows a preview of skills + latest blog posts.
- **Skills Page** — Skills are model objects (`main/models.py::Skill`) managed entirely
  from `/admin/`. The `skill_list` view just reads them and the template displays them —
  no skill is ever hardcoded in a template.
- **Contact Page** — `ContactForm` in `main/forms.py` is a `ModelForm` tied to the
  `ContactMessage` model. The `contact` view in `views.py` validates the POSTed data and
  calls `form.save()`, which writes the name/email/subject/message straight to the DB.
- **Blog Page (CRUD)** —
  - Create: `blog_create` view + `BlogPostForm`
  - Read: `blog_list` (all posts) and `blog_detail` (single post)
  - Update: `blog_update` — same `BlogPostForm`, passed `instance=post`
  - Delete: `blog_delete` — shows a confirm page, deletes on POST

## Project structure

```
portfolio_project/
├── manage.py
├── portfolio_project/      # project settings, root urls.py
└── main/                   # the app with everything for this assignment
    ├── models.py           # Skill, BlogPost, ContactMessage
    ├── forms.py            # ContactForm, BlogPostForm
    ├── views.py            # all 4 pages + CRUD logic
    ├── admin.py            # registers models so you can manage them in /admin/
    ├── urls.py             # app routes
    ├── templates/main/     # all HTML templates
    └── static/main/style.css
```

## Running it locally

1. Create a virtual environment and install Django + Pillow:
   ```
   pip install django pillow
   ```
2. From the `portfolio_project` folder (the one with `manage.py`), run migrations:
   ```
   python manage.py migrate
   ```
3. Create an admin account so you can add skills from the dashboard:
   ```
   python manage.py createsuperuser
   ```
4. Start the server:
   ```
   python manage.py runserver
   ```
5. Visit:
   - `http://127.0.0.1:8000/` — homepage
   - `http://127.0.0.1:8000/admin/` — log in and add your Skills here first
   - `http://127.0.0.1:8000/skills/` — your skills will now show up here
   - `http://127.0.0.1:8000/blog/` — create/edit/delete blog posts
   - `http://127.0.0.1:8000/contact/` — submit the form, then check
     `/admin/` → Contact messages to see it landed in the DB

## Notes for next steps (optional polish)

- Add `django.contrib.messages` styling tweaks if you want different colors per message type.
- If you want image uploads on blog posts too, add an `ImageField` to `BlogPost` the same
  way it's done on `Skill`, then add `enctype="multipart/form-data"` to `blog_form.html`'s
  `<form>` tag and pass `request.FILES` into `BlogPostForm(request.POST, request.FILES)`
  in the view.
- Right now anyone can create/edit/delete blog posts — if your course wants only logged-in
  users to manage the blog, wrap `blog_create`, `blog_update`, `blog_delete` with Django's
  `@login_required` decorator.
