from django.shortcuts import render, redirect

from .models import Topic, Entry
from  .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """显示所有的主题"""
    topics_data = Topic.objects.order_by('date_added')
    context = {'topics': topics_data}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic_data = Topic.objects.get(id=topic_id)
    entries = topic_data.entry_set.order_by('-date_added')
    context = {'topic': topic_data, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # 显示空表格或指出表单数据无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """在特定主题中添加新条目"""
    topic_data = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据：创建一个空表单
        form = EntryForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_data = form.save(commit=False)
            new_entry_data.topic = topic_data
            new_entry_data.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # 显示空表单或指出表单数据无效
    context = {'form': form, 'topic': topic_data}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry_data = Entry.objects.get(id=entry_id)
    topic_date = entry_data.topic

    if request.method != 'POST':
        # 初次请求：使用当前条目填充表单
        form = EntryForm(instance=entry_data)
    else:
        # POST 提交的数据：对数据进行处理
        form = EntryForm(instance=entry_data, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic_date.id)

    context = {'form': form, 'entry': entry_data, 'topic': topic_date}
    return render(request, 'learning_logs/edit_entry.html', context)