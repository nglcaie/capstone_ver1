import email
from multiprocessing import context
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import *
from .forms import *
from datetime import datetime
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
import os
from django.conf import settings
# Create your views here.
#integrate topic modeling
#Step 3
import re
import numpy as np
import pandas as pd
from pprint import pprint
import string

#NLTK
import nltk
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 

#Gensim
#!pip install gensim
import gensim
from gensim.parsing.preprocessing import STOPWORDS
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models.phrases import Phrases

#Spacy for lemmatization
#!pip install spacy
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim_models
#!pip install matplotlib
import matplotlib.pyplot as plt

import os

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

 
def index(request):
    return render(request, 'landing.html')
 
def loginPage(request):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('student_list')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('start_survey')
    else:
        if request.method == 'POST':
            email = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                users = request.user
                if user.is_authenticated and users.is_admin:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('student_list')
                elif user.is_authenticated and users.is_student:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('start_survey')
                else:
                    messages.error (request,'You have entered an invalid email or password.')
                    return render(request, 'login.html')
            else:
                    messages.error (request,'You have entered an invalid email or password.')
                    return render(request, 'login.html')
    return render(request, 'login.html')
 
def logout_view(request):
    logout(request)
    return redirect('login')
 
def sign_upPage(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = RegisterForm(request.POST,initial={'is_student': True})
        if form.is_valid():
            x = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save()
            messages.success(request, "Student account has been successfully created.")
            return redirect('login')
        else:
            context['register'] = form
    else:
        form = RegisterForm(initial={'is_student': True})
        context['register'] = form
    return render(request, 'sign_up.html', context)
 
def student_navbar(request):
    user = request.user.id
    student = User.objects.get(id=user)
    print(student)
    context = {'student':student}
    return render(request, 'student/student_navbar.html',context)
 
def answer_summary(request):
    context ={}
    user = request.user.id
    if Answers.objects.filter(student=user).exists():
        answers = Answers.objects.filter(student=user)
        context['answers'] = answers
    else:
        return redirect('start_survey')
    return render(request, 'student/answer_summary.html', context)
 
def start_survey(request):
    user = request.user.id
    if Answers.objects.filter(student=user).exists():
        return redirect('thankyou')
    else:
        return render(request, 'student/start_survey.html')
 
def survey_question(request):
    context ={}
    alluser = User.objects.all
    user = request.user.id
    gets = User.objects.get(id=user)
    if request.POST:
        form = AnswerForm(request.POST,initial={'student': user})
        if form.is_valid():
            x = form.save()
            gets.has_answer = 1
            gets.save()
            return redirect('thankyou')
        else:
            context['register'] = form
    else:
        form = AnswerForm(initial={'student': user})
        context['register'] = form
    return render(request, 'student/survey_question.html', context)
 
def thankyou(request):
    return render(request, 'student/thankyou.html')

def admin_navbar(request):
    return render(request, 'admin/admin_navbar.html')

def evaluation(request):
    df = pd.read_csv('D:\Pia\Downloads\capstone\cleanedDataset.csv')
    df['q1']=df['question1'].astype(str) #convert type to string
    df['q1']=df['q1'].apply(lambda x: x.lower()) #all lowercase

    #!!CONTRACTION DICTIONARY CAN REMOVE OR ADD!!
    #!!CONTRACTION DICTIONARY CAN REMOVE OR ADD!!
    contractions_dict = {"its":"it is","it's":"it is","im":"i am","i'm":"i am","can't":"cannot","sometimes":"sometimes","don't":"do not","dont":"do not",
                        "hardtime":"hard time","time":"time",'overstimulate':"overstimulate","stimulating":"stimulating","i've":"i have","doesnt":"does not",
                        "doesn't":"does not","distracted":"distracted","limited":"limited","minimal":"minimal","a lot":"alot","set up":"setup",
                        "set-up":"setup","couldn":"could not","couldnt":"could not","couldn't":"could not","a bit":"little bit","wont":"would not",
                        "there's":"there is","won't":"would not"}

    # Regular expression for finding contractions
    contractions_re=re.compile('(%s)' % '|'.join(contractions_dict.keys()))

    def expand_contractions(text,contractions_dict=contractions_dict):
        def replace(match):
            return contractions_dict[match.group(0)]
        return contractions_re.sub(replace, text)

    # Expanding Contractions in the reviews
    df['q1']=df['q1'].apply(lambda x:expand_contractions(x))

    data = df.q1.values.tolist()
    def remove_punctuation(text):
        no_punct=[words for words in text if words not in string.punctuation]
        words_wo_punct=''.join(no_punct)
        return words_wo_punct

    def tokenization(inputs):
        return word_tokenize(inputs)

    df['q1']=df['q1'].apply(lambda x:expand_contractions(x))

    data = df.q1.values.tolist()

    df['q1']=df['q1'].apply(lambda x:remove_punctuation(x))
    df['q1']=df['q1'].apply(lambda x:tokenization(x))


    lemmatizer = WordNetLemmatizer()

    def lemmatization(inputs):
        return [lemmatizer.lemmatize(word=x, pos='v') for x in inputs]

    df['q1']=df['q1'].apply(lambda x:lemmatization(x))

    data_words = df.q1.values.tolist()
    #print(data_words[:2]) 

    #GENSIM STOPWORDS
    stop_words = STOPWORDS
    #for addition of stopwords
    stop_words = STOPWORDS.union(set(['yes','tree','know','way','cause','specially','especially','create','keep','come','ung','make','plenty','schedule','become','like','also','able','currently','really','have','lot','nan','pass','go','sa', 'na', 'ko', 'yung', 'hindi', 'ng', 'kasi', 'ako', 'pa','gusto', 
            'una', 'tungkol', 'ibig', 'kahit', 'nabanggit', 'huwag', 'nasaan', 'tayo', 'napaka', 'iyo', 'nakita', 'pataas', 'may', 'pagkatapos', 
            'anumang', 'lima', 'ibabaw', 'habang', 'at', 'tulad', 'nilang', 'pa', 'doon', 'ay', 'ngayon', 'akin', 'masyado', 'dito', 'din', 
            'likod', 'pangalawa', 'katiyakan', 'maaari', 'pero', 'bakit', 'pagitan', 'niya', 'kaya', 'makita', 'hanggang', 'paraan', 'siya',
            'para', 'kapag', 'ang', 'kapwa', 'kong', 'panahon', 'kanya', 'mula', 'kanila', 'bababa', 'kailangan', 'dahil', 'iyong', 'marapat',
            'sila', 'ginawang', 'ni', 'ako', 'kumuha', 'karamihan', 'gumawa', 'noon', 'muli', 'ating', 'mismo', 'ng', 'lahat', 'palabas',
            'hindi', 'niyang', 'kanilang', 'pumupunta', 'ito', 'lamang', 'apat', 'marami', 'iyon', 'sa', 'o', 'sabi', 'kanino', 'ginawa',
            'narito', 'bilang', 'saan', 'alin', 'gagawin', 'mahusay', 'namin', 'ilagay', 'nagkaroon', 'isa', 'ibaba', 'ilalim', 'ko', 'na',
            'naging', 'minsan', 'iba', 'dalawa', 'paano', 'pagkakaroon', 'aming', 'maging', 'atin', 'sabihin', 'nais', 'pamamagitan', 'ilan',
            'pumunta', 'kung', 'paggawa', 'amin', 'am', 'sarili', 'nito', 'dapat', 'sino', 'walang', 'bago', 'ano', 'nila', 'tatlo', 'kanyang',
            'itaas', 'kaysa', 'gayunman', 'laban', 'isang', 'pababa', 'mayroon', 'kulang', 'aking', 'ka', 'maaaring', 'pareho', 'kami',
            'kailanman', 'ginagawa', 'mga', 'katulad', 'ikaw', 'inyong', 'bawat', 'kay', 'lang', 'yung', 'yan', 'iyan', 'di', 'niya',
            'nya', 'ba', 'mong', 'mo', 'naman', 'kayo', 'di', 'ur', 'ano', 'anu','po','sakin','nag','pag']))
    sw_list = {'cannot','not','do','can','should','would','very','much','too','lot','alot','really','to','sometimes','of','does'}
    #for removing the stopwords from the list
    stop_words = stop_words.difference(sw_list)

    def stopwords_remove(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


    # deacc=True removes punctuations
    # Step 9

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=2, threshold=2) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=2)  
    quadgram = gensim.models.Phrases(trigram[data_words], threshold=2)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    quadram_mod = gensim.models.phrases.Phraser(quadgram)

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    def make_quadrams(texts):
        return [quadram_mod[trigram_mod[bigram_mod[doc]]] for doc in texts]


    data_words_stopwords = stopwords_remove(data_words)


    data_words_bigrams = make_bigrams(data_words_stopwords)

    # Form Trigrams
    data_words_trigrams = make_trigrams(data_words_bigrams)

    data_words_quadrams = make_quadrams(data_words_trigrams)

    stop_words_improve = STOPWORDS
    #ADDING STOPWORDS
    #sw_list_imp = ['need_to','used_to']
    #ADDING STOPWORDS
    stop_words_improve = STOPWORDS.union(set(['need_to','used_to','theres_alot_of','hard_to','of_time','alot_of','have_choice','do_not','do_not_have',
                                            'to_do','use_to','need_to_do','nott','really_can_not','have_no','have_to_do','use_to','ampact','can_not','lack_of',
                                            'do_not_feel','of_distractions','motivation_to','of_distraction','have_to','tend_to','of_course',
                                            'to_focus','term_of','ability_to']))

    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words_improve] for doc in texts]

    improve_stop_words = remove_stopwords(data_words_quadrams)

    # Create Dictionary
    id2word = corpora.Dictionary(improve_stop_words)

    # Create Corpus
    texts = improve_stop_words

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # View
    corps = [[(id2word[id], freq) for id, freq in cp] for cp in corpus]

    lda_model20 = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=20, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=20,
                                           alpha='auto',
                                           per_word_topics=True)
    topics = lda_model20.print_topics()
    doc_lda = lda_model20[corpus]
    x=1
    return render(request, 'admin/evaluation.html',{'topics':topics,'x':x})
 
def student_list(request):
    ans = Answers.objects.all()
    print(ans)
    stud = User.objects.filter(is_student=True, has_answer=True)
    context = {'stud':stud}
    return render(request,'admin/student_list.html', context)
    
def student_answer(request, pk):
    answers = Answers.objects.filter(id=pk)
    context = {'answers':answers}
    return render(request, 'admin/student_answer.html', context)
 
def load_slot(request):
    collegeId = request.GET.get('college_Id')
    course = Course.objects.filter(college=collegeId)
    return render(request, 'student/dropdown_option.html', {'course': course})