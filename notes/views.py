from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
# Create your views here.


@login_required
def index(request):
    # notes = request.user.user_to.order_by("-created_at")
    notes = Notes.objects.filter(to_user_id=request.user.id, garbage=False).order_by(
        "-created_at"
    )
    notes_counter= Notes.objects.filter(read=0).count()
    context = {
        "notes": notes,
        # "notes_counter":notes_counter,
    }
    print(notes_counter)
    return render(request, "notes/index.html", context)


@login_required
def sent(request):
    # to_notes = request.user.user_from.order_by("-created_at")
    to_notes = Notes.objects.filter(from_user_id=request.user.id, garbage=False).order_by(
        "-created_at"
    )
    context = {
        "to_notes":to_notes,
    }
    return render(request, "notes/index.html", context)


@login_required
def send(request):
    form = NotesForm(request.POST or None)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.from_user = request.user
        temp.save()
        if temp.to_user.note_notice:
            temp.to_user.notice_note = False
            temp.to_user.save()
        return redirect("notes:index")

    context = {
        "form": form,
    }
    return render(request, "notes/send.html" , context)


@login_required
def detail(request, pk):
    note = get_object_or_404(Notes,pk=pk)
    if request.user == note.to_user:
        if not note.read:
            note.read =True
            note.save()
        if not request.user.user_to.filter(read=False).exists():
            request.user.notice_note = True
            request.user.save()
        return render(request,"notes/detail.html",{"note":note})
    elif request.user == note.from_user:
        return render(request,"notes/detail.html",{"note":note})
    else:
        return redirect("notes:index")


@login_required
def delete(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    note.delete()

    context={
        "is_deleted":True
    }
    return JsonResponse(context)


@login_required
def trash_throw_away(request, pk):
    note = Notes.objects.get(pk=pk)
    note.garbage = True
    note.save()
    return redirect("notes:index")


@login_required
def trash_return(request, pk):
    note = Notes.objects.get(pk=pk)
    note.garbage = False
    note.save()
    return redirect("notes:trash")


@login_required
def trash(request):
    trash_notes = Notes.objects.filter(to_user_id=request.user.id, 
    garbage=True).order_by("-created_at")
    print(trash_notes)
    context = {
        "notes": trash_notes,
    }
    return render(request, "notes/trash.html", context)


@login_required
def important_check(request, pk):
    note = Notes.objects.get(pk=pk)
    note.important = True
    note.save()
    return redirect("notes:index")


@login_required
def important_return(request, pk):
    note = Notes.objects.get(pk=pk)
    note.important = False
    note.save()
    return redirect("notes:index")


@login_required
def important(request):
    important_notes = Notes.objects.filter(to_user_id=request.user.id, 
    garbage=False, important=True).order_by("-created_at")
    context = {
        "notes": important_notes,
    }
    return render(request, "notes/important.html", context)