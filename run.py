from dotenv import load_dotenv

from works import create_app

load_dotenv('.env')

if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=5000, debug=True)
