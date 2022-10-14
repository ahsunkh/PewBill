class PewBillTemplate:

    def __init__(self):
        self.name = "PewBillTemplate"

    @staticmethod
    def otp_mail_template_func(otp=None):
        #otp_template = """Your verification OTP is """ + otp + """ \n PewBill"""
        otp_template = "Your verification OTP is " + str(otp) + " \n PewBill"
        return otp_template
