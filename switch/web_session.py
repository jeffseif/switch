class WebSession:

    FAILURE = '\033[1;31m✗\033[0m'
    SUCCESS = '\033[1;32m✓\033[0m'
    STATUS_TEMPLATE = '{:s} \033[1;37m{:s}\033[0m'

    def check_for_zipcode(self, zipcode):
        html = self.run_session(zipcode, self.query)
        status = self.SUCCESS if self.check_for_product(html, self.product_id) else self.FAILURE
        print(self.STATUS_TEMPLATE.format(status, self.product_description))

    def run_session(zipcode, query):
        raise NotImplementedError

    def check_for_product(zipcode, query):
        raise NotImplementedError
