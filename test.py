with open("amazon_links.txt","r") as link_data:
    lines = link_data.readlines()
    link_list = [i.strip("\n") for i in lines if i!="\n" and i!=" \n"]

