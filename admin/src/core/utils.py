from src.core.system_config.system_config import SystemConfig


def paginated(query, current_page=1):
    paginator = query.paginate(page=current_page, per_page=system_page_size())
    return { 'items': paginator.items, 'pages': paginator.pages };

def system_page_size():
    return SystemConfig \
            .query.with_entities(SystemConfig.items_qty_for_grids) \
            .first()[0]