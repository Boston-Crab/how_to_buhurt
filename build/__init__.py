from flask import Flask, render_template, request, redirect, session
#import psycopg2
import os

app = Flask(__name__)

from build import views