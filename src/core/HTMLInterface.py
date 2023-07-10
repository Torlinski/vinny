"""Interface for converting session payload to html"""
from src.models import SessionPayload

ACTIVE_SENTENCE_COLOUR = '#bf4311'
ACTIVE_PARAGRAPH_COLOUR = '#eaed82'
CHATGPT_REQUEST_COLOUR = '#156e1f'


class HTMLInterface:
    """Contains static methods for converting session data into html to serve on flask"""

    @staticmethod
    def html_text(update: SessionPayload) -> str:
        """converts session text to html"""
        output = ''
        for i, paragraph in enumerate(update.paragraphs):
            if i != update.index:
                output += '<span>' + ' '.join(paragraph) + '</span><br><br>'
            else:
                output += f'<mark style="background: {ACTIVE_PARAGRAPH_COLOUR}!important">'
                if len(paragraph) > 1:
                    output += (
                        f'<span>'
                        + ' '.join(paragraph[:-1])
                        + '</span>'
                        + f'<span style="color:{ACTIVE_SENTENCE_COLOUR};">'
                        + ' '
                        + paragraph[-1]
                        + '</span></mark><br><br>'
                    )
                elif len(paragraph) == 1:
                    output += (
                        f'<span style="color: {ACTIVE_SENTENCE_COLOUR};">'
                        + paragraph[-1]
                        + '</span></mark><br><br>'
                    )
        return output

    @staticmethod
    def html_commands(update: SessionPayload) -> str:
        """converts session commands to html"""
        output = (
            '<ul>'
            + ''.join(['<li>' + x + '</li>' for x in update.commands[::-1]])
            + '</ul>'
        )
        return output

    @staticmethod
    def html_chatgpt(update: SessionPayload) -> str:
        """converts session chatgpt request to html"""
        output = ''
        request = update.chatgpt
        if request != '':
            output += '<span>Applying: </span>'
            output += f'<span style="color:{CHATGPT_REQUEST_COLOUR}">"{request}"</span>"'
            output += (
                '<span> as a chatgpt request for the following text: </span>'
            )
            output += f'<mark style="background: {ACTIVE_PARAGRAPH_COLOUR}!important">'
            output += (
                f'<span>"{" ".join(update.paragraphs[update.index])}"</span>'
            )
            output += f'</mark>'
            output += f'<span> - Say "Send Request" to confirm. </span>'
            return output
        return ''
