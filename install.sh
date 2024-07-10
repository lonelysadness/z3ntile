#!/bin/bash
set -e
set -o pipefail

trap 'printf "Cleaning up temp folders...\n" >&2; rm -rf "$TMP_DIR"' EXIT

INITIAL_PWD=$(pwd)
TMP_DIR=$(mktemp -d)

COL_RESET="\033[0m"
COL_RED="\033[31m"
COL_GREEN="\033[32m"
COL_YELLOW="\033[33m"

BASE_PKGS="qtile python-psutil feh xorg ly kitty python-dbus-next xdg-user-dirs rofi xclip btop tree thunar flameshot ttf-jetbrains-mono-nerd picom zsh starship pulseaudio alsa-utils neovim ripgrep fd npm wget unzip python-pynvim lazygit dunst playerctl gruvbox-dark-gtk"
OPT_PKGS="keepassxc mpv discord thunderbird-bin mullvad-vpn-bin logseq-desktop-bin dnsutils transmission"
VIRT_PKGS="qemu-full virt-manager libvirt virt-viewer dnsmasq vde2 bridge-utils openbsd-netcat libguestfs dmidecode"
SYSTEM_DIRS=("$HOME/.oh-my-zsh/custom" "/usr/share/icons/gruvbox-icons/")

function echo_colored() {
    printf "${!1}%s${COL_RESET}\n" "$2"
}

function msg_info() {
    echo_colored "COL_YELLOW" " [i] $1..."
}

function msg_ok() {
    echo_colored "COL_GREEN" " [✓] $1"
}

function msg_error() {
    echo_colored "COL_RED" " [✗] $1"
    return 1
}

function exec_or_exit() {
    if ! "$@" &>/dev/null; then
        msg_error "Error executing $*"
    fi
}

function sym_link_or_exit() {
    local backup_dir target_name target symlink_target backup_target
    backup_dir=$(echo "$2" | sed 's:/*$::')
    target_name=$(basename "$1")
    target="${backup_dir}/${target_name}"

    if [[ ! -d "${backup_dir}/backup" ]]; then
        exec_or_exit sudo mkdir -p "${backup_dir}/backup"
    fi
    
    if [[ -e "$target" ]]; then
        msg_info "File/Dir $target_name already exists in $2. Backing up."
        backup_target="${backup_dir}/backup/${target_name}_$(date +%Y%m%d%H%M%S)"
        exec_or_exit sudo mv "$target" "$backup_target"
    fi

    symlink_target="${INITIAL_PWD}/$1"
    [[ -d "$1" ]] && symlink_target="${symlink_target}/"
    
    exec_or_exit sudo ln -sfn "$symlink_target" "$target"
}

function install_paru() {
    msg_info "Installing paru"
    exec_or_exit git clone "https://aur.archlinux.org/paru-bin.git" "$TMP_DIR/paru-bin"
    exec_or_exit cd "$TMP_DIR/paru-bin" 
    exec_or_exit sudo -u "$(logname)" makepkg -si --noconfirm
    msg_ok "Paru is installed"
}

function install_base_packages() {
    msg_info "Installing base packages"
    exec_or_exit paru -S $BASE_PKGS --needed --noconfirm
    exec_or_exit sudo systemctl enable ly
    msg_ok "Base packages installed"
}

function install_optional_packages() {
    msg_info "Installing optional packages"
    exec_or_exit paru -S $OPT_PKGS --needed
    msg_ok "Optional packages installed"
}

function install_virtualization_packages() {
    msg_info "Installating KVM / QEMU"
    exec_or_exit paru -S $VIRT_PKGS --needed --noconfirm 
    exec_or_exit sudo systemctl enable --now libvirtd
    exec_or_exit sudo sed -i 's/#unix_sock_group = "libvirt"/unix_sock_group = "libvirt"/' /etc/libvirt/libvirtd.conf
    exec_or_exit sudo sed -i 's/#unix_sock_rw_perms = "0770"/unix_sock_rw_perms = "0770"/' /etc/libvirt/libvirtd.conf
    exec_or_exit sudo usermod -a -G libvirt "$(logname)"
    msg_ok "Virtualization packages installed"
}

function install_nvidia_drivers() {
    msg_info "Installing Nvidia drivers"
    exec_or_exit paru -S nvidia nvidia-utils nvidia-settings --needed --noconfirm
    exec_or_exit sudo sed -i 's/MODULES=()/MODULES=(nvidia nvidia-modeset nvidia-drm)/' /etc/mkinitcpio.conf
    exec_or_exit sudo mkinitcpio -P
    msg_ok "Nvidia Drivers installed"
}

function link_config_files() {
    msg_info "Linking configuration files"
    sym_link_or_exit ".config/" "$HOME"
    sym_link_or_exit ".wallpaper/" "$HOME"
    sym_link_or_exit "bin/.zshrc" "$HOME"
    msg_ok "Configuration files linked"
}

function install_gruvbox_theme() {
    msg_info "Installing Theme"
    exec_or_exit git clone "https://github.com/SylEleuth/gruvbox-plus-icon-pack.git" "$TMP_DIR/gruvbox-icons"
    exec_or_exit sudo mkdir -p "${SYSTEM_DIRS[1]}"
    exec_or_exit sudo mv "$TMP_DIR/gruvbox-icons/Gruvbox-Plus-Dark/"* "${SYSTEM_DIRS[1]}"
    msg_ok "Theme installed"
}

function install_omz() {
    msg_info "Installing OhMyZsh"
    exec_or_exit git clone "https://github.com/zsh-users/zsh-autosuggestions" "${SYSTEM_DIRS[0]}/plugins/zsh-autosuggestions"
    exec_or_exit git clone "https://github.com/zsh-users/zsh-syntax-highlighting.git" "${SYSTEM_DIRS[0]}/plugins/zsh-syntax-highlighting"
    msg_ok "OhMyZsh installed"
}

function setup_network() {
    msg_info "Setting up network"
    exec_or_exit sudo mkdir -p /etc/systemd/network/
    exec_or_exit sudo cp -r network/* /etc/systemd/network/
    msg_ok "Network setup complete"
}

function main() {
    exec_or_exit sudo pacman -S base-devel sudo --needed --noconfirm
    install_paru
    install_base_packages

    read -rp "Install OhMyZsh & Plugins? (y/N): " omz_response
    [[ $omz_response =~ ^[Yy]$ ]] && install_omz

    link_config_files
    install_gruvbox_theme

    read -rp "Install Nvidia drivers? (y/N): " nvidia_response
    [[ $nvidia_response =~ ^[Yy]$ ]] && install_nvidia_drivers

    read -rp "Install Virtualization packages? (y/N): " virt_response
    [[ $virt_response =~ ^[Yy]$ ]] && install_virtualization_packages

    read -rp "Install Optional packages? (y/N): " opt_response
    [[ $opt_response =~ ^[Yy]$ ]] && install_optional_packages

    read -rp "Setup network and move network folder content to /etc/systemd/network/? (y/N): " network_response
    [[ $network_response =~ ^[Yy]$ ]] && setup_network

    msg_ok "Installation successful. Please restart the system to apply changes."
}

main "$@"

