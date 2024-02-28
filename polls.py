def polling(s):
    emotes = ['🟢', '🔴', '🟡', '🔵', '🟠', '🟣', '⚪', '⚫']
    
    s = " ".join(s)
    s = s.split(":")
    q = s[0]
    a = s[1].split(",")
    
    mess = "# **" + q + "**" + '\n'
    for i, e in zip(a, emotes):
        mess += e + " " + i + '\n'
    reactions = emotes[:len(a)]
    return mess, reactions
