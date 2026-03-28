import base64

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from pewbill.responses import Response
from pewbill.settings import SEND_IN_BLUE_API_KEY, SENDER_IN_BLUE


class SendEmail():
    def __ini__(self):
        self.name = "GetLoopSendEmail"

    @staticmethod
    def send_email(reciever, name, subject, content, attachment=False, file_name=None, name_file=None):
        try:
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = SEND_IN_BLUE_API_KEY
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            sender = SENDER_IN_BLUE
            to = [{"email": reciever, "name": name}]
            headers = {"Some-Custom-Name": "unique-id-1234"}
            if attachment:
                filename = file_name

                with open(filename, "rb") as file:
                    encoded_string = base64.b64encode(file.read())
                    base64_message = encoded_string.decode('utf-8')

                attachment = [{"content": base64_message, "name": name_file}]
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, attachment=attachment, html_content=content,
                                                               sender=sender, subject=subject)
                api_response = api_instance.send_transac_email(send_smtp_email)
            else:
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=content,
                                                               sender=sender, subject=subject)
                api_response = api_instance.send_transac_email(send_smtp_email)
            if api_response.message_id:
                return True
            return False
        except Exception as err:
            print(err)
            return False