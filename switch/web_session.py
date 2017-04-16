from switch.logger import Logger


FAILURE = '\033[1;31m✗\033[0m'
LOCATION = '\033[1;33m{:s}\033[0m: \033[1;90m{:s}\033[0m'
SUCCESS = '\033[1;32m✓\033[0m'
STATUS = '{:s} \033[1;37m{:s}\033[0m'


class WebSession(Logger):

    def check_for_zipcode(self, args):
        if not args.beyond_console and not self.is_console:
            return
        response = self.run_session_for_zipcode(args.zipcode, self.prompt)

        results = list(self.check_response_for_product(response, self.product_id))
        status = SUCCESS if results else FAILURE

        print(STATUS.format(status, self.product_description))
        for result in results:
            print(LOCATION.format(*result))
