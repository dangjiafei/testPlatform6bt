from rest_framework.pagination import PageNumberPagination as _PageNumberPagination


class PageNumberPagination(_PageNumberPagination):

    # 指定前端获取哪一页的key值
    page_query_param = 'page'

    # 指定前端获取每一页总数据的key值
    page_size_query_param = 'size'

    # 指定默认每一页的数据条数，优秀级最高
    page_size = 10

    # 指定前端最大的总页数
    max_page_size = 20

    page_query_description = "第几页"

    page_size_query_description = "每页几条"

    invalid_page_message = "页码无效"  # 指定错误页面的提示

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page_num'] = self.page.number
        response.data['total_page'] = self.page.paginator.num_pages
        return response
