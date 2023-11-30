class Paginator():

    def paginate(self, lst: list, numbers: int) -> dict:
        d = {}
        page_number = 1
        i = 0
        while i < len(lst):
            page = lst[i:i+numbers]
            d[page_number] = page
            page_number += 1
            i += numbers
        d['total_pages'] = page_number-1
        return d
