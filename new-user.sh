echo "Creating new user: $1" 
sudo useradd -G jupyterhub-users $1

echo "Copying over workshop materials"
sudo cp -r *.ipynb /home/$1/
sudo cp -r *.py /home/$1/

echo "Resetting permissions"
sudo chown -R $1:jupyterhub-users /home/$1/
