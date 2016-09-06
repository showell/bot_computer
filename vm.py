class VirtualMachine:
    def __init__(self, bots, verbose=False):
        self.seq = 0
        self.bots = bots
        self.requests = {}
        self.callbacks = {}
        self.messages = []
        self.replies = []
        self.verbose = verbose

    def process_message(self, callback, message):
        '''
        Send a message to the "root" bot and then start our
        event loop to handle replies from various bots.

        To avoid hitting maximum-recursion limits and to
        simulate a networked computation, the bots don't reply
        directly to us; instead they push replies on to a queue
        that we process in an event loop.
        '''
        human = self.bots['Human']
        if self.verbose:
            print "\n\n--"

        self.send_message(callback, human, message)
        self.event_loop()

    def _dispatch_request_to_bot(self, seq, bot, message, callback):
        '''
        We need a bot to do work for us, and we have a sequence
        number and a message, plus some callback that we need
        to send the bot's reply to.  The callback is often a
        wrapper to some mechanism to forward the reply on to
        another bot that requested the calculation.  The sequence
        number will allow us to match replies to requests.
        '''
        self.requests[seq] = message
        self.callbacks[seq] = callback
        def make_callback(seq):
            def my_callback(answer):
                self.replies.append((seq, answer))
            return my_callback
        bot.receive(self.send_calculation, make_callback(seq), message)

    def _handle_reply_from_bot(self, seq, answer):
        '''
        Handle a reply from a bot, which will have a sequence
        number that helps us find the callback function for the
        original request.
        '''
        self.callbacks[seq](answer)
        if self.verbose:
            print '  %4d: %s -> %s' % (
                seq,
                self.requests[seq],
                json.dumps(answer))
        del self.callbacks[seq]
        del self.requests[seq]

    def send_message(self, callback, bot, message):
        self.messages.append((self.seq, bot, message, callback))
        self.seq += 1

    def event_loop(self):
        while self.messages or self.replies:
            while self.replies:
                seq, answer = self.replies.pop(0)
                self._handle_reply_from_bot(seq, answer)

            while self.messages:
                seq, bot, message, callback = self.messages.pop(0)
                self._dispatch_request_to_bot(seq, bot, message, callback)

    def send_calculation(self, callback, token):
        message = str(token)
        action = str(token.tokens[0])
        bot = self.bots[action]
        self.send_message(callback, bot, message)

