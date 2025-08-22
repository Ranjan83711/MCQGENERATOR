MCQ Generator 🎯

An AI-powered Multiple Choice Question (MCQ) Generator built with LangChain.
This project takes custom text or PDFs as input and automatically generates MCQs with answers and distractors.
It’s designed to help educators, students, and trainers quickly create quizzes, practice tests, and assessments.

✨ Features

📄 Upload text or PDF documents as input

🧠 Uses LangChain + OpenAI LLMs for intelligent question generation

❓ Generates meaningful MCQs with multiple answer options

🎯 Identifies correct answers and creates distractors

🌐 Simple Streamlit web interface for easy usage

⚡ Saves time for teachers, learners, and trainers

🛠️ Tech Stack

1.Python
2.LangChain
3.OpenAI API
4.PyPDF (for PDF text extraction)
5.Streamlit (for web app UI)

AWS Deployment :

first login to the AWS: https://aws.amazon.com/console/

search about the EC2

you need to config the UBUNTU Machine

launch the instance

update the machine:

sudo apt update

sudo apt-get update

sudo apt upgrade -y

sudo apt install git curl unzip tar make sudo vim wget -y

git clone "Your-repository"

sudo apt install python3-pip

pip3 install -r requirements.txt

python3 -m streamlit run StreamlitAPP.py

if you want to add openai api key
create .env file in your server touch .env
vi .env #press insert #copy your api key and paste it there #press and then :wq and hit enter

go with security and add the inbound rule add the port 8501
