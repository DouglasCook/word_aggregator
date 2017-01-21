class Match():
    """A sentence with index containing locations of matches."""

    highlight_start = '\033[91m' # red
    highlight_end = '\033[0m'

    def __init__(self, word, token_ids, sent_id, doc_id):
        self.word = word
        self.token_ids = token_ids
        self.sent_id = sent_id
        self.doc_id = doc_id

    def format_sentence(self, sentences):
        """Return sentence for this match with match locations highlighted."""
        formatted = [self.format_token(t) for t in sentences[self.sent_id].tokens]
        return ''.join(formatted).strip()

    def format_token(self, token):
        """Return plain or highlighted version of given token."""
        if token.i in self.token_ids:
            return self.highlight(token.text_with_ws)
        return token.text_with_ws

    def highlight(self, string):
        """Return highlighted version of given string."""
        return f'{self.highlight_start}{string}{self.highlight_end}'
