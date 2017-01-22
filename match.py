class Match(object):
    """A sentence with index containing locations of matches."""

    def __init__(self, token_ids, sent_id, doc_id):
        """Constructor

        Args:
            token_ids: index of matching tokens
            sent_id: id of sentence containing matches
            doc_id: id of document containing sentence
        """
        self.token_ids = token_ids
        self.sent_id = sent_id
        self.doc_id = doc_id

    def format_sentence(self, sentences, hl_start, hl_end):
        """Return sentence for this match with match locations highlighted."""
        formatted = [self.format_token(t, hl_start, hl_end)
                     for t in sentences[self.sent_id].tokens]
        return ''.join(formatted).strip()

    def format_token(self, token, hl_start, hl_end):
        """Return plain or highlighted version of given token."""
        if token.i in self.token_ids:
            return self.highlight(token, hl_start, hl_end)
        return token.text_with_ws

    def highlight(self, token, hl_start, hl_end):
        """Return highlighted version of given string."""
        highlighted = f'{hl_start}{token.text}{hl_end}'
        # don't want to highlight any trailing whitespace so add it after
        return highlighted + token.whitespace_
