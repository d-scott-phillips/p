#!/usr/bin/env python3
import os, sys
dir = os.path.dirname(os.path.realpath(sys.argv[0]))
torm = [e for e in os.scandir(dir)
    if e.name not in ['opt', 'symlink.py', 'activate', '.git', '.gitignore']]
tormdir = []
while len(torm) > 0:
  e = torm.pop(0)
  if e.is_dir():
    torm.extend(os.scandir(e.path))
    tormdir.insert(0, e)
  else:
    os.remove(e.path)
for e in tormdir:
  os.rmdir(e.path)
toln = [(e, p) for p in os.scandir(os.path.join(dir, 'opt'))
    for e in os.scandir(p.path)]
dirs = set([])
conflicts = set([])
while len(toln) > 0:
  e, p = toln.pop(0)
  dst = os.path.join(dir, os.path.relpath(e.path, p.path))
  if e.is_dir():
    if dst not in dirs:
      dirs.add(dst)
      os.mkdir(dst)
    toln.extend((f, p) for f in os.scandir(e.path))
  else:
    try:
      os.symlink(os.path.relpath(e.path, os.path.dirname(dst)), dst)
    except FileExistsError:
      if dst not in conflicts:
        conflicts.add(dst)
        print('conflict: ' + os.path.relpath(dst, dir))
