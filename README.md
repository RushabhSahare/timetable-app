# timetable-app

## Setup (Ubuntu/Debian EC2)

# Update packages
sudo apt update && sudo apt upgrade -y

# Install Python and venv
sudo apt install python3 python3-pip python3-venv -y

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Access in browser
http://<EC2-public-ip>:5000
