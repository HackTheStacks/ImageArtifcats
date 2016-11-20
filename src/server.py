from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")

def hello():
    cmd = ["ls","-l"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out
if __name__ == "__main__" :
    app.run()
