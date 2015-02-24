echo 'sudo mkdir -p /media/root/sf_Latexwww' | boot2docker ssh
echo 'sudo mount -t vboxsf Latexwww /media/root/sf_Latexwww' | boot2docker ssh

# -v /media/root/sf_Latexwww:/var/www