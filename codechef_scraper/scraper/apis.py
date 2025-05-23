import requests


def get_contest_list(offset):
    """
    调试页面：https://www.codechef.com/contests
    用于获取一部分比赛列表
    """
    cookies = {
        "SESS93b6022d778ee317bf48f7dbffe03173": "7658b53a83f2feb183c765adcd43f5b7",
        "_gid": "GA1.2.1622115403.1744288780",
        "_clck": "18c7hcx%7C2%7Cfuz%7C0%7C1926",
        "_clsk": "1dnxzgp%7C1744347287018%7C1%7C1%7Cx.clarity.ms%2Fcollect",
        "g_state": '{"i_l":0}',
        "_gcl_au": "1.1.1287414113.1744288780.1010724834.1744347365.1744347364",
        "_ga_C8RQQ7NY18": "GS1.1.1744373937.5.1.1744375326.58.0.0",
        "_ga": "GA1.2.1783263705.1744288780",
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,zh-TW;q=0.5",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.codechef.com/contests",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-csrf-token": "47c908075b2df360a2d3fb45dbfdca1ee0a05e3d49914f5439ea0d63dd11dbe0",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "sort_by": "START",
        "sorting_order": "desc",
        "offset": str(offset),
        "mode": "all",
    }

    response = requests.get(
        "https://www.codechef.com/api/list/contests/past",
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()

    return response["contests"]


def get_contest_metadata(contest):
    """
    调试页面：https://www.codechef.com/START181
    获取某个比赛的元数据
    """
    cookies = {
        "SESS93b6022d778ee317bf48f7dbffe03173": "7658b53a83f2feb183c765adcd43f5b7",
        "_gid": "GA1.2.1622115403.1744288780",
        "_clck": "18c7hcx%7C2%7Cfuz%7C0%7C1926",
        "g_state": '{"i_l":0}',
        "_gcl_au": "1.1.1287414113.1744288780.1010724834.1744347365.1744347364",
        "_ga": "GA1.2.1783263705.1744288780",
        "_gat_UA-141612136-1": "1",
        "userkey": "56a7ba633e70a409025ae6f4d029a938",
        "_clsk": "1t4h6i1%7C1744377333899%7C1%7C1%7Cb.clarity.ms%2Fcollect",
        "_ga_C8RQQ7NY18": "GS1.1.1744373937.5.1.1744377345.45.0.0",
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,zh-TW;q=0.5",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": f"https://www.codechef.com/{contest}",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-csrf-token": "47c908075b2df360a2d3fb45dbfdca1ee0a05e3d49914f5439ea0d63dd11dbe0",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "v": "1744377346355",
    }

    response = requests.get(
        f"https://www.codechef.com/api/contests/{contest}",
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()

    return response


def get_division_metadata(division_link):
    """
    调试页面：https://www.codechef.com/START181A
    CodeChef中，每个比赛会分division，给不同等级的选手做
    获取每个division的元数据
    """
    cookies = {
        "_gid": "GA1.2.1210448190.1744521090",
        "_clck": "1vw9wxu%7C2%7Cfv1%7C0%7C1929",
        "_clsk": "86sswr%7C1744521098402%7C1%7C1%7Cl.clarity.ms%2Fcollect",
        "g_state": '{"i_l":0}',
        "_gcl_au": "1.1.656532890.1744521088.586691634.1744521106.1744521106",
        "SESS93b6022d778ee317bf48f7dbffe03173": "3fd030a915dc2e511d78b78feaab083d",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiI1NjM0MTU1IiwidXNlcm5hbWUiOiJicmFjZV9saWZlXzgyIiwiaWF0IjoxNzQ0NTIxMTA4LCJuYmYiOjE3NDQ1MjExMDgsImV4cCI6MTc0NjUxNTUwOH0.bQ_AmgV3VHXnbkxqDf1gzuCgeR0tsp6ngip_N4esD_U",
        "uid": "5634155",
        "_ga_C8RQQ7NY18": "GS1.1.1744521090.1.1.1744521480.57.0.0",
        "_ga": "GA1.2.176489956.1744521090",
        "_gat_UA-141612136-1": "1",
        "userkey": "56a7ba633e70a409025ae6f4d029a938",
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,zh-TW;q=0.5",
        "priority": "u=1, i",
        "referer": "https://www.codechef.com/START181A",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-csrf-token": "54d125f64ad884b90ad0dab57cb1228064516bb328ca802d65c21d03abb52e67",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "v": "1744521480711",
    }

    response = requests.get(
        f"https://www.codechef.com/api/contests{division_link}",
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()

    return response


def get_problem_metadata(problem_url):
    """
    调试页面：https://www.codechef.com/problems/FLIPPRE
    获取某个problem的元数据
    """
    cookies = {
        "_gid": "GA1.2.1210448190.1744521090",
        "_clck": "1vw9wxu%7C2%7Cfv1%7C0%7C1929",
        "_clsk": "86sswr%7C1744521098402%7C1%7C1%7Cl.clarity.ms%2Fcollect",
        "g_state": '{"i_l":0}',
        "_gcl_au": "1.1.656532890.1744521088.586691634.1744521106.1744521106",
        "SESS93b6022d778ee317bf48f7dbffe03173": "3fd030a915dc2e511d78b78feaab083d",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiI1NjM0MTU1IiwidXNlcm5hbWUiOiJicmFjZV9saWZlXzgyIiwiaWF0IjoxNzQ0NTIxMTA4LCJuYmYiOjE3NDQ1MjExMDgsImV4cCI6MTc0NjUxNTUwOH0.bQ_AmgV3VHXnbkxqDf1gzuCgeR0tsp6ngip_N4esD_U",
        "uid": "5634155",
        "_gat_UA-141612136-1": "1",
        "_ga_C8RQQ7NY18": "GS1.1.1744521090.1.1.1744522710.41.0.0",
        "_ga": "GA1.1.176489956.1744521090",
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,zh-TW;q=0.5",
        "priority": "u=1, i",
        "referer": "https://www.codechef.com/problems/FLIPPRE",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-csrf-token": "54d125f64ad884b90ad0dab57cb1228064516bb328ca802d65c21d03abb52e67",
        "x-requested-with": "XMLHttpRequest",
    }

    response = requests.get(
        f"https://www.codechef.com/api/contests/PRACTICE{problem_url}",
        cookies=cookies,
        headers=headers,
    ).json()

    return response


def get_explained_solution_list(problem_code):
    """
    调试页面：https://www.codechef.com/problems/FLIPPRE?tab=submissions
    获取某个problem的explained solution的列表
    """
    cookies = {
        "_gid": "GA1.2.1210448190.1744521090",
        "_clck": "1vw9wxu%7C2%7Cfv1%7C0%7C1929",
        "g_state": '{"i_l":0}',
        "_gcl_au": "1.1.656532890.1744521088.586691634.1744521106.1744521106",
        "SESS93b6022d778ee317bf48f7dbffe03173": "3fd030a915dc2e511d78b78feaab083d",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiI1NjM0MTU1IiwidXNlcm5hbWUiOiJicmFjZV9saWZlXzgyIiwiaWF0IjoxNzQ0NTIxMTA4LCJuYmYiOjE3NDQ1MjExMDgsImV4cCI6MTc0NjUxNTUwOH0.bQ_AmgV3VHXnbkxqDf1gzuCgeR0tsp6ngip_N4esD_U",
        "uid": "5634155",
        "_clsk": "ksx7ei%7C1744523217847%7C1%7C1%7Cl.clarity.ms%2Fcollect",
        "_gat_UA-141612136-1": "1",
        "_ga_C8RQQ7NY18": "GS1.1.1744521090.1.1.1744523652.23.0.0",
        "_ga": "GA1.2.176489956.1744521090",
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,zh-TW;q=0.5",
        "if-modified-since": "Sun, 13 Apr 2025 05:53:59 +0000",
        "if-none-match": 'W/"1744523639"',
        "priority": "u=1, i",
        "referer": "https://www.codechef.com/problems/FLIPPRE?tab=submissions",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-csrf-token": "54d125f64ad884b90ad0dab57cb1228064516bb328ca802d65c21d03abb52e67",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "problemCode": problem_code,
    }

    response = requests.get(
        "https://www.codechef.com/api/annotations/top",
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()

    return response


def get_solution_list(problem_code, language):
    """
    调试页面：https://www.codechef.com/status/FLIPPRE?contest=&language=PYTH%203&status=Correct
    获取AC的python3的solution列表
    """
    cookies = {
        "_gid": "GA1.2.1210448190.1744521090",
        "_clck": "1vw9wxu%7C2%7Cfv1%7C0%7C1929",
        "g_state": '{"i_l":0}',
        "_gcl_au": "1.1.656532890.1744521088.586691634.1744521106.1744521106",
        "SESS93b6022d778ee317bf48f7dbffe03173": "3fd030a915dc2e511d78b78feaab083d",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiI1NjM0MTU1IiwidXNlcm5hbWUiOiJicmFjZV9saWZlXzgyIiwiaWF0IjoxNzQ0NTIxMTA4LCJuYmYiOjE3NDQ1MjExMDgsImV4cCI6MTc0NjUxNTUwOH0.bQ_AmgV3VHXnbkxqDf1gzuCgeR0tsp6ngip_N4esD_U",
        "uid": "5634155",
        "_clsk": "ksx7ei%7C1744523217847%7C1%7C1%7Cl.clarity.ms%2Fcollect",
        "_ga": "GA1.2.176489956.1744521090",
        "_ga_C8RQQ7NY18": "GS1.1.1744521090.1.1.1744524346.60.0.0",
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,zh-TW;q=0.5",
        "if-modified-since": "Sun, 13 Apr 2025 06:03:14 +0000",
        "if-none-match": 'W/"1744524194"',
        "priority": "u=1, i",
        "referer": "https://www.codechef.com/status/FLIPPRE",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-csrf-token": "54d125f64ad884b90ad0dab57cb1228064516bb328ca802d65c21d03abb52e67",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "limit": "20",
        "page": "0",
        "contest": "",
        "language": language,
        "status": "Correct",
        "usernames": "",
    }

    response = requests.get(
        f"https://www.codechef.com/api/submissions/PRACTICE/{problem_code}",
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()

    return response


def get_solution(submission_id):
    """
    调试页面：https://www.codechef.com/viewsolution/1148731571
    获取某个solution
    """
    cookies = {
        "_gid": "GA1.2.1210448190.1744521090",
        "_clck": "1vw9wxu%7C2%7Cfv1%7C0%7C1929",
        "g_state": '{"i_l":0}',
        "_gcl_au": "1.1.656532890.1744521088.586691634.1744521106.1744521106",
        "SESS93b6022d778ee317bf48f7dbffe03173": "3fd030a915dc2e511d78b78feaab083d",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiI1NjM0MTU1IiwidXNlcm5hbWUiOiJicmFjZV9saWZlXzgyIiwiaWF0IjoxNzQ0NTIxMTA4LCJuYmYiOjE3NDQ1MjExMDgsImV4cCI6MTc0NjUxNTUwOH0.bQ_AmgV3VHXnbkxqDf1gzuCgeR0tsp6ngip_N4esD_U",
        "uid": "5634155",
        "_clsk": "ksx7ei%7C1744525795718%7C3%7C1%7Cl.clarity.ms%2Fcollect",
        "_ga_0F9XESWZ11": "GS1.2.1744525859.1.0.1744525859.60.0.0",
        "_gat_UA-141612136-1": "1",
        "_ga_C8RQQ7NY18": "GS1.1.1744521090.1.1.1744527080.13.0.0",
        "_ga": "GA1.2.176489956.1744521090",
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,zh-TW;q=0.5",
        "if-modified-since": "Sun, 13 Apr 2025 06:50:58 +0000",
        "if-none-match": 'W/"1744527058"',
        "priority": "u=1, i",
        "referer": "https://www.codechef.com/viewsolution/1148731571",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-csrf-token": "54d125f64ad884b90ad0dab57cb1228064516bb328ca802d65c21d03abb52e67",
        "x-requested-with": "XMLHttpRequest",
    }

    response = requests.get(
        f"https://www.codechef.com/api/submission-code/{submission_id}",
        cookies=cookies,
        headers=headers,
    ).json()

    return response


def get_annotation(submission_id):
    """
    调试页面：https://www.codechef.com/viewsolution/1148731571
    尝试获取某个solution的annotation
    """
    cookies = {
        "_gid": "GA1.2.1210448190.1744521090",
        "_clck": "1vw9wxu%7C2%7Cfv1%7C0%7C1929",
        "g_state": '{"i_l":0}',
        "_gcl_au": "1.1.656532890.1744521088.586691634.1744521106.1744521106",
        "SESS93b6022d778ee317bf48f7dbffe03173": "3fd030a915dc2e511d78b78feaab083d",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiI1NjM0MTU1IiwidXNlcm5hbWUiOiJicmFjZV9saWZlXzgyIiwiaWF0IjoxNzQ0NTIxMTA4LCJuYmYiOjE3NDQ1MjExMDgsImV4cCI6MTc0NjUxNTUwOH0.bQ_AmgV3VHXnbkxqDf1gzuCgeR0tsp6ngip_N4esD_U",
        "uid": "5634155",
        "_clsk": "ksx7ei%7C1744525795718%7C3%7C1%7Cl.clarity.ms%2Fcollect",
        "_ga_0F9XESWZ11": "GS1.2.1744525859.1.0.1744525859.60.0.0",
        "_gat_UA-141612136-1": "1",
        "_ga_C8RQQ7NY18": "GS1.1.1744521090.1.1.1744527080.13.0.0",
        "_ga": "GA1.2.176489956.1744521090",
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,zh-TW;q=0.5",
        "if-modified-since": "Sun, 13 Apr 2025 06:50:59 +0000",
        "if-none-match": 'W/"1744527059"',
        "priority": "u=1, i",
        "referer": "https://www.codechef.com/viewsolution/1148731571",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-csrf-token": "54d125f64ad884b90ad0dab57cb1228064516bb328ca802d65c21d03abb52e67",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "submission_id": submission_id,
    }

    response = requests.get(
        "https://www.codechef.com/api/annotations",
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()

    return response
