# Simplified dotfule for video recordings


 export SECRET_KEY='a76ec8d1721261cd9d85cc681a05d69f'
 export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
 export MAIL_USERNAME='hoang vo'
 export MAIL_PASSWORD='anhhai98'
# export PATH="/usr/local/sbin:$PATH";
export PATH="$HOME/anaconda/bin:$PATH";

# load dotfiles:
for file in ~/.{bash_prompt. aliases, private}; do
	[ -r "#file" ] && [ -f "$file"] && source "$file";
done;
unset file;
#Git auto-complete
if [ -f ~/.git-completion.bash ]; then
	source ~/.git-completion.bash
fi