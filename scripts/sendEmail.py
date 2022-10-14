import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from pewbill.responses import Response
from pewbill.settings import SEND_IN_BLUE_API_KEY, SENDER_IN_BLUE


class SendEmail():
    def __ini__(self):
        self.name = "GetLoopSendEmail"

    @staticmethod
    def send_email(reciever, name, subject, content):
        try:
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = SEND_IN_BLUE_API_KEY
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            sender = SENDER_IN_BLUE
            to = [{"email": reciever, "name": name}]
            headers = {"Some-Custom-Name": "unique-id-1234"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=content,
                                      sender=sender, subject=subject)
            api_response = api_instance.send_transac_email(send_smtp_email)
            return Response.create_data("Sent successfully")

            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
            if data.sid:
                return True
            return False
        except Exception as err:
            return False
