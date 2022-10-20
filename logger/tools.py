
from django.core.mail import send_mail

def envoyerEmail(titre,text,liste_destinataire,contenu_html):
    final_ =[]
    for dest in liste_destinataire:
        length = len(dest)
        if dest[length-2] == "/":
            dest = dest.split("/")[0]
            final_.append(dest)
        else:
            final_.append(dest)
    return send_mail(
        titre,  #subject
        text, 
        "saravincent@amexpert.biz",#from_mail
        final_,  #recipient list []
        fail_silently=True,  #fail_silently
        html_message="<p>"+text+"</p>"
    )
    