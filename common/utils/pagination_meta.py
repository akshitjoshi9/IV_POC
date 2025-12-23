from common.utils import PaginationMeta


def build_pagination_meta(params, page) -> PaginationMeta:
    """
    Build pagination metadata from request and paginated result.
    Args:
        params: Request params with page size.
        page: Paginated result with current page info.
        ex: build_pagination_meta(params, page)
    Returns:
        PaginationMeta object with page details.
    """
    return PaginationMeta(
        page_size=params.size,
        total_pages=page.pages,
        current_page=page.page,
        total_entries=page.total,
        next=page.page + 1 if page.page < page.pages else None,
        previous=page.page - 1 if page.page > 1 else None,
    )
