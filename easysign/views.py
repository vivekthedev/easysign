from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserChangeForm
from .models import User, Document 
from django.conf import settings
from dropbox_sign import Configuration, ApiClient, ApiException, apis
import openai
openai.api_key = settings.OPEN_AI_KEY


class Home(LoginRequiredMixin,TemplateView):
    template_name = 'easysign/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        
        configuration = Configuration(username=settings.DROPBOX_API_KEY)
        with ApiClient(configuration) as api_client:
            signature_request_api = apis.SignatureRequestApi(api_client)
            try:
                response = signature_request_api.signature_request_list()
                res = response.to_dict()
                documents = [(x["signature_request_id"], x["title"], x["signing_url"]) for x in res["signature_requests"]]
            except ApiException as e:
                print("Exception when calling Dropbox Sign API: %s\n" % e)
        context['documents'] = documents
        
        return context

class UserCreate(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/usercreation_form.html'
    success_url = '/'

class UserEdit(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "registration/userupdate_form.html"
    success_url = '/'

def process_doc(request, doc_id):
    try:
        doc = Document.objects.get(doc_id=doc_id)
    except :

        configuration = Configuration(username=settings.DROPBOX_API_KEY)

        with ApiClient(configuration) as api_client:
            signature_request_api = apis.SignatureRequestApi(api_client)

            signature_request_id = doc_id

            try:
                response = signature_request_api.signature_request_files(signature_request_id, file_type="pdf")
                from PyPDF2 import PdfReader
                file = PdfReader(response)
                content = [page.extract_text() for page in file.pages]
                doc = Document.objects.create(doc_id=doc_id, original_content='\n\n---\n\n'.join(content))
            except ApiException as e:
                print("Exception when calling Dropbox Sign API: %s\n" % e)
    return render(request, "easysign/text_document.html", {'doc':doc})


def get_text(request, action, doc_id):
    prompts = [
        "translate the give text in hindi {text}", 
        "translate the give text in spanish {text}", 
        "translate the give text in chinese {text}", 
        "summarize this content {text}"
    ]
    doc = Document.objects.get(doc_id=doc_id)
    if action == 0: content = doc.hindi_content    
    if action == 1: content = doc.spanish_content    
    if action == 2: content = doc.chinese_content    
    if action == 3: content = doc.summary
    print(content)   
    if not content:
        print("here")
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompts[action].format(text=doc.original_content)}
        ]
        )
        content = completion.choices[0].message["content"]
    if action == 0: doc.hindi_content = content   
    if action == 1: doc.spanish_content = content    
    if action == 2: doc.chinese_content = content   
    if action == 3: doc.summary = content
    doc.save()   
    return render(request, "easysign/ai_output.html", {'text':content})