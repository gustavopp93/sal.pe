from django.conf import settings
import mandrill


def send_email_via_mandrill(email, name, subject, template_name, template_content):
    try:
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
        message = {'from_email': 'no-reply@sal.pe',
                   'from_name': 'sal.pe',
                   'global_merge_vars': template_content,
                   'subject': subject,
                   'to': [{'email': email,
                           'name': name,
                           'type': 'to'}]}
        mandrill_client.messages.send_template(template_name=template_name,
                                               template_content=template_content,
                                               message=message, async=True)
    except mandrill.Error:
        pass