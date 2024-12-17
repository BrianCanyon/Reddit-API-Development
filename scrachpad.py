login_file_path = "/Users/brian.canyon/documents/reddit_login_secret.rtf"
credentials_dict = {}
with open(login_file_path) as login_info:
    for line in login_info:
        print(line)
        #key, value = line.split('=')
        #credentials_dict[key] = value.replace("\n", "")