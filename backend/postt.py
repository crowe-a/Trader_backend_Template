import requests
import hmac
import json,time


def geetest_validate(captcha_id,token,lot_number, captcha_output, pass_token, gen_time,user):
    # 1. Initialize GeeTest parameter information
    captcha_id = captcha_id
    captcha_key = token
    api_server = 'http://gcaptcha4.geetest.com'#https://gcaptcha4.geetest.com/verify

    # 2. Generate signature
    lotnumber_bytes = lot_number.encode()
    prikey_bytes = captcha_key.encode()
    time.sleep(1)
    sign_token = hmac.new(prikey_bytes, lotnumber_bytes, digestmod='SHA256').hexdigest()

    # 3. Prepare verification parameters
    query = {'captcha_id': captcha_id, 
            'captcha_output': captcha_output, 
            'gen_time':gen_time ,
            'lot_number': lot_number , 
            'pass_token': pass_token,
            'risk_type': 'icon',
            'userAgent': user}
#     query={
#     "status": "success",
#     "data": {
#         "lot_number": lot_number,
#         "result": "success",
#         "fail_count": 0,
#         "seccode": {
#             "captcha_id": captcha_id,
#             "lot_number": lot_number,
#             "pass_token": pass_token,
#             "gen_time": gen_time,
#             "captcha_output": captcha_output
#         },
#         "score": "90",
#         "payload": "AgFD8gWUUuHFx-XvpP7J2Qtq5RKOHhojCqzH6uKXlTQdv7WAI5STwloTGtXF_unpIPYdtY8SK2wsSNfg73KE6dSiop4g332uIJvgDs9gVWeOTm6xL9Xyi-dpWaDjbj_jEZAh-r4T-SYMqHBkLYc4HDe1NyJOk6wChcfgBR6K9UVqnvC2NWK8xLTiqg1mtPvO_AuC2QpXd9LRvc0bT3HRJUKFMQi1A8tI5rWOQKmNVQ7KZyklLZkiQX2AGul8ZQsYN3zeurdoY-vUB9oMNwtZNElRFjZiCqw8gdPm1jcNw2xbRk7UCP33VB6O-J6tled9mYshIS-3ByZ6vphzIhAR8n83Nq6OqxmFbTd-JYfUbTi7pMLGmbd2TlBkXnea7egtkVcY7hCEChUKwoVk1qfYR5GoeusnPYWdGvimRzlER6AjiQxPJ2Z0lYNhfsdk9FsMcZwdSmlvgAtoyBuiKPQJs27n9SVgoHud7uMOGhenfDk5IrtcW-opqhnpqGIaUPuw5HbpIVMKopPUTen5ls0g7PC8mN3B7bqj5wvn_HS_9srtyBn2Zs6_wjp5SDv6gGT-G-LCe_lWWiAO-uWTufhK99BGdtGlz4XnwMLilQ_AkWUqabRLEajZkadL_-mf5oVOMG5TACgbU9wm3_YzsizJU4CaeSG6OkIlI6ntAj-ULgi_7TGS6UjHEmpRYNeo-Ls5CNRAtkIuS4_vzAqM4SA8QDb5Pk-GHvzKIT4rvClR3ZHld3BHUKcixZ0LF2CPhXLynuVj1zEwtiZSrZYdA3dHEGnt8aZ1CbxoLLpLsipY33Ll8v2UoM7Gqy1MXtOG-2LDDaRmnqVWYGdhTO-Z94YCbSmsZPvxpBCpmONKYbfXA3ar9_8cPDTIk5bHK9WC5cEbjdGANUIwJQqndpDvQJqh-3dh7Dge6hoZp1WxZRcc4LvB0kAK8jvJdSFjT9kRATpBbzEBmLijyod5N3PEGtbihZLyh9XUwsJYhyr7Nw4rrSLphUcx2Mz2ooBWgddJToy77Vjd-QvsFW1q5ZuGY1KMLE2gL3FNPtjhCMIWU1FTtAeBBRQ9fWC6xwRtpSByrLWXqKTliaXsR-DKgkRgScWEanRlc3LwZW1n2uCNa_iBv7JVApO3jfhJxnjPdnpBGL43e_Bo91ujtNWXHBWfRYvam3Fy_F37kqD7DskcGB4h0o5hz1FtROTBXxeKiQByoy8igTrfn-V9Sgxe81ASWYyraVH8E_SAOIyEhL5Zh9IZ-5rZG_Usv7FYXtwiy3AKjNCAH8W71eeuSpn2yTzAno2XZ8cOTOGuyTp8lcLMoJ9YLaP09-mo0poXYwYOf7n5tfyc9KQL9Z9a3qUU0iJNWdfu3vnQzuFGwmnaXUe__C9CWNlugNtBESUfBqUu7_KYolFJDY8AHFc5GLSuuLDNvUx2RIxNWjhQ4Jrm060Scf43zsa0wQtx4zBW87my-8lh62YK1Wf7B1iy3bP0khJfhm5-4-D-gGb-wnvXoIdm9e7T0qH5JT2EzYoSdprO_J4YMyi3YdjXE-suc-CD8munN_z6yRU7H3Pl65fXrTA7cpT06uILDT1llfCaleLGweqPBtMR509ZOipytP7BH8cSnfW-MEevqUlup85sEM0VqHnM2S3Lsfk1AAApjh6bvrV9QL82TNxaBpZBnSUh2ro31-jeDeyjqjpofLL1TPtJ5xm_Wni3sO7_EhMzHuk_RCkBFp3ZgyyCw8PJHB448qXTl0gWkvBrqnPQur57LnWWei-NmabsoPAeMvZhM5xAUzVd2n1iFD6d2k-p29E-ziNHkJ--tiagrvmQF_4CZKOJWC3ULkuxBLRMya5bZyoaNfZR66N6cL9Xkfdz4TQqZwzgBpVuTcryD2tZmYS9Na8eM1K93ycaI4L0FUzRb-n4xjE1v5DFonbeiULB0mkTAadrCCqd0bmueORQzpPeahNK8iNYRsfQzxeFP0ZSb5dDWgZMr63B2XbfENsYJ3Hs_ra4NHVtP1TLzEvTaK-zUzfy8O6RUGhC6SCwX_FL6elw1evEXoiWlVLfDu3el8IobUJ9W0I4cz-Q-4EmBuKSVTl5ioCBwM1ov0do4OvHrrnDkSWYfDxobjJL8FjE0TCSA9l1JrfKxOrq8hZI8XaSboBCfnTTDOA3K3WMhZ5FRGjJd7LUZSUkD0tsjr8FqiIkUYtwQzj89Psw6ad9PomvQ7xedT-6OPMCsdyqViQdl3zU-LNiaeKhoGdgWj8qI-5JfiP3Zko0AEY1-EITRy2pykbGshy4vZr_1fP3sbw5sFcArNT3CdQ5sXJ5DmyQsvlxRNg9WBdzOIi63s_UCFd46FxZjPYWx5a1tf5iv46hVoraaozeuFQI0NTk2QBQFKXLu3yyeOrfkk8v2XHqA9qmkP_JnW7c8LGdKEMPE-uIZFFwuVw5RYNfhtrxyXcPgQUWHePDy6B2rDqh-ehcG2U0aqyWC9MkliUAtszy6E3QvQmmtleXqHz04_qK2yAEvabacigHv0NUfOhismVvzaSD_7za1zZDURHEHEyoutEymK3a3FtoSieWooR3CpPANSpsclJJar2g2tzf7UM3y5Oi7PisGprV0d33WSFtN7dfU3U2a-WRfIMyvRmGjRRzcjVFzgzTkDfd8Vi1837vXB3GDtZD2y39_CXpL-4Goqep7V4kn-gnZRBd7AjnOrU8Q1cBLXyWd8GYt0GN9NWjn4e5qCROWu7YhPmIRnvzZ__XVqGizTLTy7RMlVPcs_5XeTx_UAfiR3YRN3aiGIgrF0I8gozckOqW6sRnpxnuuyFPRHvcXCgvKWASbllZAR5LPzyNxvT0bVTN3YOyLFY_WUtO7HgI4GR2iB_VpnbJqUA2kcT4RQVYI0lTNAgFRzh5xrlr479Ap32rxvOMEeoqnZPAk-y8iBaascOQ9G-s_mxrwJZh3mb9y6oHDjSXsSvKt0GBFPVYnBxFoHEiXfgh_GKElifjKvNB4zIvLL-mYNTH22QvFlTOwnuqQ5HfJDDeTFxqvKfbqJadQ8Hi_IPQcITpWm435FSzvXAsjK2rTPEPojpjktxcBTCFDKh2X0SGljfNZzAX0zZeBXHhfVD8IqTFrjwAZQ1k0Fk5CgJUtPhEYKaJcurG4vnHS3e241D16S9weybk6Z93tyrpRE7dVw0gIqz1NVJS4Cbu2VWBF1mBLw1dDSiwHeKxh8KnB8lNwP5Z9LVD59_zBFWnXACC6wHsupszk6-7ILyIHDmqaf8mObNpZnNlaZ0VN6_9QJAaDRaNk7tY_SdBuTxqEnDt2ekPMeuPqmLfbjbl_GYTGI-p-wfyBD4IYt8sRXivt1OBscAAVW1Pfr3K9AldCCJ9gNN98zSrr9Dcv1xy5FFBLa5wTgzw0mge9sKc",
#         "process_token": "667e2398913dc26a439b14db089d3920ae5febe8f83c86d934de72d94ec4046a",
#         "payload_protocol": 1
#     }
# }
    
    
    #url = f"{api_server}/verify?callback=geetest_{gen_time}&captcha_id={}&captcha_output={}&gen_time={}&lot_number={}&pass_token={}&risk_type={}&userAgent={}&"
   
    url = f"{api_server}/verify?callback=geetest_{gen_time}"
    time.sleep(1)
    try:
        # 4. POST request with json payload
        res = requests.post(url, json=query)
        res.raise_for_status()
        gt_msg = res.json()
    except Exception as e:
        print("hata1")
        gt_msg = {'result': 'fail', 'reason': 'request geetest api fail'}
    time.sleep(1)
    # 5. Return verification result for business logic
    if gt_msg.get('result') == 'success':
        print("succes")
        return {'login': 'success', 'reason': gt_msg.get('reason', '')}
    else:
        return {'login': 'fail', 'reason': gt_msg.get('reason', '')}

# simple:
# result = geetest_validate(lot_number, captcha_output, pass_token, gen_time)
# print(result)
