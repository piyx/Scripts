import os
from pathlib import Path
from github import Github
from dotenv import load_dotenv

load_dotenv('.env')

base = "C:\\Users\\piyx\\Desktop\\repos"
base_path = Path(base)

change_command = '''
git filter-branch -f --env-filter \
"GIT_AUTHOR_NAME='AUTHOR_NAME'; GIT_AUTHOR_EMAIL='OLD_EMAIL_GOES_HERE'; \
GIT_COMMITTER_NAME='COMMITTER_NAME'; GIT_COMMITTER_EMAIL='NEW_EMAIL_GOES_HERE';" HEAD
'''

push_command = '''
git push origin +{branch_name}
'''

token = os.getenv("GITHUB_TOKEN")
g = Github(token)
user = g.get_user()

for dir_name in os.listdir(path=base_path):
    repo = g.get_repo(f'{user.login}/{dir_name}')
    branch_name = list(repo.get_branches())[0].name
    repo_path = Path(base+'\\'+dir_name)
    os.chdir(repo_path)
    os.system(command=change_command)
    push_command = f'git push origin +{branch_name}'
    os.system(command=push_command)
