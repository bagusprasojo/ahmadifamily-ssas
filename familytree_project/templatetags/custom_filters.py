from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def add_highlight(text, word):
    if not word:
        return text
    regex = re.compile(re.escape(word), re.IGNORECASE)
    return regex.sub(lambda m: f'<mark>{m.group(0)}</mark>', text)

@register.filter
def snippet_around_keyword(text, word):
    if not word:
        return strip_tags(text)[:100] + '...'

    # Bersihkan tag HTML dulu
    clean_text = strip_tags(text)

    word_lower = word.lower()
    text_lower = clean_text.lower()
    index = text_lower.find(word_lower)

    if index == -1:
        return clean_text[:400] + '...'

    start = max(index - 200, 0)
    end = min(index + 200, len(clean_text))
    snippet = clean_text[start:end]

    # Highlight keyword
    regex = re.compile(re.escape(word), re.IGNORECASE)
    snippet = regex.sub(lambda m: f'<mark>{m.group(0)}</mark>', snippet)

    return mark_safe(f"...{snippet}...")

