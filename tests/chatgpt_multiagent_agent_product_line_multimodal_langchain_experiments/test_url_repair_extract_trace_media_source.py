
from typing import Optional
def recover_prompt_constructor(info): return f"""
Please recover any URL from the given context. Every URL shall be visitable, starting with "http://" or "https://".

Context:

{info}

URLs:

"""


def indexify_string_list(string_list): return [
    f'[{index}] {url}' for index, url in enumerate(string_list)]


def youtube_select_prompt_constructor(url_list): 
    urls_content = '\n'.join(indexify_string_list(url_list))
    return f"""
Please select URLs if they are directed to YouTube. I will give you URLs with index in front of them. Give your selection by selected indices in squared brackets separated by space like: [1] [3].

URLs:

{urls_content}

Selected URLs:

"""

from test_chatgpt_cn_api import get_reply_from_chatgpt
def repair_content_with_url(info):
    prompt = recover_prompt_constructor(info)
    content = get_reply_from_chatgpt(prompt)
    return content

import re

def get_youtube_selection_ids(urls):
    prompt = youtube_select_prompt_constructor(urls)
    response= get_reply_from_chatgpt(prompt)
    numbers = re.findall(r'\[\d+\]', response)
    indices = []
    for num in numbers:
        num = num.strip("[").strip(']').strip()
        num = int(num)
        indices.append(num)
    return indices

def select_youtube_urls(url_list, indices):
    fatal_error:Optional[str]= None
    selected_urls = []
    index_errors = 0
    url_counts = len(url_list)
    max_index = url_counts-1
    for index in indices:
        try:
            url = url_list[index]
            print("selected:", url)
            selected_urls.append(url)
        except IndexError:
            index_errors += 1
            # TODO: handle error by recursively letting the LLM knows the error and querying answer.
            # TODO: determine if error is fatal (not recoverable in 5 iterations)
            # TODO: eliminate possibility of external cause of fatal error by inferance
            print('index not found: %d (max index is %d)' % (index, max_index))
    print("summary".center(80, "="))
    print("given url counts: %d" % url_counts)
    print("selected url counts: %d", len(selected_urls))
    print("index errors: %d" % index_errors)
    return selected_urls

from urlextract import URLExtract

extractor = URLExtract()

def extract_url(content):
    """
    Just extract the url. Do not repair.
    """
    
    urls = extractor.find_urls(content)
    return urls


def repair_and_get_repaired_url_list(info):
    content = repair_content_with_url(info)
    url_list = extract_url(content)
    return url_list


if __name__ == '__main__':
    info_direct = """
Youtube
原标题A Thousand Miles-Neco are(FULL VERSION)
https://youtu.be/Ddpx0JLOH6o?si=zZMjAEFj_TOXkQct
音频下载：
https://wwxa.lanzouj.com/idPN81a5u4ab
密码:5292
"""

    info_indirect = """
转自Youtube
/watch?v=mSqRH4WwnnY // By :Encrypted Lobster
"""

    info_list = [info_direct, info_indirect]
    for i, info in enumerate(info_list):
        print(f"processing info #{i}")
        print(info)
        repaired_urls = repair_and_get_repaired_url_list(info)
        indices = get_youtube_selection_ids(repaired_urls)
        selected_urls = select_youtube_urls(repaired_urls, indices)
        print("selected urls:")
        for url in selected_urls:
            print(f'\t{url}')
        print()