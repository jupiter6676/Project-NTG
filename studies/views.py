from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    studies = Study.objects.all()

    context = {
        'studies': studies,
    }

    return render(request, 'studies/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        study_form = StudyForm(request.POST, request.FILES)

        if study_form.is_valid():
            study = study_form.save(commit=False)
            study.host_user = request.user
            study.save()

            List.objects.create(user=request.user, study=study, is_accepted=True)

            return redirect('studies:detail', study.pk)

    else:
        study_form = StudyForm()

    context = {
        'study_form': study_form,
    }

    return render(request, 'studies/create.html', context)


def detail(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)
    waiting_list = List.objects.filter(study=study, is_accepted=False)
    accepted_list = List.objects.filter(study=study, is_accepted=True)

    waiting_user_list = waiting_list.values_list('user', flat=True)
    accepted_user_list = accepted_list.values_list('user', flat=True)

    # print(accepted_user_list) # user_pk 쿼리셋

    context = {
        'study': study,
        'waiting_list': waiting_list,
        'accepted_list': accepted_list,
        'waiting_user_list': waiting_user_list,
        'accepted_user_list': accepted_user_list,
    }

    return render(request, 'studies/detail.html', context)


@login_required
def update(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user != study.host_user:
        return redirect('studies:index')

    if request.method == 'POST':
        study_form = StudyForm(request.POST, request.FILES, instance=study)

        if study_form.is_valid():
            study = study_form.save(commit=False)
            study.host_user = request.user
            study.save()

            return redirect('studies:detail', study.pk)

    else:
        study_form = StudyForm(instance=study)

    context = {
        'study_form': study_form,
    }

    return render(request, 'studies/create.html', context)


@login_required
def delete(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user == study.host_user and request.method == 'POST':
        study.delete()
        
    return redirect('studies:index')


# 스터디 모집 마감 & 재모집 (방장)
@login_required
def close(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user == study.host_user and request.method == 'POST':
        if study.is_closed == False:
            study.is_closed = True
            study.save()
        else:
            study.is_closed = False
            study.save()
            # messages.warning(request, '이미 모집이 마감된 스터디입니다.')

    return redirect('studies:detail', study_pk)


# 스터디 가입 신청 (방장 제외)
@login_required
def apply(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user != study.host_user and request.method == 'POST':
        if study.is_closed == False:
            user_pks = List.objects.values_list('user', flat=True)
            
            # 아직 신청하지 않았으면, 유저를 List에 추가
            if not request.user.pk in user_pks:
                List.objects.create(user=request.user, study=study)
        else:
            messages.warning(request, '이미 모집이 마감된 스터디입니다.')

    return redirect('studies:detail', study_pk)


# 스터디 가입 신청 취소 (방장 제외)
@login_required
def apply_cancel(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user != study.host_user and request.method == 'POST':
        list_user = List.objects.get(user=request.user, study=study)
        list_user.delete()

    return redirect('studies:detail', study_pk)


# 스터디 가입 신청 수락 (방장)
@login_required
def accept(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.user == study.host_user and request.method == 'POST':
        if study.is_closed == False:
            # 해당 유저의 가입 승인 여부를 True로
            list_user = List.objects.get(user=user, study=study)
            list_user.is_accepted = True
            list_user.save()

            # 수락 후 정원이 다 차면, 모집 마감
            accepted_list_cnt = List.objects.filter(study=study, is_accepted=True).count()
            if study.limit == accepted_list_cnt:
                study.is_closed = True
                study.save()

    return redirect('studies:detail', study_pk)


# 스터디 가입 신청 거절 (방장)
@login_required
def deny(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.user == study.host_user and request.method == 'POST':
        list_user = List.objects.get(user=user, study=study)
        list_user.delete()

    return redirect('studies:detail', study_pk)


# 스터디 추방 (방장)
@login_required
def kick(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.user == study.host_user and request.method == 'POST':
        list_user = List.objects.get(user=user, study=study)
        list_user.delete()

        accepted_list_cnt = List.objects.filter(study=study, is_accepted=True).count()
        study.limit == accepted_list_cnt
        # study.is_closed = False
        study.save()

    return redirect('studies:detail', study_pk)


# 스터디 탈퇴 (방장 제외)
@login_required
def withdraw(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    if request.user != study.host_user and request.method == 'POST':
        list_user = List.objects.get(user=request.user, study=study)
        list_user.delete()

        accepted_list_cnt = List.objects.filter(study=study, is_accepted=True).count()
        study.limit == accepted_list_cnt
        # study.is_closed = False
        study.save()

    return redirect('studies:detail', study_pk)