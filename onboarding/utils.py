import phonenumbers


class Utility:

    @staticmethod
    def get_valid_mobile_number(mobile, country_code):
        try:

            complete_number = str(country_code) + str(mobile)
            parsed_number = phonenumbers.parse(complete_number)
            is_valid = phonenumbers.is_possible_number(parsed_number)

            if not is_valid:
                return {
                    "status": 0,
                    "message": "Please enter a valid mobile Number"
                }

            valid_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            return {"status": 1, "valid_number": valid_number}
        except Exception as e:
            print(e)
            return {
                "status": 0,
                "message": "Please enter a valid mobile Number"
            }
