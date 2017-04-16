class WebSession:

    FAILURE = '\033[1;31m✗\033[0m'
    SUCCESS = '\033[1;32m✓\033[0m'
    STATUS_TEMPLATE = '{:s} \033[1;37m{:s}\033[0m'

    def check_for_zipcode(self, zipcode):
        response = self.run_session_for_zipcode(zipcode, self.prompt)
        status = self.SUCCESS if self.check_response_for_product(response, self.product_id) else self.FAILURE
        print(self.STATUS_TEMPLATE.format(status, self.product_description))
