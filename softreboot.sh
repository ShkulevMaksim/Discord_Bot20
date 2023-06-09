#!/bin/bash
tmux kill-session -t Bot
tmux new-session -s Bot -d 'python3 ./bot.py'
