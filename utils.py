# from passlib.context import CryptContext
# import sib_api_v3_sdk
# from sib_api_v3_sdk.rest import ApiException
# import os
#
# _pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def get_password_hash(password: str) -> str:
#     return _pwd.hash(password)
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return _pwd.verify(plain_password, hashed_password)
#
# def send_otp_email(receiver_email: str, otp: str):
#     configuration = sib_api_v3_sdk.Configuration()
#     configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")
#
#     api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
#     sender = {"email": os.getenv("BREVO_SENDER_EMAIL")}
#     to = [{"email": receiver_email}]
#     subject = "Your OTP Code for Sign Up"
#     html_content = f"<p>Your OTP code is <b>{otp}</b>. It will expire in 2 minutes.</p>"
#
#     send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#         to=to, sender=sender, subject=subject, html_content=html_content
#     )
#
#     try:
#         api_instance.send_transac_email(send_smtp_email)
#         return True
#     except ApiException as e:
#         print(f"Error sending OTP: {e}")
#         return False

from passlib.context import CryptContext
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password hashing and verification
def get_password_hash(password: str) -> str:
    return _pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd.verify(plain_password, hashed_password)

# Send OTP email
def send_otp_email(receiver_email: str, otp: str):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"email": os.getenv("BREVO_SENDER_EMAIL")}
    to = [{"email": receiver_email}]
    subject = "Your OTP Code for Sign Up"
    html_content = f"<p>Your OTP code is <b>{otp}</b>. It will expire in 2 minutes.</p>"

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, sender=sender, subject=subject, html_content=html_content
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        print(f"OTP sent successfully to {receiver_email}")
        return True
    except ApiException as e:
        print(f"Error sending OTP: {e.body if hasattr(e, 'body') else str(e)}")
        return False
