class Validator:

    @staticmethod
    def parse_amount(amount):
        try:
            float(amount)
            return True
        except Exception as e:
            return False