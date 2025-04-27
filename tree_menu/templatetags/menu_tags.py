from django import template
from tree_menu.models import Menu

register = template.Library()

def build_tree(items):
    nodes = {i.id: {'i': i, 'kids': []} for i in items}
    roots = []
    for n in nodes.values():
        pid = n['i'].parent_id
        if pid and pid in nodes:
            nodes[pid]['kids'].append(n)
        else:
            roots.append(n)
    return roots

def mark_active(nodes, path):
    for n in nodes:
        n['cur'] = (n['i'].get_url() == path)
        if n['kids']:
            mark_active(n['kids'], path)
            n['open'] = any(c.get('cur') or c.get('open') for c in n['kids']) or n['cur']
        else:
            n['open'] = n['cur']

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, name):
    req = context['request']
    try:
        m = Menu.objects.get(name=name)
    except Menu.DoesNotExist:
        return {'nodes': []}
    items = list(m.items.select_related('parent'))
    tree = build_tree(items)
    mark_active(tree, req.path)
    return {'nodes': tree}
