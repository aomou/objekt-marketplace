# 放一些小工具

# sort ordering 排序用的
def get_ordering(request):

    default_ordering = [
        'season__seasonNum',
        'season__seasonPrefix',
        'collection__name',
        'artist__name',
        'member__memberNum',
    ]

    sort_map = {
        'season': ['season__seasonNum', 'season__seasonPrefix'],
        'collection': ['collection__name'],
        'member': ['member__memberNum'],
        'artist': ['artist__tokenId'],
    }

    sort_by_1 = request.GET.get('sort_by')
    sort_by_2 = request.GET.get('sort_by_2')
    ordering = default_ordering.copy()

    if sort_by_1 in sort_map:
        for field in reversed(sort_map[sort_by_1]):
            if field in ordering:
                ordering.remove(field)
            ordering.insert(0, field)

    if sort_by_2 in sort_map:
        for field in reversed(sort_map[sort_by_2]):
            if field in ordering:
                ordering.remove(field)
            ordering.insert(0, field)

    order = request.GET.get('order', 'asc')
    if order == 'desc':
        ordering = [f'-{field}' for field in ordering]

    return ordering