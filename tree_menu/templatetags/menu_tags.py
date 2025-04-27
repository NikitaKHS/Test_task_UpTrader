from django import template
from tree_menu.models import MenuItem

register = template.Library()

def build_tree(items):
    nodes = {i.id: {'i': i, 'kids': []} for i in items}
    roots = []
    for node in nodes.values():
        pid = node['i'].parent_id
        if pid and pid in nodes:
            nodes[pid]['kids'].append(node)
        else:
            roots.append(node)
    return roots

def mark_active(nodes, path):
    for node in nodes:
        node['cur'] = (node['i'].get_url() == path)
        if node['kids']:
            mark_active(node['kids'], path)
            node['open'] = any(c.get('cur') or c.get('open') for c in node['kids']) or node['cur']
        else:
            node['open'] = node['cur']

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, name):
    request = context.get('request')
    if not request:
        return {'nodes': []}
    items = list(
        MenuItem.objects
            .filter(menu__name=name)
            .select_related('parent')
    )
    tree = build_tree(items)
    mark_active(tree, request.path)
    return {'nodes': tree}
