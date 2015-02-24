docker run -it \
-v /media/root/sf_Latexwww:/var/www \
-h="DOCK-Latex" \
ubuntu/latex:v000003

# echo "IP container 'boot2docker ip': " ; boot2docker ip 
# docker ps | awk -F " " '{print $1, $2, $12, $13, $14, $15, $16, $17, $18}'
