export ZSH="$HOME/.oh-my-zsh"
plugins=(git zsh-syntax-highlighting zsh-autosuggestions)


source $ZSH/oh-my-zsh.sh
source $HOME/.config/zsh/.zshenv
source $HOME/.config/zsh/alias.zsh

eval "$(starship init zsh)"
