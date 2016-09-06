class VirtualMachine:
    def __init__(self, bots, verbose=False):
        self.seq = 0
        self.bots = bots
        self.requests = {}
        self.callbacks = {}
        self.messages = []
        self.replies = []
        self.verbose = verbose

    def send_message(self, callback, bot, message):
        self.messages.append((self.seq, bot, message, callback))
        self.seq += 1

    def event_loop(self):
        while self.messages or self.replies:
            while self.replies:
                seq, answer = self.replies.pop(0)
                self.callbacks[seq](answer)
                if self.verbose:
                    print '  %4d: %s -> %s' % (
                        seq,
                        self.requests[seq],
                        json.dumps(answer))
                del self.callbacks[seq]
                del self.requests[seq]
            while self.messages:
                seq, bot, message, callback = self.messages.pop(0)
                self.requests[seq] = message
                self.callbacks[seq] = callback
                def make_callback(seq):
                    def my_callback(answer):
                        self.replies.append((seq, answer))
                    return my_callback
                bot.receive(self.send_calculation, make_callback(seq), message)

    def send_calculation(self, callback, token):
        # generalize
        message = str(token)
        action = str(token.tokens[0])
        bot = self.bots[action]
        self.send_message(callback, bot, message)

    def process_message(self, message):
        human = self.bots['Human']
        if self.verbose:
            print "\n\n--"

        def callback(answer):
            print '%s -> %s' % (message, repr(answer))

        self.send_message(callback, human, message)
        self.event_loop()

