import requests
import pandas as pd
lst = []
cookies = {
    'x-anon-id': '93ff408a-f137-43a0-b0bb-2bcc8fb0094f',
    '_ga': 'GA1.1.992729195.1747215846',
    'gbStickyBuckets__id||93ff408a-f137-43a0-b0bb-2bcc8fb0094f': '{%22attributeName%22:%22id%22%2C%22attributeValue%22:%2293ff408a-f137-43a0-b0bb-2bcc8fb0094f%22%2C%22assignments%22:{%22ab-test-announcement-or-basic-banner__0%22:%221%22}}',
    '__stripe_mid': 'fb7d39bc-796b-4ff9-ab26-5a5465e7cba66bc1b5',
    '__stripe_sid': '6bcbe5dc-eadd-4147-9e43-67e05ab6f2a52a7ebf',
    '_gcl_au': '1.1.1090066898.1747215865',
    'CookieScriptConsent': '{"googleconsentmap":{"ad_storage":"targeting","analytics_storage":"performance","ad_user_data":"targeting","ad_personalization":"targeting","functionality_storage":"functionality","personalization_storage":"functionality","security_storage":"functionality"},"bannershown":1,"action":"accept","consenttime":1722613384,"categories":"[\\"targeting\\",\\"performance\\",\\"unclassified\\",\\"functionality\\"]","key":"898a3c45-4012-4e2c-af6f-d1f975173c03"}',
    '_ga_RF4WWQM7BF': 'GS2.1.s1747215845$o1$g1$t1747216380$j37$l0$h1700230090',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'baggage': 'sentry-environment=production,sentry-release=d967211c24c2a73d01e07657a5c5a059d45f77da,sentry-public_key=1dbee0ad22c14f97ee922e8b6d478b55,sentry-trace_id=e90afd7efc1340d58135505557ce944a,sentry-sampled=false,sentry-sample_rand=0.9981489194512352,sentry-sample_rate=0.01',
    'content-type': 'application/json',
    'origin': 'https://www.udio.com',
    'priority': 'u=1, i',
    'referer': 'https://www.udio.com/home',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'e90afd7efc1340d58135505557ce944a-bcbfce1471dd2a1b-0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': 'x-anon-id=93ff408a-f137-43a0-b0bb-2bcc8fb0094f; _ga=GA1.1.992729195.1747215846; gbStickyBuckets__id||93ff408a-f137-43a0-b0bb-2bcc8fb0094f={%22attributeName%22:%22id%22%2C%22attributeValue%22:%2293ff408a-f137-43a0-b0bb-2bcc8fb0094f%22%2C%22assignments%22:{%22ab-test-announcement-or-basic-banner__0%22:%221%22}}; __stripe_mid=fb7d39bc-796b-4ff9-ab26-5a5465e7cba66bc1b5; __stripe_sid=6bcbe5dc-eadd-4147-9e43-67e05ab6f2a52a7ebf; _gcl_au=1.1.1090066898.1747215865; CookieScriptConsent={"googleconsentmap":{"ad_storage":"targeting","analytics_storage":"performance","ad_user_data":"targeting","ad_personalization":"targeting","functionality_storage":"functionality","personalization_storage":"functionality","security_storage":"functionality"},"bannershown":1,"action":"accept","consenttime":1722613384,"categories":"[\\"targeting\\",\\"performance\\",\\"unclassified\\",\\"functionality\\"]","key":"898a3c45-4012-4e2c-af6f-d1f975173c03"}; _ga_RF4WWQM7BF=GS2.1.s1747215845$o1$g1$t1747216380$j37$l0$h1700230090',
}
for page in range(0,1020,30):
    print(page)
    json_data = {
        'searchQuery': {
            'sort': 'cache_recent',
            'searchTerm': '',
        },
        'pageSize': 30,
        'pageParam': page,
        'trendingId': 'f0cb9c5c-4bc3-4035-be39-95b4fc4c83c0',
        'readOnly': True,
    }
    
    response = requests.post('https://www.udio.com/api/songs/search', cookies=cookies, headers=headers, json=json_data)
    sj_lst = response.json()['data']
    for m in sj_lst:
        data = {}
        data['title'] = m['title']
        data['artist'] = m['artist']
        data['time'] = m['created_at']
        data['duration'] = m['duration']
        data['prompt'] = m['prompt']
        data['song_path'] = m['song_path']
        data['tags'] = '&'.join(m['tags'])
        lst.append(data)
    
result = pd.DataFrame(lst)
result.to_excel('第7块.xlsx',index=None)