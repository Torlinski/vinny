"""Interface for converting session payload to html"""

active_sentence_colour = '#bf4311'
active_paragraph_colour = '#eaed82'


class HTML_Interface:
    """Contains static methods for converting session data into html to serve on flask"""

    @staticmethod
    def html_text(update):
        output = ''
        for i, paragraph in enumerate(update.get('paragraphs')):
            if i != update.get('index'):
                output += '<span>' + ' '.join(paragraph) + '</span><br><br>'
            else:
                output += f'<mark style="background: {active_paragraph_colour}!important">'
                if len(paragraph) > 1:
                    output += (
                        f'<span>'
                        + ' '.join(paragraph[:-1])
                        + '</span>'
                        + f'<span style="color:{active_sentence_colour};">'
                        + ' '
                        + paragraph[-1]
                        + '</span></mark><br><br>'
                    )
                elif len(paragraph) == 1:
                    output += (
                        f'<span style="color: {active_sentence_colour};">'
                        + paragraph[-1]
                        + '</span></mark><br><br>'
                    )
        return output

    @staticmethod
    def html_commands(update):
        output = (
            '<ul>'
            + ''.join(
                ['<li>' + x + '</li>' for x in update.get('commands')[::-1]]
            )
            + '</ul>'
        )
        return output

    @staticmethod
    def html_chatgpt(update):
        output = ''
        request = update.get('chatgpt')
        if request != '':
            output += '<span>Applying: </span>'
            output += f'<span style="color:#156e1f">"{request}"</span>"'
            output += (
                '<span> as a chatgpt request for the following text: </span>'
            )
            output += f'<mark style="background: {active_paragraph_colour}!important">'
            output += f'<span>"{" ".join(update.get("paragraphs")[update.get("index")])}"</span>'
            output += f'</mark>'
            output += f'<span> - Say "Send Request" to confirm. </span>'
            return output
        return ''
