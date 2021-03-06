"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs as get_so_jobs
from remote import get_jobs as get_remote_jobs
from wwr import get_jobs as get_wwr_jobs
from exporter import save_to_file





def get_jobs(word):
  so_jobs= get_so_jobs(word)
  remote_jobs = get_remote_jobs(word)
  wwr_jobs = get_wwr_jobs(word)
  jobs = so_jobs + remote_jobs + wwr_jobs
  return jobs





app = Flask("SupperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else: 
      jobs = get_jobs(word)
      db[word]= jobs
    # print(jobs)
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")



app.run(host="0.0.0.0")

