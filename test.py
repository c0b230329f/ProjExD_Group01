syp_lst = [
        "20××年、東京工科大学のマスコットキャラの,こうかとんが何らかの力によって邪悪な存在へと,変貌してしまった。", 
        "邪悪な存在となったこうかとんは学生の単位と学部長賞を奪っていった。", 
        "そこで立ち上がったのは、プロジェクト演習Dチーム3であった。", 
        "こうかとんの手下とこうかとんを倒すため、いざ出陣！"
    ]

for tx in syp_lst:
    txt_len = len(tx)
    #print(txt_len)
    if txt_len > 30:
        print(tx[:20])
        print(tx[20:40])
        print(tx[40:])

for j in range(20, 60, 20):
    print(j)