from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Entry, User
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import Q



def index(request):
    if request.user.is_authenticated:
        topics_as_creator_ids = Topic.objects.filter(creator=request.user).values_list('id', flat=True)
        entries_created_ids = Entry.objects.filter(creator=request.user).values_list('topic_id', flat=True)
        entries_as_collaborator_ids = Entry.objects.filter(collaborators=request.user).values_list('topic_id', flat=True)
        all_topic_ids = set(topics_as_creator_ids) | set(entries_created_ids) | set(entries_as_collaborator_ids)
        all_user_topics = Topic.objects.filter(id__in=all_topic_ids).distinct()

        context = {'topics': all_user_topics}
        return render(request, 'structure/index.html', context)
    else:
        return render(request,'structure/index.html')    

def topics(request):
    """Mostra todos os assuntos"""	
    topics = Topic.objects.order_by('date_added')
    context = {'topics':topics}
    return render(request,'structure/topics.html',context)

def topic(request,topic_id):
    """Mostra um unico assunto e todas as suas entradas"""	
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entry_set.filter(
        Q(creator=request.user) | Q(collaborators=request.user)
    )
    context = {'topic':topic,'entries':entries}
    return render(request,'structure/topic.html',context)

def new_topic(request):
    """"Adiciona novo assunto"""
    if request.method != 'POST':
        #Nenhum dado submetido; cria um formulario em branco
        form = TopicForm()
    else:
        #Dados de POST submetidos; processa os dados
          form = TopicForm(request.POST)
          if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.creator = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {'form':form}
    return render(request,'structure/new_topic.html',context)

def new_entry(request, topic_id):
    """Acrescenta uma nova entrada para um assunto especifico"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco
        form = EntryForm()
    else:
        # Dados de POST submetidos; processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.creator = request.user  # Definindo o usuário como criador
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'structure/new_entry.html', context)


def view_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.user != entry.creator and request.user not in entry.collaborators.all():
        raise Http404

    context = {'entry': entry}
    return render(request, 'topic.html', context)

def edit_entry(request, entry_id):
    """Deleta uma entrada existente"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # Verifica se o usuário tem permissão para editar
    if request.user != entry.creator:
        raise Http404
    if request.method == 'POST':
        if 'add_collaborator' in request.POST:
            user_id = request.POST.get('user_id')
            user_to_add = User.objects.get(id=user_id)
            entry.collaborators.add(user_to_add)
            return redirect('edit_entry', entry_id=entry_id)

        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    else:
        form = EntryForm(instance=entry)

    users_not_collaborators = User.objects.exclude(
        id__in=entry.collaborators.all()
    ).exclude(id=entry.creator.id)

    context = {'entry': entry, 'topic': topic, 'form': form, 'users': users_not_collaborators}
    return render(request, 'structure/edit_entry.html', context)

def delete_entry(request,entry_id):
    """Deleta uma entrada existente"""	
    entry = Entry.objects.get(id=entry_id)
    entry.delete()
    return HttpResponseRedirect(reverse('topic',args=[entry.topic.id]))

def add_collaborator(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        entry.collaborators.add(user)
        if entry.group:
            entry.group.user_set.add(user)
        entry.save()
        return redirect('edit_entry', entry_id=entry_id)

    return redirect('edit_entry', entry_id=entry_id)
 

def remove_collaborator(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        entry.collaborators.remove(user)
        if entry.group:
            entry.group.user_set.remove(user)
        entry.save()
        return redirect('edit_entry', entry_id=entry_id)

    return redirect('edit_entry', entry_id=entry_id)

def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, creator=request.user)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topics')
    else:
        form = TopicForm(instance=topic)
    return render(request, 'structure/edit_topic.html', {'form': form, 'topic': topic})


def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, creator=request.user)
    if request.method == 'POST':
        topic.delete()
        return redirect('topics')
    return render(request, 'structure/delete_topic.html', {'topic': topic})
