#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串，自动提现需要自己抓包
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可
# 分享一篇文章，找到 put.json 的请求，拷贝请求体，放入对应参数
cookies1 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1614518622,1614518706,1614519687,1614519702; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1614518622,1614518706,1614519687,1614519702; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2249606658%22%2C%22%24device_id%22%3A%22177d75c283537f-0448be6c558cf1-754c1351-370944-177d75c283610ac%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177d75c283537f-0448be6c558cf1-754c1351-370944-177d75c283610ac%22%7D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2249606658%22%2C%22%24device_id%22%3A%22177d75c7ec91257-01184aa34829048-754c1351-370944-177d75c7eca11e1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177d75c7ec91257-01184aa34829048-754c1351-370944-177d75c7eca11e1%22%7D","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=0fa4b0ee165f5625c4eded4a009fbbf9&sign=4640eedac8accd32c4a99dbb3e3e5af0&channel_code=80000000&uid=49606658&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=aebb65b92c4e678d204083af4609715f&openudid=0fa4b0ee165f5625c4eded4a009fbbf9&device_type=1&device_brand=iphone&sm_device_id=2021012616463582c8c62cdd9f0c469a6f2bf555253b56010b24df97aac2cd&device_id=50015433&version_code=200&os_version=14.4&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWKyt42whaKOl7CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfsLmurIGvfbKEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWKyt42whaKOl7CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfsLmurIGvfbKEY2Ft&cookie_id=aebb65b92c4e678d204083af4609715f","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTcytgUVRgcM9nTByBYEMCphZtrL34IfUTdhoeF4kO_vIleB9-uwUV3fCDNdrm2ORyLU8p31xFkusLGcClpAvzN6G777mMmb2MgUOT55k-mvTK6Z9wWSXdpXRjjkYFZUR4EcucJrTN2MQimskWbG3vumbxfQwM3AQkv2Yo265yqzLfOaNDH6yzxCW6EgsTVpVHSYGPQGBA-33a5neRSZNcDluey5P3n4aeErXdprxelyKYb71rhINSpaw1hf5N5j9FHduuvJPtXHV0vduLy8HmwvB2QR4BEDQiUX5mWLZMYTv6BTQd8q1lzWcdXV7Zu7xWTkMqelbnXuhGa4WH0onjRe1Q4OMj56BAd83IEvJomAjgsbmu8D5sUIwcO8HL0Ps75mVIlDFQX03VplSmiO6uBWMg1g6-PieCNsKrLrV48PxPHc0lmiXuPsqXhhjQy5-HVz9nrHYgQ2VbMZw6UMryrtDdg-8qMzLkHtVrVRmjALfwWHNua9ukgBsYZY-gcCew0yAVY30ehEsCzA7QINb-qzYZVn5EvJ2mS8ckYv_zGihJE6iz4kUg4_0E8fVXVuEyc2P64AIPq98EHG9L8-ldZjPVrLKSwPKfbP_HpfvsVQiz1_SFvP1YCbvDH26e_jkCDazTP5PNIn2TEmfd_Op36qCYSUtqFR7YyNRkaetOZ7kQ%3D%3D',
  'YOUTH_REDBODY': '',  
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTcytgUVRgcM9nTByBYEMCphZtrL34IfUTdhoeF4kO_vIleB9-uwUV3fCDNdrm2ORyLU8p31xFkusLGcClpAvzN6G777mMmb2Mi6ZAeO2i5Z9zzgItR3h8EXUf1VRbLZskPEnuD5l9p1yx8c4l8eJW_NS9YzcbRuMwATHfhCfVfNx3_zijES-7NUK37CsKDm-EPEZgkCSkGZiUWDAsnXZP7l_AsmiquQTmwDtjuiHpNo-N0wLS1D28fu-Gzd1-lMLRCnRnHurMF1NWDpYnD7ThTK6JMtD4YF5tQpfyAcuEhoRR8h7KCEtia48zskuQAtGBJDEKEz4kwF1KVZ6bqXSmypwh7we8s4B9LqJH_3dEviiw-e0Wz_njSdNeRYv0rXUje7qUSRpkxC_jCxjplnTD26gBlfbMPmCtr3XPBxDOMswnG-tXpFlz5h3zG2QBn3lXp6qhMlxmsVXx74iPnO7sXnrJJ_KPTBxZFMA8CfcBnrFfk9tTl8OU1H92_16DMmrlq2cj8K0yfwuhGBCRGrjkKOxqDQFteOYVsjOnLjuJCTmtKc0rM_W5rzXwqrSFFQhia8xMa_5_HfjHHs-QOX7mdTL0Q-ji9I3GWBuqGvTupyX5g4wVz8VjUoUEbq-ZCBJiXLGhtreB1clGUhV7Vi_ksOabZcvi4Aheo%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.0&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.0&device_brand=iphone&device_id=50015433&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=1&openudid=0fa4b0ee165f5625c4eded4a009fbbf9&os_version=14.4&phone_code=0fa4b0ee165f5625c4eded4a009fbbf9&phone_network=WIFI&platform=3&request_time=1614520981&resolution=828x1792&sm_device_id=2021012616463582c8c62cdd9f0c469a6f2bf555253b56010b24df97aac2cd&szlm_ddid=D2fS7jFh3rh69j4lBvADilmar3ZsC6ofPeECXmh7wlq7AXd8&time=1614520982&token=38f2064c62802da79d4991da7fe9afa4&uid=49606658&uuid=0fa4b0ee165f5625c4eded4a009fbbf9'
}
cookies2 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2253276019%22%2C%22%24device_id%22%3A%22177f2fe10fd10a-026662adba7528-754c1351-370944-177f2fe10fe701%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177f2fe10fd10a-026662adba7528-754c1351-370944-177f2fe10fe701%22%7D; sajssdk_2019_cross_new_user=1","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=0fa4b0ee165f5625c4eded4a009fbbf9&sign=4783b32156bbb0841eb3aef25609485a&channel_code=80000000&uid=53276019&channel=80000000&access=WIfI&app_version=2.0.2&device_platform=iphone&cookie_id=c62b8749d330d02382e60d1610000c63&openudid=0fa4b0ee165f5625c4eded4a009fbbf9&device_type=1&device_brand=iphone&sm_device_id=2021012616463582c8c62cdd9f0c469a6f2bf555253b56010b24df97aac2cd&device_id=50015433&version_code=202&os_version=14.4&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66rrWWxzXWxhoyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3hWuGfKDgsLm2apqGcXY&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66rrWWxzXWxhoyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3hWuGfKDgsLm2apqGcXY&cookie_id=c62b8749d330d02382e60d1610000c63","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBCEif5kxttnpywiuywli8nWaoHM8H0lyEPajpOK1cTnePIU5tb44C4NA0dSWC8BATtHy3NKrYK-V1Nf6hszDytNorMq0O4QggzesHQ8ENHZOnqSQmINqv8OifElavsyySZdzB-Dxl_uWpqaTeAwMDoQxpKUPOn8I6CUBSopbAKdrMzO08NBQeM0hNGgdicmEaWyQ2V_k6CxX2OpQ2KdKGj94qZKyppF5KBlry7MJZPTmu6SWnZLsFXsuR9Zr1qIh6iI6-MThPx8g4rwPhNl_4JxzcGlmZqE9QLP_0fB8J0Cw__R7vXqgGp0iK9XZVqsiEkAjoYr32K5AZaFexAHXkB_84Gb0lAqBL2s2pCCTsIBoUzKZ9m3PoxYE1y4SpSp-yum_q5ewJJEl4A3Irx88noDafMrdfhejb3ZAk431ZBZVym0ot0gNNw8QIh_qnatfVbOToBY1mubydtdhnRm7b57UrWBVax9Qs3YJYDcFLBI27rDkhWLET30NMHM6XV4IuAeYs0J9__UrKsb6d0zMcTR1_9ScEzg-W_3QttWkdGTJkcJ_Hl2b8yRGCW6fQpUcIICZ6Fm80XQ0GzoR-v_w-TSBgvIMW-Z89x01pUqovuz00OWG8I5AdST7pzMj_uuhP4IsgRWBSxIq3uy0sXsZa9HTkdPdk3lkUJ3ZRDSxmg_1Q%3D%3D',
  'YOUTH_REDBODY': '',  
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBCEif5kxttnpywiuywli8nWaoHM8H0lyEPajpOK1cTnePIU5tb44C4NA0dSWC8BATtHy3NKrYK-V1Nf6hszDytNorMq0O4QggyBBdEgbe_ZsOv8mOJo_GsXlVSwA_CQ8DLvoC3TSAhd-kQR7OyJtA8pcoQSeLtciYxboPY4Dk592RawKi7iXjA4_zmVHLx8_NZfl_bqmCNE0rK2MALlMxyfrAXklNggTX4xbMPju355nUKilZEHSfAMiVV6h6m4in8aUkH66JzEMpriaoaRnmxHwR3yDR-KNJGmaJ7zOHD8Q6ErgPGlVtmUd870rsZivcD_nfNJBbka3DO2ZhjI4dt2wFwC0Yzrpdg7Hre8MqtskcP0c9pwHq01pDpmQIihiXfdD3D236qN5cu5f7vlznXQW-LWLDOBJlltmNXWSqnDbPhmND1YpgnXqNu8Wcy703xwlVZGsu71ZWQ4n8fyaYCOzXiUt1XjYJAKkgHrEYD6BVU1BtM8CFOBvjXt_FMAO44BLfjXEmDZz59JI7vQNOxPILsr2hVzCJ_YvO5Qs_K2Td9Jo12ie8guuxVkb7AzQEIWyrZxSdLisTPMFbyJ6IT7-PElUu_FMXm8-7YBhUNeftTL6qYxU_wO4WiA2DTWn3ZCqX0cKsfl-OTyII3EmnRxv24dcjUN8BA%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.2&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=50015433&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=1&openudid=0fa4b0ee165f5625c4eded4a009fbbf9&os_version=14.4&phone_code=0fa4b0ee165f5625c4eded4a009fbbf9&phone_network=WIFI&platform=3&request_time=1614689858&resolution=828x1792&sm_device_id=2021012616463582c8c62cdd9f0c469a6f2bf555253b56010b24df97aac2cd&szlm_ddid=D2brVva7pvhBWQS6RN1fRiAsKF2/0QNYhtt6UZzFTN47wX6f&time=1614689858&token=cc218601a6a90b050cf3d4b53daf997d&uid=53276019&uuid=0fa4b0ee165f5625c4eded4a009fbbf9'
}
cookies3 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"Hm_lpvt_6c30047a5b80400b0fd3f410638b8f0c=1615806236; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1615806236; Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775=1615806236; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1615806236; sajssdk_2019_cross_new_user=1; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2254440466%22%2C%22%24device_id%22%3A%22178358e7c6bbda-09a9d1e4287338-754c1351-370944-178358e7c6ce0d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22178358e7c6bbda-09a9d1e4287338-754c1351-370944-178358e7c6ce0d%22%7D","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=0fa4b0ee165f5625c4eded4a009fbbf9&sign=b03d57bf0c97ee47be00f68b9e4bef6a&channel_code=80000000&uid=54440466&channel=80000000&access=WIfI&app_version=2.0.2&device_platform=iphone&cookie_id=2034dc6cf00600ed3a67b6e6c50b9f46&openudid=0fa4b0ee165f5625c4eded4a009fbbf9&device_type=1&device_brand=iphone&sm_device_id=2021012616463582c8c62cdd9f0c469a6f2bf555253b56010b24df97aac2cd&device_id=50015433&version_code=202&os_version=14.4&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp4VphHyGmK_OqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqXsKmiZYGJn2mEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp4VphHyGmK_OqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqXsKmiZYGJn2mEY2Ft&cookie_id=2034dc6cf00600ed3a67b6e6c50b9f46","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBCEif5kxttnpywiuywli8nWaoHM8H0lyEPajpOK1cTnePIU5tb44C4NA0dSWC8BATtHy3NKrYK-V1Nf6hszDytNorMq0O4QggzesHQ8ENHZOlF0p6YPeVEIWHEjB33j1AUdqEjGHMEPYL1Y_IpEaYWpsOWpvhMoC6WXXsnrAykt8W08E_2zDtvWQvwoQ_YGu8ck8cGr5NPrOrZ7xsji4AEHopKaJ2KTbSqODRMb0rGE8lRyocge0fegicUXjRCBDMMqAWrXw8qPuTnnH2vPSkc1UUg2Z-OtlfQiJjoCLPyubZaY6NpKf8qUju66-DIe8dGwVdJwfb6zzSKWq3CWZOVSnqCvoQ2USVFzNjSuLICsG-1eNKfgVQvNI9ifTIP_Wns0_GK2Y2nsRnMKebRS8E7jANx83UqZd3Et1_0rzy5npigIky_vMfx39APLz9nUwQoEZ9yUbhXgcy3SkW6_DcP8KcYqtJxm_DEU2Zjt34z3q2vNOOOpFJ5qZ9dwGDxpSFC8IX9e5F8KbscdWJ-pppSz0oS3P_A1snEWnxyAEWvVeNKUoWHZGxYsXYfGVoiv9yIunCUw-4S6_UqrIau3XQdYf74fcCN5coyIqgL-XyGJ8tUstS24vGbQU_UFSF_4GZWgJhzV2S9ht5FerWMb8OtQk1CzYB50rO2_SlyRIQ-eRQ%3D%3D',
  'YOUTH_REDBODY': '',  
  'YOUTH_READTIMEBODY': '"p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBCEif5kxttnpywiuywli8nWaoHM8H0lyEPajpOK1cTnePIU5tb44C4NA0dSWC8BATtHy3NKrYK-V1Nf6hszDytNorMq0O4QggyBBdEgbe_ZsOv8mOJo_GsXlVSwA_CQ8DLvoC3TSAhd-kQR7OyJtA8pcoQSeLtciYxboPY4Dk592RawKi7iXjA4_zmVHLx8_NZfl_bqmCNE0rK2MALlMxyfrAXklNggTX4xbMPju355nUKilZEHSfAMiVV6h6m4in8aUkH66JzEMpriaoaRnmxHwR3yDR-KNJGmaJ7zOHD8Q6ErgPGlVtmUd870rsZivcD_nfNJBbka3DO2ZhjI4dt2TJ3dZFoDi4Z8EzHEgJj89U7xzRkywI7MG3Now6OlI_EVogaMVwyip1tcY1yCYqbob89iJVVBvNpV9_W9j8_ubYL9EHcSmyGSoPQCWf0TIBpDz_8qzIFyyYcCLk-RjZ_xLtSrhez_OSs160td7PBSkdZ-Gx2LArnNpgiXghXaBzeFt44B_ULe-VWOlk6Ljp3TGlAry3sW0Y--xmj0SH5TJi0POs-fgmbSTz9wx1vg91DV2vkhaZCitjZB4nIt5mGXYDu-I2hRR1AL7qMpN8lDHKoxr-xSs52B3sLwqMRd-B5BruYoAUMLRN4cjz7v5sY7PTPxqJGXWJ8%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.2&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=50015433&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=1&openudid=0fa4b0ee165f5625c4eded4a009fbbf9&os_version=14.4&phone_code=0fa4b0ee165f5625c4eded4a009fbbf9&phone_network=WIFI&platform=3&request_time=1615807535&resolution=828x1792&sm_device_id=2021012616463582c8c62cdd9f0c469a6f2bf555253b56010b24df97aac2cd&szlm_ddid=D2brVva7pvhBWQS6RN1fRiAsKF2/0QNYhtt6UZzFTN47wX6f&time=1615807536&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJwaG9uZV9uZXR3b3JrIjoiV0lGSSIsInRpbWUiOiIxNjE1ODA3NTM2IiwiYXBwX3ZlcnNpb24iOiIyLjAuMiIsInBob25lX2NvZGUiOiIwZmE0YjBlZTE2NWY1NjI1YzRlZGVkNGEwMDlmYmJmOSIsInN6bG1fZGRpZCI6IkQyYnJWdmE3cHZoQldRUzZSTjFmUmlBc0tGMiUyRjBRTllodHQ2VVp6RlRONDd3WDZmIiwiZGV2aWNlX2lkIjoiNTAwMTU0MzMiLCJtb2JpbGVfdHlwZSI6IjIiLCJjaGFubmVsIjoiODAwMDAwMDAiLCJ1dWlkIjoiMGZhNGIwZWUxNjVmNTYyNWM0ZWRlZDRhMDA5ZmJiZjkiLCJyZXNvbHV0aW9uIjoiODI4eDE3OTIiLCJuZXRfdHlwZSI6IjEiLCJjaWQiOiI4MDAwMDAwMCIsImFjY2VzcyI6IldJRkkiLCJvcGVudWRpZCI6IjBmYTRiMGVlMTY1ZjU2MjVjNGVkZWQ0YTAwOWZiYmY5IiwidWlkIjoiNTQ0NDA0NjYiLCJwbGF0Zm9ybSI6IjMiLCJjbGllbnRfdmVyc2lvbiI6IjIuMC4yIiwicmVxdWVzdF90aW1lIjoiMTYxNTgwNzUzNSIsIm9zX3ZlcnNpb24iOiIxNC40Iiwic21fZGV2aWNlX2lkIjoiMjAyMTAxMjYxNjQ2MzU4MmM4YzYyY2RkOWYwYzQ2OWE2ZjJiZjU1NTI1M2I1NjAxMGIyNGRmOTdhYWMyY2QiLCJpc25ldyI6IjEiLCJkZXZpY2VfbW9kZWwiOiJpUGhvbmUiLCJkZXZpY2VfcGxhdGZvcm0iOiJpcGhvbmUiLCJkZXZpY2VfdHlwZSI6ImlwaG9uZSIsImRldmljZV9icmFuZCI6ImlwaG9uZSIsImNoYW5uZWxfY29kZSI6IjgwMDAwMDAwIn0.i9Pk2-LHYJW_wqROZ6rCm3KupHfy9L0MniUKq-dDduruEv2ZsU-grfNim1jcNixo5lhBYiihFwA4vcv9mSi5Xg&uid=54440466&uuid=0fa4b0ee165f5625c4eded4a009fbbf9'
}
COOKIELIST = [cookies1,cookies2,cookies3]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = f'YOUTH_HEADER{str(i+1)}'
    readBodyVar = f'YOUTH_READBODY{str(i+1)}'
    redBodyVar = f'YOUTH_REDBODY{str(i+1)}'
    readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
    withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
    shareBodyVar = f'YOUTH_SHAREBODY{str(i+1)}'
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and redBodyVar in os.environ and os.environ[redBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies'+str(i + 1)]["YOUTH_REDBODY"] = os.environ[redBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_SHAREBODY"] = os.environ[shareBodyVar]
      COOKIELIST.append(globals()['cookies'+str(i + 1)])
  print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"

def get_standard_time():
  """
  获取utc时间和北京时间
  :return:
  """
  # <class 'datetime.datetime'>
  utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
  beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
  return beijing_datetime

def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
  """
  签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/sign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def signInfo(headers):
  """
  签到详情
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/getSign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到详情')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def punchCard(headers):
  """
  打卡报名
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/signUp'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('打卡报名')
    print(response)
    if response['code'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doCard(headers):
  """
  早起打卡
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/doCard'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('早起打卡')
    print(response)
    if response['code'] == 1:
      shareCard(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareCard(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
  endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
  try:
    response = requests_session().post(url=startUrl, headers=headers, timeout=30).json()
    print('打卡分享')
    print(response)
    if response['code'] == 1:
      time.sleep(0.3)
      responseEnd = requests_session().post(url=endUrl, headers=headers, timeout=30).json()
      if responseEnd['code'] == 1:
        return responseEnd
    else:
      return
  except:
    print(traceback.format_exc())
    return

def luckDraw(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/luckdraw'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('七日签到')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def timePacket(headers):
  """
  计时红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}TimePacket/getReward'
  try:
    response = requests_session().post(url=url, data=f'{headers["Referer"].split("?")[1]}', headers=headers, timeout=30).json()
    print('计时红包')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def watchWelfareVideo(headers):
  """
  观看福利视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/recordNum?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('观看福利视频')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers, body):
  """
  分享文章
  :param headers:
  :return:
  """
  url = 'https://ios.baertt.com/v2/article/share/put.json'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('分享文章')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def threeShare(headers, action):
  """
  三餐分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareNew/execExtractTask'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  body = f'{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('三餐分享')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def openBox(headers):
  """
  开启宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/openHourRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('开启宝箱')
    print(response)
    if response['code'] == 1:
      share_box_res = shareBox(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareBox(headers):
  """
  宝箱分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/shareEnd'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('宝箱分享')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendList(headers):
  """
  好友列表
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友列表')
    print(response)
    if response['error_code'] == '0':
      if len(response['data']['active_list']) > 0:
        for friend in response['data']['active_list']:
          if friend['button'] == 1:
            time.sleep(1)
            friendSign(headers=headers, uid=friend['uid'])
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendSign(headers, uid):
  """
  好友签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友签到')
    print(response)
    if response['error_code'] == '0':
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def sendTwentyScore(headers, action):
  """
  每日任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print(f'每日任务 {action}')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchAdVideo(headers):
  """
  看广告视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data="type=taskCenter", headers=headers, timeout=30).json()
    print('看广告视频')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchGameVideo(body):
  """
  激励视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
  headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('激励视频')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def visitReward(body):
  """
  回访奖励
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/mission/msgRed.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('回访奖励')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def articleRed(body):
  """
  惊喜红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/article/red_packet.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('惊喜红包')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def readTime(body):
  """
  阅读时长
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/user/stay.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('阅读时长')
    print(response)
    if response['error_code'] == '0':
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def rotary(headers, body):
  """
  转盘任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘任务')
    print(response)
    return response
  except:
    print(traceback.format_exc())
    return

def rotaryChestReward(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘宝箱')
    print(response)
    if response['status'] == 1:
      i = 0
      while (i <= 3):
        chest = response['data']['chestOpen'][i]
        if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
          time.sleep(1)
          runRotary(headers=headers, body=f'{body}&num={i+1}')
        i += 1
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def runRotary(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('领取宝箱')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doubleRotary(headers, body):
  """
  转盘双倍
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘双倍')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def incomeStat(headers):
  """
  收益统计
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=50).json()
    print('收益统计')
    print(response)
    if response['status'] == 0:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def withdraw(body):
  """
  自动提现
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('自动提现')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def bereadRed(headers):
  """
  时段红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}Task/receiveBereadRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('时段红包')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = f'📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account['YOUTH_HEADER']
    readBody = account['YOUTH_READBODY']
    redBody = account['YOUTH_REDBODY']
    readTimeBody = account['YOUTH_READTIMEBODY']
    withdrawBody = account['YOUTH_WITHDRAWBODY']
    shareBody = account['YOUTH_SHAREBODY']
    rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += f'\n【账号】：{sign_info["user"]["nickname"]}'
      content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
      result += f'【账号】: {sign_info["user"]["nickname"]}'
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
    shareArticle(headers=headers, body=shareBody)
    for action in ['beread_extra_reward_one', 'beread_extra_reward_two', 'beread_extra_reward_three']:
      time.sleep(5)
      threeShare(headers=headers, action=action)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
    # article_red_res = articleRed(body=redBody)
    # if article_red_res:
    #   content += f'\n【惊喜红包】：+{article_red_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

    rotaryChestReward(headers=headers, body=rotaryBody)
    for i in range(5):
      watchWelfareVideo(headers=headers)
    timePacket(headers=headers)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward', 'first_share_article']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += f'\n【{group["name"]}】：+{group["money"]}青豆'
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 300000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += f'\n【自动提现】：发起提现30元成功'
          content += f'\n【自动提现】：发起提现30元成功'
          send(title=title, content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

      result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
      content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

  print(content)

  # 每天 23:00 发送消息推送
  if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 5:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 23:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
