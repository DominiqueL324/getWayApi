
from django.core.mail import send_mail

def envoyerEmail(titre,text,liste_destinataire,contenu_html):
    send_mail(
        titre,  #subject
        text, 
        "noreplyamexpert@amexpert.biz",#from_mail
        liste_destinataire,  #recipient list []
        fail_silently=True,  #fail_silently
        html_message="<p>"+text+"</p>"
    )