from django import template


register = template.Library()
@register.filter
def isoddnumberseason(totseasonnumber, currentseasonnumber):
        
    if ((totseasonnumber + 1) - currentseasonnumber) % 2 != 0: 
        return int(0)
    else:
        return int(1)