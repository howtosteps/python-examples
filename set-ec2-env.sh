sudo yum update -y
sudo yum install git -y

python3 -m venv .env
source ~/.env/bin/activate

pip install --upgrade pip

echo "source ${HOME}/.env/bin/activate" >> ${HOME}/.bashrc