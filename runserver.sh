#!/bin/bash


# Fungsi untuk mencetak teks dengan warna
print_color_text() {
    local color=$1
    local text=$2
    echo -e "\e[${color}m${text}\e[0m"
}

# Menampilkan opsi dengan warna yang berbeda
echo "$(print_color_text '1;33' 'Pilih operasi yang ingin dijalankan:')"
echo "$(print_color_text '1;36' '1. Run Server')"
echo "$(print_color_text '1;34' '2. python manage.py makemigrations')"
echo "$(print_color_text '1;32' '3. python manage.py migrate')"

read -p "Masukkan nomor operasi: " choice

case $choice in
    1)
        gnome-terminal --tab --title="tailwind CSS" -- bash -c "npm run tailwind"
        gnome-terminal --tab --title="Django Server Running" -- bash -c "python manage.py runserver"
        ;;
   
    2)
        gnome-terminal --tab --title="Django Server Running" -- bash -c "python manage.py makemigrations"
        ;;
    3)
        gnome-terminal --tab --title="Django Server Running" -- bash -c "python manage.py migrate"
        ;;
    *)
        echo "Pilihan tidak valid."
        ;;
esac
