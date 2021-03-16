#!/bin/bash
status_log=$(git status -sb)
# 這裡使用的是 master 分支，根據需求自行修改
if [ "$status_log" == "## master...origin/master" ];then
  echo "nothing to commit, working tree clean"
else
  git add .&&git commit -m "update by github actions `date +'%Y-%m-%d %H:%M:%S'`"&&git push origin master
fi
