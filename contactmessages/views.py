from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import ContactMessage

@login_required(login_url='/panel/login/')
@role_required('admin')
def message_list(request):
    status_filter = request.GET.get('status', '')
    messages = ContactMessage.objects.all().order_by('-created_at')
    
    if status_filter in ['new', 'read', 'archived']:
        messages = messages.filter(status=status_filter)
        
    context = {
        'messages': messages,
        'current_status': status_filter
    }
    return render(request, 'panel/message_list.html', context)

@login_required(login_url='/panel/login/')
@role_required('admin')
def message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    
    if message.status == 'new':
        message.status = 'read'
        message.save()
        
    context = {
        'message': message
    }
    return render(request, 'panel/message_detail.html', context)

@login_required(login_url='/panel/login/')
@role_required('admin')
def message_archive(request, pk):
    if request.method == 'POST':
        message = get_object_or_404(ContactMessage, pk=pk)
        message.status = 'archived'
        message.save()
    return redirect('message_list')
