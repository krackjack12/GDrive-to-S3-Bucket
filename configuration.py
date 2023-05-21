import configparser

config = configparser.ConfigParser()

config.add_section("aws_s3")

config.set("aws_s3","name","s3")
config.set("aws_s3","region_name","ap-south-1")
config.set("aws_s3","bucket_name","")
config.set("aws_s3","access_key","")
config.set("aws_s3","access_secret","")


config.add_section("gdrive")

config.set("gdrive","scopes","https://www.googleapis.com/auth/drive")
config.set("gdrive","client_secret_file","client_secret.json")
config.set("gdrive","application_name","")
config.set("gdrive","folder_id","")

with open("config.ini","w") as file:
    config.write(file)