from flask import Blueprint
from flask import Flask, request, session, redirect, url_for
from cas import CASClient

app = Flask(__name__)
app.secret_key = 'V7nlCN90LPHOTA9PGGyf'

