from csv import reader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Blog, Entry, File
from .forms import EntryForm, UploadEntryFile
from django.utils import timezone


# views for crete, view and edit blog model
class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'app_blogs/blog_list.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = self.model.objects.filter(user_id=user_id)
        return queryset


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    fields = ['name', 'tags']
    template_name = 'app_blogs/new-blog.html'
    success_url = reverse_lazy('blog-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BlogEditView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    fields = ['name', 'tags']
    template_name = 'app_blogs/blog_edit.html'
    success_url = reverse_lazy('blog-list')


class BlogDetailView(LoginRequiredMixin, generic.DetailView):
    model = Blog
    template_name = 'app_blogs/entry_list.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry_list = self.object.entries.all()
        context['entry_list'] = entry_list
        return context


# view to create, edit entries
class EntryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'app_blogs/new_entry.html'

    def get_success_url(self):
        return reverse('entry-list', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        blog_id = self.kwargs.get('pk')
        blog = Blog.objects.get(id=blog_id)
        form.instance.blog = blog
        entry = form.save()
        files = self.request.FILES.getlist('file')
        description = form.cleaned_data.get('description')
        for item in files:
            file_model = File(entry=entry, file=item, description=description)
            file_model.save()
        return super().form_valid(form)


class EntryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Entry
    template_name = 'app_blogs/entry_detail.html'
    context_object_name = 'entry'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.object
        files = entry.files.all()
        context['files'] = files
        return context


class EntryEditView(LoginRequiredMixin, generic.UpdateView):
    model = Entry
    template_name = 'app_blogs/entry_edit.html'
    form_class = EntryForm

    def get_success_url(self):
        return reverse_lazy('detail-entry', args=[self.object.pk])

    def form_valid(self, form):
        entry = self.object
        entry.mod_date = timezone.now()
        files = self.request.FILES.getlist('file')
        description = form.cleaned_data.get('description')
        for item in files:
            file_model = File(entry=entry, file=item, description=description)
            file_model.save()
        return super().form_valid(form)


class MainPageView(generic.ListView):
    model = Entry
    template_name = 'app_blogs/entry_all.html'
    context_object_name = 'entry_list'


def upload_entry_from_file(request, pk):
    if request.method == 'POST':
        form = UploadEntryFile(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get('file').read()
            file = file.decode('utf-8').split('\n')
            csv_reader = reader(file, quotechar='"')
            for row in csv_reader:
                if row:  # if not empty line
                    # check if entry with title does not already exist
                    entry, created = Entry.objects.get_or_create(
                        title=row[0],
                        defaults={"blog_id": pk, "body_text": row[1]})
            return redirect(reverse('entry-list', args=[pk]))
    else:
        form = UploadEntryFile()
    return render(request, 'app_blogs/upload_entry_file.html',
                  {'form': form})
