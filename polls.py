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


from poll_dict import PollDict
def polling2(s):
    emotes = ['🟢', '🔴', '🟡', '🔵', '🟠', '🟣', '⚪', '⚫']
    emotes_special = {'pizza': '🍕', 'coffee': '☕', 'ice_cream': '🍨',
                      'computer': '🖥️', 'plane': '✈️', 'vision': '👁️',
                      'language': '📝', 'train': '🚅', 'bike': '🚲',
                      'bus': '🚌', 'car': '🚗'}
    emotes_temp = []
    s = " ".join(s)
    emote = None
    question, answers = map(str.strip, s.split(':'))
    mess = f"# **{question}**\n"

    for i, answer in enumerate(map(str.strip, answers.split(','))):
        word_elements = word_check(answer.lower())
        for element in word_elements:
            if element in emotes_special and emotes_special[element] not in emotes_temp:
                emote = emotes_special[element]
                break
        else:
            for emoted in emotes:
                if emoted not in emotes_temp:
                    emote = emoted
                    break

        mess += f"{emote} {answer}\n"
        emotes_temp.append(emote)

    return mess, emotes_temp


def word_check(sentence):
    dictionary = PollDict()
    emotes_dict = dictionary.emotes_dict

    matching_types = []
    for emote_type, keywords in emotes_dict.items():
        if any(keyword in sentence for keyword in keywords):
            matching_types.append(emote_type)
    return matching_types


