from django import template
from menu.models import MenuItem
from django.urls import resolve

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_path = context['request'].path
    try:
        current_url_name = resolve(current_path).url_name
    except:
        current_url_name = None

    all_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    item_dict = {item.id: item for item in all_items}
    children_map = {}
    active_item_id = None

    for item in all_items:
        children_map.setdefault(item.parent_id, []).append(item)
        if item.get_absolute_url() == current_path or item.named_url == current_url_name:
            active_item_id = item.id

    active_branch_ids = set()

    def fill_active_branch(item_id):
        while item_id:
            active_branch_ids.add(item_id)
            item = item_dict.get(item_id)
            if item and item.parent_id:
                item_id = item.parent_id
            else:
                break

    if active_item_id:
        fill_active_branch(active_item_id)

    def build_tree(parent_id=None, active_chain=None):
        items = []
        for item in children_map.get(parent_id, []):
            is_active = item.id in active_branch_ids
            in_active_chain = active_chain and item.id in active_chain

            show_children = in_active_chain or is_active or item.id == active_item_id or item.id in children_map.get(
                active_item_id, [])

            items.append({
                'item': item,
                'children': build_tree(item.id, active_branch_ids) if show_children else [],
                'is_active': is_active
            })
        return items

    return {'menu_tree': build_tree()}
