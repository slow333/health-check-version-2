from flask import request
from ..extensions import db

def pagenation(query, per_page=10, orders=None, request_args=None):
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * per_page

    if orders is not None:
        query = query.order_by(orders)
    else:
        # 모델에 'id' 속성이 있다고 가정하고 기본 정렬 적용
        query = query.order_by(query.column_descriptions[0]['entity'].id.desc())

    query_result = query.limit(per_page).offset(offset).all()
    total = query.order_by(None).count()

    # 페이지네이션: 현재 페이지 기준으로 최대 5개 페이지만 표시
    # 페이지네이션: 10개 페이지 링크 고정
    total_pages = (total // per_page) + (1 if total % per_page else 0)
    page_len = len(query_result)

    start_page = max(1, page - 4)
    end_page = min(total_pages, start_page + 9)
    if end_page - start_page < 9:
        start_page = max(1, end_page - 9)

    pagination_data = {
        'query_result': query_result,
        'page': page,
        'per_page': per_page,        
        'total_pages': total_pages,
        'page_len': page_len,
        'start_page': start_page,
        'end_page': end_page,
        'request_args': request_args
    }
    return pagination_data