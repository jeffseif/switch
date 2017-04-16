from colors import BLUE
from colors import GREEN
from colors import RED
from colors import YELLOW
from colors import WHITE

from switch.ifttt import IFTTT
from switch.logger import Logger


FAILURE = RED('✗')
SUCCESS = GREEN('✓')


class WebSession(Logger):

    def check_for_zipcode(self, args):
        if not args.beyond_console and not self.is_console:
            return
        response = self.run_session_for_zipcode(args.zipcode, self.prompt)

        results = list(self.check_response_for_product(response, self.product_id))
        status = SUCCESS if results else FAILURE

        print(' '.join((status, WHITE(self.product_description))))
        for left, right in results:
            print(YELLOW(left) + ': ' + BLUE(right))
            IFTTT(self.product_description, ' '.join((left, self.__class__.__name__)), right)
