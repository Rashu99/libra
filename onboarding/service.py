from random import randint
from django.core.cache import cache
from django.conf import settings
import bcrypt

from onboarding import constants
from onboarding.sms_service import SMSService
from onboarding.utils import Utility


class Service:

    def get_otp_for_user_mobile(self, mobile, country_code, platform="WEB", request_id=None):

        complete_mobile = Utility.get_valid_mobile_number(mobile, country_code)
        if complete_mobile['status'] == 0:
            return {
                'status': 0,
                'message': 'Mobile Number is not valid!'
            }

        try:
            resp = self.generate_verification_code(complete_mobile['valid_number'], country_code, platform, request_id)
            return resp
        except Exception as e:
            print(e)
            return {
                'status': 0,
                'message': f'Some Exception Occurs. {e}'
            }

    def generate_verification_code(self, complete_mobile, country_code="+91", platform="WEB", request_id=None):
        code = randint(100000, 999999)

        cache_key = "mobile_cache_otp" + '_' + str(complete_mobile)
        last_otp_sent = settings.OTP_VALIDITY - cache.ttl(cache_key)

        if last_otp_sent < settings.OTP_RESEND_TIME:
            return {
                'status': 0,
                'message': f'Please wait {settings.OTP_RESEND_TIME} secs before trying again.'
            }

        sms_otp_counter_key = constants.USER_SMS_OTP_COUNTER_KEY_INITIALS + '_' + str(complete_mobile)
        sms_otp_counter = cache.get(sms_otp_counter_key)
        if not sms_otp_counter:
            sms_otp_counter = 1
            cache.set(sms_otp_counter_key, sms_otp_counter, settings.SMS_OTP_COOLDOWN_TIME * 60)
        else:
            sms_otp_counter = int(sms_otp_counter)
            sms_otp_counter += 1
            cache.incr(sms_otp_counter_key, 1)

        if sms_otp_counter > settings.THRESHOLD_SMS_OTP_COUNTER:
            if sms_otp_counter == settings.THRESHOLD_SMS_OTP_COUNTER + 1:
                cache.set(sms_otp_counter_key, sms_otp_counter, settings.SMS_OTP_COOLDOWN_TIME * 60)
            return {
                'status': 0,
                'message': f'Please try again after {settings.SMS_OTP_COOLDOWN_TIME} minutes'
            }

        text_message = f'Your six digit otp for login on Library App is {code}'
        SMSService().send_sms(complete_mobile, text_message, country_code, request_id)

        hashed_code = bcrypt.hashpw(str(code).encode('ascii'), bcrypt.gensalt())
        cache.set(cache_key, hashed_code, settings.OTP_VALIDITY)
        return {
            'status': 1,
            'message': 'OTP Sent Successfully!'
        }
