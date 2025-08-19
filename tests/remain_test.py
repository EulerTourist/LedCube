PanW = 4; panAcross = 5; panDown = 4
# 00,01,02,03,04
# 05,06,07,08,09
# 10,11,12,13,14
# 15,16,17,18,19

turns_idh_idx = ['12', '3', '6', '9']
for d in turns_idh_idx:
    for pan in range(panAcross*panDown):
        # i = panAcross * v_idx + h_idx
        h_idx = pan%panAcross
        v_idx = pan//panAcross
        border = ''
        pan1 = ''

        if d == '12':
            if v_idx == 0: 
                border = 'border'
                v_idx = panDown-1
            else: 
                v_idx -= 1
        elif d == '3':
            if h_idx == panAcross-1: 
                border = 'border'
                h_idx = 0
            else:
                h_idx += 1
        elif d == '6':
            if v_idx == panDown-1: 
                border = 'border'
                v_idx = 0
            else:
                v_idx += 1
        elif d == '9':
            if h_idx == 0: 
                border = 'border'
                h_idx = panAcross-1
            else:
                h_idx -= 1
        pan1 = panAcross * v_idx + h_idx

        print(d, pan, "->", h_idx, v_idx, border, pan1)

    print()